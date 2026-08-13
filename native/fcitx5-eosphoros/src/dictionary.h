#pragma once

#include "topup.h"

#include <cstddef>
#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>

namespace eosphoros {

struct DictionaryEntry {
    std::string text;
    std::string code;
    std::int32_t weight = 0;
    std::uint32_t ordinal = 0;
};

struct Candidate {
    std::string text;
    std::string code;
    bool completion = false;
};

class Dictionary {
public:
    bool load(const std::string &path, std::string *error = nullptr);
    std::vector<Candidate> lookup(const std::string &input,
                                  std::size_t limit = 50) const;
    bool hasPrefix(const std::string &input) const;
    std::size_t size() const { return entryCount_; }
    const TopupConfig &topupConfig() const { return topupConfig_; }
    std::size_t pageSize() const { return pageSize_; }

private:
    std::unordered_map<std::string, std::vector<DictionaryEntry>> byCode_;
    std::vector<std::string> sortedCodes_;
    std::size_t entryCount_ = 0;
    TopupConfig topupConfig_;
    std::size_t pageSize_ = 5;
};

} // namespace eosphoros
