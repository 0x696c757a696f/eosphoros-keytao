#include "candidate.h"

#include "engine.h"
#include <fcitx/text.h>

namespace eosphoros::fcitx5 {
namespace {
fcitx::Text candidateText(const std::string &value, const std::string &comment) {
    fcitx::Text result(value);
    if (!comment.empty()) {
        result.append(" " + comment, fcitx::TextFormatFlag::DontCommit);
    }
    return result;
}
} // namespace

CandidateWord::CandidateWord(EosphorosEngine *engine, std::size_t index,
                             const std::string &text, const std::string &code,
                             bool completion, const std::string &comment)
    : fcitx::CandidateWord(candidateText(text, comment)), engine_(engine), index_(index) {
    (void)code;
    (void)completion;
}

void CandidateWord::select(fcitx::InputContext *inputContext) const {
    engine_->selectCandidate(inputContext, index_);
}

} // namespace eosphoros::fcitx5
