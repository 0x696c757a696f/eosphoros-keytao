#pragma once

#include <cstddef>
#include <string_view>

namespace eosphoros {

enum class TopupAction { Continue, CommitAndStartNext, ClearAndConsumeNext };

struct TopupConfig {
    std::string_view topupKeys = "avuio;";
    std::size_t minLength = 4;
    std::size_t maxLength = 6;
    bool autoClear = true;
    bool topupCommand = false;
};

class TopupPolicy {
public:
    explicit TopupPolicy(TopupConfig config = {}) : config_(config) {}

    TopupAction decide(std::string_view input, char next,
                       bool hasCommittableCandidate) const;

private:
    bool isTopup(char key) const;
    TopupConfig config_;
};

} // namespace eosphoros
