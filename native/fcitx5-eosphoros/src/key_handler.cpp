#include "key_handler.h"

namespace eosphoros {

KeyResult KeyHandler::handle(EosphorosContext &context,
                             const LogicalKey &key) const {
    switch (key.kind) {
    case KeyKind::Code:
        return context.type(key.code);
    case KeyKind::Space:
        return context.space();
    case KeyKind::Enter:
        return context.enter();
    case KeyKind::Backspace:
        return context.backspace();
    case KeyKind::Escape:
        return context.escape();
    case KeyKind::Up:
        return {context.moveSelection(-1), {}};
    case KeyKind::Down:
        return {context.moveSelection(1), {}};
    case KeyKind::PageUp:
        return {context.moveSelection(-static_cast<int>(context.pageSize())), {}};
    case KeyKind::PageDown:
        return {context.moveSelection(static_cast<int>(context.pageSize())), {}};
    case KeyKind::Select: {
        const auto pageStart =
            (context.selected() / context.pageSize()) * context.pageSize();
        return context.select(pageStart + key.index);
    }
    case KeyKind::Symbol:
        return context.symbol(key.text);
    case KeyKind::PassThrough:
        break;
    }
    return {};
}

} // namespace eosphoros
