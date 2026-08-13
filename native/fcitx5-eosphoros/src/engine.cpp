#include "engine.h"

#include "candidate.h"
#include <cstdlib>
#include <fcitx-utils/key.h>
#include <fcitx-utils/keysym.h>
#include <fcitx-utils/standardpath.h>
#include <fcitx/addonmanager.h>
#include <fcitx/candidatelist.h>
#include <fcitx/event.h>
#include <fcitx/inputcontext.h>
#include <fcitx/inputpanel.h>
#include <fcitx/instance.h>
#include <fcitx/text.h>

namespace eosphoros::fcitx5 {
namespace {

LogicalKey logicalKey(const fcitx::Key &key) {
    // Some frontends keep Shift in the raw key state. normalize() removes it
    // for letter keys while retaining real Ctrl/Alt/Super shortcuts, matching
    // the Rime processor's plain_code_key behavior.
    const auto normalized = key.normalize();
    if (normalized.hasModifier()) {
        return {};
    }
    const auto symbol = normalized.sym();
    if (symbol >= FcitxKey_a && symbol <= FcitxKey_z) {
        return {KeyKind::Code,
                static_cast<char>('a' + symbol - FcitxKey_a), 0};
    }
    if (symbol >= FcitxKey_A && symbol <= FcitxKey_Z) {
        return {KeyKind::Code,
                static_cast<char>('a' + symbol - FcitxKey_A), 0};
    }
    if (symbol == FcitxKey_semicolon) {
        return {KeyKind::Code, ';', 0};
    }
    if (symbol == FcitxKey_apostrophe) {
        return {KeyKind::Code, '\'', 0};
    }
    switch (symbol) {
    case FcitxKey_space:
        return {KeyKind::Space};
    case FcitxKey_Return:
    case FcitxKey_KP_Enter:
        return {KeyKind::Enter};
    case FcitxKey_BackSpace:
        return {KeyKind::Backspace};
    case FcitxKey_Escape:
        return {KeyKind::Escape};
    case FcitxKey_Up:
        return {KeyKind::Up};
    case FcitxKey_Down:
        return {KeyKind::Down};
    case FcitxKey_Page_Up:
        return {KeyKind::PageUp};
    case FcitxKey_Page_Down:
        return {KeyKind::PageDown};
    default:
        if (symbol >= FcitxKey_1 && symbol <= FcitxKey_9) {
            return {KeyKind::Select, '\0',
                    static_cast<std::size_t>(symbol - FcitxKey_1)};
        }
        return {};
    }
}

} // namespace

EosphorosEngine::EosphorosEngine(fcitx::Instance *instance)
    : instance_(instance),
      stateFactory_([this](fcitx::InputContext &inputContext) {
          return new State(&inputContext, &dictionary_);
      }) {
    instance_->inputContextManager().registerProperty("eosphorosNativeState",
                                                       &stateFactory_);

    std::string path;
    if (const auto *overridePath = std::getenv("EOSPHOROS_NATIVE_DICTIONARY")) {
        path = overridePath;
    } else {
        path = fcitx::StandardPath::global().locate(
            fcitx::StandardPath::Type::PkgData,
            "eosphoros-native/eosphoros-native.dict");
    }
    if (path.empty()) {
        dictionaryError_ = "native dictionary was not found";
    } else {
        dictionary_.load(path, &dictionaryError_);
    }
}

State *EosphorosEngine::state(fcitx::InputContext *inputContext) {
    return inputContext->propertyFor(&stateFactory_);
}

void EosphorosEngine::apply(fcitx::InputContext *inputContext,
                            const KeyResult &result) {
    for (const auto &text : result.commits) {
        inputContext->commitString(text);
    }
    updateUI(inputContext);
}

void EosphorosEngine::keyEvent(const fcitx::InputMethodEntry &,
                               fcitx::KeyEvent &event) {
    if (event.isRelease()) {
        return;
    }
    auto *inputContext = event.inputContext();
    auto *current = state(inputContext);
    const auto result = keyHandler_.handle(current->context, logicalKey(event.key()));

    if (result.consumed) {
        apply(inputContext, result);
        event.filterAndAccept();
    }
}

void EosphorosEngine::selectCandidate(fcitx::InputContext *inputContext,
                                     std::size_t index) {
    apply(inputContext, state(inputContext)->context.select(index));
}

void EosphorosEngine::updateUI(fcitx::InputContext *inputContext) {
    const auto &context = state(inputContext)->context;
    inputContext->inputPanel().reset();
    if (!context.input().empty()) {
        fcitx::Text preedit(context.input());
        preedit.setCursor(context.input().size());
        inputContext->inputPanel().setPreedit(preedit);

        auto list = std::make_unique<fcitx::CommonCandidateList>();
        list->setPageSize(static_cast<int>(dictionary_.pageSize()));
        list->setLayoutHint(fcitx::CandidateLayoutHint::Vertical);
        list->setCursorPositionAfterPaging(
            fcitx::CursorPositionAfterPaging::ResetToFirst);
        fcitx::KeyList selectionKeys;
        for (std::size_t i = 0; i < dictionary_.pageSize(); ++i) {
            selectionKeys.emplace_back(std::to_string(i + 1));
        }
        list->setSelectionKey(selectionKeys);
        for (std::size_t i = 0; i < context.candidates().size(); ++i) {
            const auto &candidate = context.candidates()[i];
            list->append<CandidateWord>(this, i, candidate.text, candidate.code,
                                        candidate.completion);
        }
        if (!context.candidates().empty()) {
            list->setGlobalCursorIndex(static_cast<int>(context.selected()));
        }
        inputContext->inputPanel().setCandidateList(std::move(list));
    }
    inputContext->updatePreedit();
    inputContext->updateUserInterface(fcitx::UserInterfaceComponent::InputPanel);
}

void EosphorosEngine::reset(const fcitx::InputMethodEntry &,
                            fcitx::InputContextEvent &event) {
    state(event.inputContext())->context.reset();
    updateUI(event.inputContext());
}

std::string EosphorosEngine::subModeIconImpl(const fcitx::InputMethodEntry &,
                                             fcitx::InputContext &) {
    return "fcitx-eosphoros-native";
}

std::string EosphorosEngine::subModeLabelImpl(const fcitx::InputMethodEntry &,
                                              fcitx::InputContext &) {
    return "晨";
}

fcitx::AddonInstance *Factory::create(fcitx::AddonManager *manager) {
    return new EosphorosEngine(manager->instance());
}

} // namespace eosphoros::fcitx5
