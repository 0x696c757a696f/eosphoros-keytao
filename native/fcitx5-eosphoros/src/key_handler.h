#pragma once

#include "context.h"

#include <cstddef>

namespace eosphoros {

enum class KeyKind {
    PassThrough,
    Code,
    Space,
    Enter,
    Backspace,
    Escape,
    Up,
    Down,
    PageUp,
    PageDown,
    Select,
    Symbol,
    Calculator,
    ToggleZzc,
    ZzcCommand,
    DeleteCustom,
};

struct LogicalKey {
    KeyKind kind = KeyKind::PassThrough;
    char code = '\0';
    std::size_t index = 0;
    std::string text;
};

class KeyHandler {
public:
    KeyResult handle(EosphorosContext &context, const LogicalKey &key) const;
};

} // namespace eosphoros
