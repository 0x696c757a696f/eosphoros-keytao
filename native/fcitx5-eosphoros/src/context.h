#pragma once

#include "dictionary.h"
#include "topup.h"

#include <cstddef>
#include <string>
#include <vector>

namespace eosphoros {

enum class Mode { Normal, English, ReversePinyin, ReverseLiangfen, ReverseGBK };

struct KeyResult {
    bool consumed = false;
    std::vector<std::string> commits;
};

class Context {
public:
    explicit Context(const Dictionary *dictionary,
                     TopupConfig topupConfig = {});

    KeyResult type(char key);
    KeyResult space();
    KeyResult enter();
    KeyResult select(std::size_t index);
    KeyResult backspace();
    KeyResult escape();
    bool moveSelection(int delta);
    void reset();

    const std::string &input() const { return input_; }
    const std::vector<Candidate> &candidates() const { return candidates_; }
    std::size_t selected() const { return selected_; }
    Mode mode() const { return mode_; }

private:
    bool hasCommittableCandidate() const;
    void refresh();
    KeyResult commit(std::size_t index);

    const Dictionary *dictionary_;
    TopupPolicy topup_;
    std::string input_;
    std::vector<Candidate> candidates_;
    std::size_t selected_ = 0;
    Mode mode_ = Mode::Normal;
};

} // namespace eosphoros
