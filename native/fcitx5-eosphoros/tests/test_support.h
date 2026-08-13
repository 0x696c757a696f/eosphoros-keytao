#pragma once

#include <stdexcept>
#include <string>
#include <vector>

inline void require(bool value, const std::string &message) {
    if (!value) {
        throw std::runtime_error(message);
    }
}

inline std::vector<std::string> split(const std::string &text, char delimiter) {
    std::vector<std::string> result;
    std::string item;
    for (const char value : text) {
        if (value == delimiter) {
            result.push_back(item);
            item.clear();
        } else {
            item.push_back(value);
        }
    }
    result.push_back(item);
    return result;
}
