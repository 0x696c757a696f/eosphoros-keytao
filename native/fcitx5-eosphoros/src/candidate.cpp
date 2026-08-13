#include "candidate.h"

#include "engine.h"
#include <fcitx/text.h>

namespace eosphoros::fcitx5 {

CandidateWord::CandidateWord(Engine *engine, std::size_t index,
                             const std::string &text, const std::string &code,
                             bool completion)
    : fcitx::CandidateWord(fcitx::Text(text)), engine_(engine), index_(index) {
    (void)code;
    (void)completion;
}

void CandidateWord::select(fcitx::InputContext *inputContext) const {
    engine_->selectCandidate(inputContext, index_);
}

} // namespace eosphoros::fcitx5
