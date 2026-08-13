#pragma once

#include "dictionary.h"

#include <string>
#include <unordered_map>
#include <vector>

namespace eosphoros {

class AuxiliaryData {
public:
    bool load(const std::string &path, std::string *error = nullptr);
    const std::string *pronunciation(const std::string &text) const;
    const std::vector<std::string> *emoji(const std::string &text) const;

private:
    std::unordered_map<std::string, std::string> pronunciation_;
    std::unordered_map<std::string, std::vector<std::string>> emoji_;
};

} // namespace eosphoros
