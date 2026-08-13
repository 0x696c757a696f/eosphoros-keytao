#pragma once

#include <cstddef>
#include <string>
#include <string_view>

namespace eosphoros {

enum class TopupAction {
    Continue,
    CommitFirst,
    CommitSelected,
    CommitAndStartNext,
    Clear,
    ClearAndStartNext,
    PassThrough,
    HoldAndConsume,
};

struct TopupConfig {
    std::string topupThis = "bcdefghjklmnpqrstwxyz";
    std::string topupKeys = "avuio;";
    std::size_t minLength = 4;
    std::size_t maxLength = 6;
    bool autoClear = true;
    bool topupCommand = false;
};

struct LookupResult {
    bool hasCandidate = false;
    bool selectedCommittable = false;
    std::size_t selectedIndex = 0;
};

struct TopupDecision {
    TopupAction action = TopupAction::Continue;
};

class TopupPolicy {
public:
    explicit TopupPolicy(TopupConfig config = {}) : config_(config) {}

    TopupDecision process(std::string_view input, char next,
                          const LookupResult &lookup) const;

private:
    bool isTopup(char key) const;
    TopupConfig config_;
};

} // namespace eosphoros
