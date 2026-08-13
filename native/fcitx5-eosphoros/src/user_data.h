#pragma once

#include "dictionary.h"

#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>

namespace eosphoros {

class UserData {
public:
    explicit UserData(std::string path = {});
    bool load(std::string *error = nullptr);
    bool record(const std::string &code, const std::string &text,
                bool custom = false, std::string *error = nullptr);
    bool removeCustom(const std::string &code, const std::string &text,
                      std::string *error = nullptr);
    bool undoLastCustom(std::string *error = nullptr);
    bool clearCustom(std::string *error = nullptr);
    std::vector<Candidate> candidates(const std::string &code) const;
    std::uint64_t frequency(const std::string &code,
                            const std::string &text) const;
    const std::string &path() const { return path_; }

private:
    struct Entry {
        std::uint64_t frequency = 0;
        bool custom = false;
        std::uint64_t sequence = 0;
    };
    bool save(std::string *error);
    static std::string key(const std::string &code, const std::string &text);

    std::string path_;
    std::unordered_map<std::string, Entry> entries_;
    std::uint64_t sequence_ = 0;
};

} // namespace eosphoros
