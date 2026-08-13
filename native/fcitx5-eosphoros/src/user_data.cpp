#include "user_data.h"

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <sstream>

namespace eosphoros {
namespace {
bool valid(const std::string &value) {
    return !value.empty() && value.find_first_of("\t\r\n") == std::string::npos;
}
} // namespace

UserData::UserData(std::string path) : path_(std::move(path)) {}

std::string UserData::key(const std::string &code, const std::string &text) {
    return code + '\0' + text;
}

bool UserData::load(std::string *error) {
    entries_.clear();
    sequence_ = 0;
    if (path_.empty() || !std::filesystem::exists(path_)) return true;
    std::ifstream source(path_);
    std::string line;
    while (std::getline(source, line)) {
        if (line.empty() || line.front() == '#') continue;
        std::istringstream row(line);
        std::string code, text, count, kind, sequence;
        if (!std::getline(row, code, '\t') || !std::getline(row, text, '\t') ||
            !std::getline(row, count, '\t') || !std::getline(row, kind, '\t') ||
            !valid(code) || !valid(text)) {
            if (error) *error = "invalid user data row";
            return false;
        }
        try {
            std::getline(row, sequence);
            const std::uint64_t order = sequence.empty()
                                            ? 0
                                            : static_cast<std::uint64_t>(
                                                  std::stoull(sequence));
            entries_[key(code, text)] = {std::stoull(count), kind == "custom", order};
            sequence_ = std::max(sequence_, order);
        } catch (...) {
            if (error) *error = "invalid user data frequency";
            return false;
        }
    }
    return source.eof();
}

bool UserData::save(std::string *error) {
    if (path_.empty()) return true;
    const std::filesystem::path target(path_);
    std::error_code ec;
    std::filesystem::create_directories(target.parent_path(), ec);
    const auto temporary = target.string() + ".tmp";
    std::ofstream output(temporary, std::ios::trunc);
    if (!output) { if (error) *error = "cannot write user data"; return false; }
    output << "# EOSPHOROS_USER_V2\n";
    std::vector<std::pair<std::string, Entry>> rows(entries_.begin(), entries_.end());
    std::sort(rows.begin(), rows.end(), [](const auto &a, const auto &b) {
        return a.first < b.first;
    });
    for (const auto &[joined, entry] : rows) {
        const auto separator = joined.find('\0');
        output << joined.substr(0, separator) << '\t' << joined.substr(separator + 1)
               << '\t' << entry.frequency << '\t'
               << (entry.custom ? "custom" : "learned") << '\t'
               << entry.sequence << '\n';
    }
    output.close();
    if (!output) { if (error) *error = "cannot flush user data"; return false; }
    std::filesystem::rename(temporary, target, ec);
    if (ec) {
        std::filesystem::remove(target, ec); ec.clear();
        std::filesystem::rename(temporary, target, ec);
    }
    if (ec) { if (error) *error = "cannot replace user data"; return false; }
    return true;
}

bool UserData::record(const std::string &code, const std::string &text,
                      bool custom, std::string *error) {
    if (!valid(code) || !valid(text)) return false;
    auto &entry = entries_[key(code, text)];
    ++entry.frequency;
    entry.custom = entry.custom || custom;
    if (custom) entry.sequence = ++sequence_;
    return save(error);
}

bool UserData::removeCustom(const std::string &code, const std::string &text,
                            std::string *error) {
    const auto found = entries_.find(key(code, text));
    if (found == entries_.end() || !found->second.custom) return false;
    entries_.erase(found);
    return save(error);
}

bool UserData::undoLastCustom(std::string *error) {
    auto latest = entries_.end();
    for (auto it = entries_.begin(); it != entries_.end(); ++it) {
        if (it->second.custom &&
            (latest == entries_.end() || it->second.sequence > latest->second.sequence))
            latest = it;
    }
    if (latest == entries_.end()) return false;
    entries_.erase(latest);
    return save(error);
}

bool UserData::clearCustom(std::string *error) {
    bool changed = false;
    for (auto it = entries_.begin(); it != entries_.end();) {
        if (it->second.custom) { it = entries_.erase(it); changed = true; }
        else ++it;
    }
    return changed && save(error);
}

std::uint64_t UserData::frequency(const std::string &code,
                                  const std::string &text) const {
    const auto found = entries_.find(key(code, text));
    return found == entries_.end() ? 0 : found->second.frequency;
}

std::vector<Candidate> UserData::candidates(const std::string &code) const {
    std::vector<Candidate> result;
    const auto prefix = code + '\0';
    for (const auto &[joined, entry] : entries_) {
        if (entry.custom && joined.compare(0, prefix.size(), prefix) == 0) {
            result.push_back({joined.substr(prefix.size()), code, false, "自造词"});
        }
    }
    std::sort(result.begin(), result.end(), [this, &code](const auto &a, const auto &b) {
        return frequency(code, a.text) > frequency(code, b.text);
    });
    return result;
}

} // namespace eosphoros
