#include "topup.h"

namespace eosphoros {

bool TopupPolicy::isTopup(char key) const {
    return config_.topupKeys.find(key) != std::string_view::npos;
}

TopupAction TopupPolicy::decide(std::string_view input, char next,
                                bool hasCommittableCandidate) const {
    if (input.empty() || input == ";") {
        return TopupAction::Continue;
    }
    if (config_.topupCommand && isTopup(input.front())) {
        return TopupAction::Continue;
    }

    const bool previousTopup = isTopup(input.back());
    const bool nextTopup = isTopup(next);
    const bool fixedRule = input.size() >= config_.maxLength ||
                           (previousTopup && !nextTopup) ||
                           (input.size() >= config_.minLength &&
                            !previousTopup && !nextTopup);
    if (!fixedRule) {
        return TopupAction::Continue;
    }
    if (hasCommittableCandidate) {
        return TopupAction::CommitAndStartNext;
    }
    return config_.autoClear ? TopupAction::ClearAndConsumeNext
                             : TopupAction::Continue;
}

} // namespace eosphoros
