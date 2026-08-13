#include "context.h"
#include "special.h"

#include <algorithm>
#include <cctype>

namespace eosphoros {

namespace {
Mode modeForInput(const std::string &input) {
    if (input.empty()) {
        return Mode::Normal;
    }
    switch (input.front()) {
    case 'i': return Mode::English;
    case 'u': return Mode::ReversePinyin;
    case 'v': return Mode::ReverseLiangfen;
    case 'o': return Mode::ReverseGBK;
    case '=': return Mode::Calculator;
    default: return Mode::Normal;
    }
}
} // namespace

EosphorosContext::EosphorosContext(const Dictionary *dictionary,
                                   const AuxiliaryData *auxiliary,
                                   UserData *userData)
    : dictionary_(dictionary), auxiliary_(auxiliary),
      userData_(userData),
      topup_(dictionary->topupConfig()) {}

void EosphorosContext::refresh() {
    mode_ = modeForInput(input_);
    candidates_ = specialCandidates(input_);
    if (candidates_.empty() && !input_.empty() && mode_ != Mode::Calculator) {
        candidates_ = dictionary_->lookup(input_, mode_);
    }
    if (userData_ && mode_ == Mode::Normal && !input_.empty()) {
        auto custom = userData_->candidates(input_);
        for (auto it = custom.rbegin(); it != custom.rend(); ++it) {
            const auto duplicate = std::find_if(candidates_.begin(), candidates_.end(),
                [&it](const Candidate &candidate) { return candidate.text == it->text; });
            if (duplicate == candidates_.end()) candidates_.insert(candidates_.begin(), *it);
        }
        std::stable_sort(candidates_.begin(), candidates_.end(),
            [this](const Candidate &a, const Candidate &b) {
                if (a.completion != b.completion) return !a.completion;
                return userData_->frequency(input_, a.text) >
                       userData_->frequency(input_, b.text);
            });
    }
    if (auxiliary_) {
        if (mode_ == Mode::ReversePinyin || mode_ == Mode::ReverseLiangfen ||
            mode_ == Mode::ReverseGBK) {
            for (auto &candidate : candidates_) {
                if (const auto *value = auxiliary_->pronunciation(candidate.text)) {
                    candidate.comment = *value;
                }
            }
        } else if (mode_ == Mode::Normal) {
            const auto originalSize = candidates_.size();
            for (std::size_t i = 0; i < originalSize; ++i) {
                if (candidates_[i].completion) continue;
                const auto *values = auxiliary_->emoji(candidates_[i].text);
                if (!values) continue;
                for (const auto &value : *values) {
                    const auto duplicate = std::any_of(
                        candidates_.begin(), candidates_.end(),
                        [&value](const Candidate &candidate) {
                            return candidate.text == value;
                        });
                    if (!duplicate) {
                        candidates_.push_back(
                            {value, candidates_[i].code, false, "Emoji"});
                    }
                }
            }
        }
    }
    if (candidates_.empty()) {
        selected_ = 0;
    } else {
        selected_ = std::min(selected_, candidates_.size() - 1);
    }
}

std::string EosphorosContext::displayInput() const {
    if (mode_ != Mode::Normal && mode_ != Mode::Calculator && input_.size() > 1) {
        return input_.substr(1);
    }
    return input_;
}

bool EosphorosContext::hasCommittableCandidate() const {
    return selected_ < candidates_.size() && !candidates_[selected_].completion;
}

bool EosphorosContext::hasExactCandidate() const {
    return std::any_of(candidates_.begin(), candidates_.end(),
                       [](const Candidate &candidate) {
                           return !candidate.completion;
                       });
}

KeyResult EosphorosContext::type(char key) {
    KeyResult result;
    if (!(key >= 'a' && key <= 'z') && key != ';' && key != '\'' && key != '=') {
        return result;
    }

    // These prefixes are translator namespaces in the Rime scheme.  They do
    // not participate in key-topup or normal-code auto fallback.
    if (mode_ != Mode::Normal) {
        input_.push_back(key);
        selected_ = 0;
        refresh();
        result.consumed = true;
        return result;
    }

    const LookupResult lookup{!candidates_.empty(), hasCommittableCandidate(),
                              selected_};
    const auto action = topup_.process(input_, key, lookup).action;
    topupState_.lastAction = action;
    if (action == TopupAction::CommitAndStartNext) {
        ++topupState_.transitions;
        result.commits.push_back(candidates_[selected_].text);
        if (userData_ && candidates_[selected_].comment != "Emoji")
            userData_->record(input_, candidates_[selected_].text);
        input_.assign(1, key);
        selected_ = 0;
        refresh();
        result.consumed = true;
        return result;
    }
    if (action == TopupAction::ClearAndStartNext) {
        input_.assign(1, key);
        candidates_.clear();
        selected_ = 0;
        mode_ = Mode::Normal;
        ++topupState_.transitions;
        refresh();
        result.consumed = true;
        return result;
    }
    if (action == TopupAction::HoldAndConsume) {
        result.consumed = true;
        return result;
    }

    // Rime's auto_fallback switch is enabled by default.  When appending a
    // normal code would leave no exact candidate, commit the current exact
    // candidate and let the new key begin the next segment.  Fixed top-up is
    // evaluated first above, matching eosphoros_topup.lua.
    if (hasCommittableCandidate()) {
        const auto previous = candidates_[selected_].text;
        input_.push_back(key);
        selected_ = 0;
        refresh();
        if (!hasExactCandidate()) {
            result.commits.push_back(previous);
            if (userData_) userData_->record(input_.substr(0, input_.size() - 1), previous);
            input_.assign(1, key);
            selected_ = 0;
            refresh();
            ++topupState_.transitions;
        }
        result.consumed = true;
        return result;
    }

    input_.push_back(key);
    selected_ = 0;
    refresh();
    result.consumed = true;
    return result;
}

KeyResult EosphorosContext::typeCalculator(char key) {
    if (mode_ != Mode::Calculator || !isCalculatorCharacter(key)) return {};
    input_.push_back(key);
    selected_ = 0;
    refresh();
    return {true, {}};
}

KeyResult EosphorosContext::commit(std::size_t index) {
    KeyResult result{true, {}};
    if (index < candidates_.size()) {
        result.commits.push_back(candidates_[index].text);
        if (userData_ && mode_ == Mode::Normal && candidates_[index].comment != "Emoji")
            userData_->record(input_, candidates_[index].text);
    }
    reset();
    return result;
}

KeyResult EosphorosContext::space() {
    if (input_.empty()) {
        return {};
    }
    if (!candidates_.empty()) {
        return commit(selected_);
    }
    reset();
    return {true, {}};
}

KeyResult EosphorosContext::enter() {
    if (input_.empty()) {
        return {};
    }
    KeyResult result{true, {input_}};
    reset();
    return result;
}

KeyResult EosphorosContext::select(std::size_t index) {
    if (input_.empty() || index >= candidates_.size()) {
        return {};
    }
    return commit(index);
}

KeyResult EosphorosContext::symbol(const std::string &text) {
    KeyResult result{true, {}};
    if (!input_.empty()) {
        if (hasCommittableCandidate()) {
            result.commits.push_back(candidates_[selected_].text);
        } else {
            result.commits.push_back(input_);
        }
    }
    result.commits.push_back(text);
    reset();
    return result;
}

KeyResult EosphorosContext::backspace() {
    if (input_.empty()) {
        return {};
    }
    input_.pop_back();
    selected_ = 0;
    refresh();
    return {true, {}};
}

KeyResult EosphorosContext::escape() {
    if (input_.empty()) {
        return {};
    }
    reset();
    return {true, {}};
}

bool EosphorosContext::moveSelection(int delta) {
    if (candidates_.empty()) {
        return false;
    }
    const auto count = static_cast<int>(candidates_.size());
    const auto current = static_cast<int>(selected_);
    selected_ = static_cast<std::size_t>(std::clamp(current + delta, 0, count - 1));
    return true;
}

void EosphorosContext::reset() {
    input_.clear();
    candidates_.clear();
    selected_ = 0;
    mode_ = Mode::Normal;
    topupState_ = {};
}

} // namespace eosphoros
