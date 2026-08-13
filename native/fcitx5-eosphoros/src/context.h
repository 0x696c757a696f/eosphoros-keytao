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

struct TopupState {
    TopupAction lastAction = TopupAction::Continue;
    std::size_t transitions = 0;
};

class EosphorosContext {
public:
    explicit EosphorosContext(const Dictionary *dictionary);

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
    std::size_t pageSize() const { return dictionary_->pageSize(); }
    const TopupState &topupState() const { return topupState_; }

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
    TopupState topupState_;
};

} // namespace eosphoros
