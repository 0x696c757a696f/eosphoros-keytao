#pragma once

#include "context.h"
#include "dictionary.h"

#include <fcitx/addonfactory.h>
#include <fcitx/inputcontextproperty.h>
#include <fcitx/inputmethodengine.h>
#include <memory>
#include <string>

namespace fcitx {
class AddonManager;
class Instance;
} // namespace fcitx

namespace eosphoros::fcitx5 {

class State final : public fcitx::InputContextProperty {
public:
    State(fcitx::InputContext *inputContext, const Dictionary *dictionary)
        : inputContext(inputContext), context(dictionary) {}

    fcitx::InputContext *inputContext;
    Context context;
};

class Engine final : public fcitx::InputMethodEngineV2 {
public:
    explicit Engine(fcitx::Instance *instance);

    void keyEvent(const fcitx::InputMethodEntry &entry,
                  fcitx::KeyEvent &event) override;
    void reset(const fcitx::InputMethodEntry &entry,
               fcitx::InputContextEvent &event) override;
    std::string subModeIconImpl(const fcitx::InputMethodEntry &entry,
                                fcitx::InputContext &inputContext) override;
    std::string subModeLabelImpl(const fcitx::InputMethodEntry &entry,
                                 fcitx::InputContext &inputContext) override;

    void selectCandidate(fcitx::InputContext *inputContext, std::size_t index);

private:
    State *state(fcitx::InputContext *inputContext);
    void apply(fcitx::InputContext *inputContext, const KeyResult &result);
    void updateUI(fcitx::InputContext *inputContext);

    fcitx::Instance *instance_;
    Dictionary dictionary_;
    std::string dictionaryError_;
    fcitx::FactoryFor<State> stateFactory_;
};

class Factory final : public fcitx::AddonFactory {
public:
    fcitx::AddonInstance *create(fcitx::AddonManager *manager) override;
};

} // namespace eosphoros::fcitx5
