#include "auxiliary.h"

#include <array>
#include <cstdint>
#include <fstream>

namespace eosphoros {
namespace {
constexpr std::array<char, 8> kMagic{'E','O','S','A','U','X','0','1'};

bool number(std::istream &source, std::uint32_t &value) {
    std::array<unsigned char, 4> bytes{};
    if (!source.read(reinterpret_cast<char *>(bytes.data()), bytes.size())) return false;
    value = static_cast<std::uint32_t>(bytes[0]) |
            (static_cast<std::uint32_t>(bytes[1]) << 8) |
            (static_cast<std::uint32_t>(bytes[2]) << 16) |
            (static_cast<std::uint32_t>(bytes[3]) << 24);
    return true;
}

bool text(std::istream &source, std::string &value) {
    std::uint32_t size = 0;
    if (!number(source, size) || size > 16U * 1024U * 1024U) return false;
    value.resize(size);
    return size == 0 || source.read(value.data(), size).good();
}
} // namespace

bool AuxiliaryData::load(const std::string &path, std::string *error) {
    std::ifstream source(path, std::ios::binary);
    std::array<char, 8> magic{};
    std::uint32_t pronCount = 0, emojiCount = 0;
    if (!source || !source.read(magic.data(), magic.size()) || magic != kMagic ||
        !number(source, pronCount) || !number(source, emojiCount)) {
        if (error) *error = "invalid native auxiliary data";
        return false;
    }
    std::unordered_map<std::string, std::string> pron;
    std::unordered_map<std::string, std::vector<std::string>> emoji;
    for (std::uint32_t i = 0; i < pronCount; ++i) {
        std::string key, value;
        if (!text(source, key) || !text(source, value)) return false;
        pron.emplace(std::move(key), std::move(value));
    }
    for (std::uint32_t i = 0; i < emojiCount; ++i) {
        std::string key; std::uint32_t count = 0;
        if (!text(source, key) || !number(source, count) || count > 1000) return false;
        auto &values = emoji[key]; values.reserve(count);
        for (std::uint32_t j = 0; j < count; ++j) {
            std::string value;
            if (!text(source, value)) return false;
            values.push_back(std::move(value));
        }
    }
    pronunciation_ = std::move(pron); emoji_ = std::move(emoji);
    return true;
}

const std::string *AuxiliaryData::pronunciation(const std::string &value) const {
    const auto found = pronunciation_.find(value);
    return found == pronunciation_.end() ? nullptr : &found->second;
}

const std::vector<std::string> *AuxiliaryData::emoji(const std::string &value) const {
    const auto found = emoji_.find(value);
    return found == emoji_.end() ? nullptr : &found->second;
}
} // namespace eosphoros
