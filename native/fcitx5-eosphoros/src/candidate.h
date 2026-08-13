#pragma once

#include <cstddef>
#include <fcitx/candidatelist.h>

namespace eosphoros::fcitx5 {

class Engine;

class CandidateWord final : public fcitx::CandidateWord {
public:
    CandidateWord(Engine *engine, std::size_t index, const std::string &text,
                  const std::string &code, bool completion);
    void select(fcitx::InputContext *inputContext) const override;

private:
    Engine *engine_;
    std::size_t index_;
};

} // namespace eosphoros::fcitx5
