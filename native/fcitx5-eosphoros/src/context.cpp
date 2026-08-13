#include "context.h"

#include <algorithm>
#include <cctype>

namespace eosphoros {

Context::Context(const Dictionary *dictionary, TopupConfig topupConfig)
    : dictionary_(dictionary), topup_(topupConfig) {}

void Context::refresh() {
    candidates_ = input_.empty() ? std::vector<Candidate>{}
                                 : dictionary_->lookup(input_);
    if (candidates_.empty()) {
        selected_ = 0;
    } else {
        selected_ = std::min(selected_, candidates_.size() - 1);
    }
}

bool Context::hasCommittableCandidate() const {
    return selected_ < candidates_.size() && !candidates_[selected_].completion;
}

KeyResult Context::type(char key) {
    KeyResult result;
    if (!(key >= 'a' && key <= 'z') && key != ';' && key != '\'') {
        return result;
    }

    const auto action = topup_.decide(input_, key, hasCommittableCandidate());
    if (action == TopupAction::CommitAndStartNext) {
        result.commits.push_back(candidates_[selected_].text);
        input_.assign(1, key);
        selected_ = 0;
        refresh();
        result.consumed = true;
        return result;
    }
    if (action == TopupAction::ClearAndConsumeNext) {
        reset();
        result.consumed = true;
        return result;
    }

    input_.push_back(key);
    selected_ = 0;
    refresh();
    result.consumed = true;
    return result;
}

KeyResult Context::commit(std::size_t index) {
    KeyResult result{true, {}};
    if (index < candidates_.size()) {
        result.commits.push_back(candidates_[index].text);
    }
    reset();
    return result;
}

KeyResult Context::space() {
    if (input_.empty()) {
        return {};
    }
    if (!candidates_.empty()) {
        return commit(selected_);
    }
    reset();
    return {true, {}};
}

KeyResult Context::enter() {
    if (input_.empty()) {
        return {};
    }
    KeyResult result{true, {input_}};
    reset();
    return result;
}

KeyResult Context::select(std::size_t index) {
    if (input_.empty() || index >= candidates_.size()) {
        return {};
    }
    return commit(index);
}

KeyResult Context::backspace() {
    if (input_.empty()) {
        return {};
    }
    input_.pop_back();
    selected_ = 0;
    refresh();
    return {true, {}};
}

KeyResult Context::escape() {
    if (input_.empty()) {
        return {};
    }
    reset();
    return {true, {}};
}

bool Context::moveSelection(int delta) {
    if (candidates_.empty()) {
        return false;
    }
    const auto count = static_cast<int>(candidates_.size());
    const auto current = static_cast<int>(selected_);
    selected_ = static_cast<std::size_t>(std::clamp(current + delta, 0, count - 1));
    return true;
}

void Context::reset() {
    input_.clear();
    candidates_.clear();
    selected_ = 0;
    mode_ = Mode::Normal;
}

} // namespace eosphoros
