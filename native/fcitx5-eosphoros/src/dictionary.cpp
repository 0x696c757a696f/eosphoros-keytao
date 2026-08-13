#include "dictionary.h"

#include <algorithm>
#include <array>
#include <fstream>
#include <limits>
#include <unordered_set>

namespace eosphoros {
namespace {

constexpr std::array<char, 8> kMagic{'E', 'O', 'S', 'D', 'I', 'C', 'T', '1'};

template <typename T> bool readNumber(std::istream &stream, T &value) {
    std::array<unsigned char, sizeof(T)> bytes{};
    if (!stream.read(reinterpret_cast<char *>(bytes.data()), bytes.size())) {
        return false;
    }
    value = 0;
    for (std::size_t i = 0; i < bytes.size(); ++i) {
        value |= static_cast<T>(bytes[i]) << (i * 8);
    }
    return true;
}

bool readString(std::istream &stream, std::uint32_t length, std::string &out) {
    if (length > 16U * 1024U * 1024U) {
        return false;
    }
    out.resize(length);
    return length == 0 || stream.read(out.data(), length).good();
}

} // namespace

bool Dictionary::load(const std::string &path, std::string *error) {
    std::ifstream stream(path, std::ios::binary);
    if (!stream) {
        if (error) {
            *error = "cannot open dictionary: " + path;
        }
        return false;
    }

    std::array<char, 8> magic{};
    std::uint32_t version = 0;
    std::uint32_t count = 0;
    if (!stream.read(magic.data(), magic.size()) || magic != kMagic ||
        !readNumber(stream, version) || version != 1 ||
        !readNumber(stream, count)) {
        if (error) {
            *error = "invalid native dictionary header";
        }
        return false;
    }

    std::unordered_map<std::string, std::vector<DictionaryEntry>> loaded;
    for (std::uint32_t ordinal = 0; ordinal < count; ++ordinal) {
        std::uint32_t codeLength = 0;
        std::uint32_t textLength = 0;
        std::uint32_t rawWeight = 0;
        DictionaryEntry entry;
        if (!readNumber(stream, codeLength) || !readNumber(stream, textLength) ||
            !readNumber(stream, rawWeight) || codeLength > 64 ||
            !readString(stream, codeLength, entry.code) ||
            !readString(stream, textLength, entry.text)) {
            if (error) {
                *error = "truncated or invalid native dictionary entry";
            }
            return false;
        }
        entry.weight = static_cast<std::int32_t>(rawWeight);
        entry.ordinal = ordinal;
        loaded[entry.code].push_back(std::move(entry));
    }

    byCode_ = std::move(loaded);
    sortedCodes_.clear();
    sortedCodes_.reserve(byCode_.size());
    for (const auto &[code, entries] : byCode_) {
        (void)entries;
        sortedCodes_.push_back(code);
    }
    std::sort(sortedCodes_.begin(), sortedCodes_.end());
    entryCount_ = count;
    return true;
}

bool Dictionary::hasPrefix(const std::string &input) const {
    const auto it = std::lower_bound(sortedCodes_.begin(), sortedCodes_.end(), input);
    return it != sortedCodes_.end() && it->compare(0, input.size(), input) == 0;
}

std::vector<Candidate> Dictionary::lookup(const std::string &input,
                                          std::size_t limit) const {
    std::vector<Candidate> result;
    std::unordered_set<std::string> seen;
    const auto appendCode = [&](const std::string &code, bool completion,
                                std::vector<Candidate> &out) {
        const auto found = byCode_.find(code);
        if (found == byCode_.end()) {
            return;
        }
        for (const auto &entry : found->second) {
            if (out.size() >= limit) {
                return;
            }
            if (seen.insert(entry.text).second) {
                out.push_back({entry.text, entry.code, completion});
            }
        }
    };

    appendCode(input, false, result);
    std::vector<const DictionaryEntry *> completions;
    auto it = std::lower_bound(sortedCodes_.begin(), sortedCodes_.end(), input);
    while (it != sortedCodes_.end() &&
           it->compare(0, input.size(), input) == 0) {
        if (*it != input) {
            const auto found = byCode_.find(*it);
            for (const auto &entry : found->second) {
                completions.push_back(&entry);
            }
        }
        ++it;
    }
    std::sort(completions.begin(), completions.end(), [](const auto *left,
                                                         const auto *right) {
        return left->ordinal < right->ordinal;
    });
    for (const auto *entry : completions) {
        if (result.size() >= limit) {
            break;
        }
        if (seen.insert(entry->text).second) {
            result.push_back({entry->text, entry->code, true});
        }
    }
    return result;
}

} // namespace eosphoros
