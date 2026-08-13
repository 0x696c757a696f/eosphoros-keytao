#include "topup.h"

namespace eosphoros {

bool TopupPolicy::isTopup(char key) const {
    return config_.topupKeys.find(key) != std::string_view::npos;
}

TopupDecision TopupPolicy::process(std::string_view input, char next,
                                   const LookupResult &lookup) const {
    if (input.empty()) {
        return {};
    }
    if (config_.topupCommand && isTopup(input.front())) {
        return {};
    }

    const bool previousTopup = isTopup(input.back());
    const bool nextTopup = isTopup(next);
    const bool fixedRule = input.size() >= config_.maxLength ||
                           (previousTopup && !nextTopup) ||
                           (input.size() >= config_.minLength &&
                            !previousTopup && !nextTopup);
    if (!fixedRule) {
        return {};
    }
    if (lookup.selectedCommittable) {
        return {TopupAction::CommitAndStartNext};
    }
    return config_.autoClear ? TopupDecision{TopupAction::ClearAndStartNext}
                             : TopupDecision{TopupAction::HoldAndConsume};
}

} // namespace eosphoros
