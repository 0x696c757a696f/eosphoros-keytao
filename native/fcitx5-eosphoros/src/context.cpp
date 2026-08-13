#include "context.h"

#include <algorithm>
#include <cctype>

namespace eosphoros {

EosphorosContext::EosphorosContext(const Dictionary *dictionary)
    : dictionary_(dictionary), topup_(dictionary->topupConfig()) {}

void EosphorosContext::refresh() {
    candidates_ = input_.empty() ? std::vector<Candidate>{}
                                 : dictionary_->lookup(input_);
    if (candidates_.empty()) {
        selected_ = 0;
    } else {
        selected_ = std::min(selected_, candidates_.size() - 1);
    }
}

bool EosphorosContext::hasCommittableCandidate() const {
    return selected_ < candidates_.size() && !candidates_[selected_].completion;
}

KeyResult EosphorosContext::type(char key) {
    KeyResult result;
    if (!(key >= 'a' && key <= 'z') && key != ';' && key != '\'') {
        return result;
    }

    const LookupResult lookup{!candidates_.empty(), hasCommittableCandidate(),
                              selected_};
    const auto action = topup_.process(input_, key, lookup).action;
    topupState_.lastAction = action;
    if (action == TopupAction::CommitAndStartNext) {
        ++topupState_.transitions;
        result.commits.push_back(candidates_[selected_].text);
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

    input_.push_back(key);
    selected_ = 0;
    refresh();
    result.consumed = true;
    return result;
}

KeyResult EosphorosContext::commit(std::size_t index) {
    KeyResult result{true, {}};
    if (index < candidates_.size()) {
        result.commits.push_back(candidates_[index].text);
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
