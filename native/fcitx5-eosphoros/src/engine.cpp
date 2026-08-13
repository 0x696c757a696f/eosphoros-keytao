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

constexpr std::size_t kPageSize = 5;

char codeKey(const fcitx::Key &key) {
    if (key.hasModifier()) {
        return '\0';
    }
    const auto symbol = key.sym();
    if (symbol >= FcitxKey_a && symbol <= FcitxKey_z) {
        return static_cast<char>('a' + symbol - FcitxKey_a);
    }
    if (symbol == FcitxKey_semicolon) {
        return ';';
    }
    if (symbol == FcitxKey_apostrophe) {
        return '\'';
    }
    return '\0';
}

} // namespace

Engine::Engine(fcitx::Instance *instance)
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

State *Engine::state(fcitx::InputContext *inputContext) {
    return inputContext->propertyFor(&stateFactory_);
}

void Engine::apply(fcitx::InputContext *inputContext, const KeyResult &result) {
    for (const auto &text : result.commits) {
        inputContext->commitString(text);
    }
    updateUI(inputContext);
}

void Engine::keyEvent(const fcitx::InputMethodEntry &, fcitx::KeyEvent &event) {
    if (event.isRelease()) {
        return;
    }
    auto *inputContext = event.inputContext();
    auto *current = state(inputContext);
    KeyResult result;

    if (const char key = codeKey(event.key())) {
        result = current->context.type(key);
    } else if (!event.key().hasModifier()) {
        switch (event.key().sym()) {
        case FcitxKey_space:
            result = current->context.space();
            break;
        case FcitxKey_Return:
        case FcitxKey_KP_Enter:
            result = current->context.enter();
            break;
        case FcitxKey_BackSpace:
            result = current->context.backspace();
            break;
        case FcitxKey_Escape:
            result = current->context.escape();
            break;
        case FcitxKey_Up:
            result.consumed = current->context.moveSelection(-1);
            break;
        case FcitxKey_Down:
            result.consumed = current->context.moveSelection(1);
            break;
        case FcitxKey_Page_Up:
            result.consumed =
                current->context.moveSelection(-static_cast<int>(kPageSize));
            break;
        case FcitxKey_Page_Down:
            result.consumed =
                current->context.moveSelection(static_cast<int>(kPageSize));
            break;
        default:
            if (event.key().sym() >= FcitxKey_1 &&
                event.key().sym() <= FcitxKey_9) {
                const auto pageStart =
                    (current->context.selected() / kPageSize) * kPageSize;
                const auto index = pageStart + static_cast<std::size_t>(
                                                   event.key().sym() -
                                                   FcitxKey_1);
                result = current->context.select(index);
            }
            break;
        }
    }

    if (result.consumed) {
        apply(inputContext, result);
        event.filterAndAccept();
    }
}

void Engine::selectCandidate(fcitx::InputContext *inputContext,
                             std::size_t index) {
    apply(inputContext, state(inputContext)->context.select(index));
}

void Engine::updateUI(fcitx::InputContext *inputContext) {
    const auto &context = state(inputContext)->context;
    inputContext->inputPanel().reset();
    if (!context.input().empty()) {
        fcitx::Text preedit(context.input());
        preedit.setCursor(context.input().size());
        inputContext->inputPanel().setPreedit(preedit);

        auto list = std::make_unique<fcitx::CommonCandidateList>();
        list->setPageSize(kPageSize);
        list->setLayoutHint(fcitx::CandidateLayoutHint::Vertical);
        list->setCursorPositionAfterPaging(
            fcitx::CursorPositionAfterPaging::ResetToFirst);
        list->setSelectionKey({fcitx::Key("1"), fcitx::Key("2"),
                               fcitx::Key("3"), fcitx::Key("4"),
                               fcitx::Key("5")});
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

void Engine::reset(const fcitx::InputMethodEntry &,
                   fcitx::InputContextEvent &event) {
    state(event.inputContext())->context.reset();
    updateUI(event.inputContext());
}

std::string Engine::subModeIconImpl(const fcitx::InputMethodEntry &,
                                    fcitx::InputContext &) {
    return "fcitx-eosphoros-native";
}

std::string Engine::subModeLabelImpl(const fcitx::InputMethodEntry &,
                                     fcitx::InputContext &) {
    return "晨";
}

fcitx::AddonInstance *Factory::create(fcitx::AddonManager *manager) {
    return new Engine(manager->instance());
}

} // namespace eosphoros::fcitx5
