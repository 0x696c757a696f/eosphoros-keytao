#pragma once

#include <cstddef>
#include <fcitx/candidatelist.h>

namespace eosphoros::fcitx5 {

class EosphorosEngine;

class CandidateWord final : public fcitx::CandidateWord {
public:
    CandidateWord(EosphorosEngine *engine, std::size_t index,
                  const std::string &text,
                  const std::string &code, bool completion);
    void select(fcitx::InputContext *inputContext) const override;

private:
    EosphorosEngine *engine_;
    std::size_t index_;
};

} // namespace eosphoros::fcitx5
