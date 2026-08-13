#pragma once

#include "auxiliary.h"
#include "dictionary.h"
#include "topup.h"

#include <cstddef>
#include <string>
#include <vector>

namespace eosphoros {

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
    explicit EosphorosContext(const Dictionary *dictionary,
                              const AuxiliaryData *auxiliary = nullptr);

    KeyResult type(char key);
    KeyResult typeCalculator(char key);
    KeyResult space();
    KeyResult enter();
    KeyResult select(std::size_t index);
    KeyResult symbol(const std::string &text);
    KeyResult backspace();
    KeyResult escape();
    bool moveSelection(int delta);
    void reset();

    const std::string &input() const { return input_; }
    const std::vector<Candidate> &candidates() const { return candidates_; }
    std::size_t selected() const { return selected_; }
    Mode mode() const { return mode_; }
    std::string displayInput() const;
    std::size_t pageSize() const { return dictionary_->pageSize(); }
    const TopupState &topupState() const { return topupState_; }
    bool hasExactCandidate() const;

private:
    bool hasCommittableCandidate() const;
    void refresh();
    KeyResult commit(std::size_t index);

    const Dictionary *dictionary_;
    const AuxiliaryData *auxiliary_;
    TopupPolicy topup_;
    std::string input_;
    std::vector<Candidate> candidates_;
    std::size_t selected_ = 0;
    Mode mode_ = Mode::Normal;
    TopupState topupState_;
};

} // namespace eosphoros
