#pragma once

#include "dictionary.h"

#include <string>
#include <unordered_map>
#include <vector>

namespace eosphoros {

class AuxiliaryData {
public:
    struct CharacterParts { std::string sound; std::string rhyme; std::string stroke; };
    bool load(const std::string &path, std::string *error = nullptr);
    const std::string *pronunciation(const std::string &text) const;
    const std::vector<std::string> *emoji(const std::string &text) const;
    const CharacterParts *characterParts(const std::string &text) const;
    std::string convert(const std::string &text) const;

private:
    std::unordered_map<std::string, std::string> pronunciation_;
    std::unordered_map<std::string, std::vector<std::string>> emoji_;
    std::unordered_map<std::string, CharacterParts> characterParts_;
    std::unordered_map<std::string, std::string> conversion_;
};

} // namespace eosphoros
