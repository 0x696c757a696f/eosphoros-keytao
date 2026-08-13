#include "context.h"
#include "dictionary.h"
#include "user_data.h"

#include <cassert>
#include <filesystem>
#include <iostream>

int main(int argc, char **argv) {
    assert(argc == 3);
    const std::filesystem::path path(argv[2]);
    std::filesystem::remove(path);
    eosphoros::Dictionary dictionary;
    std::string error;
    assert(dictionary.load(argv[1], &error));
    eosphoros::UserData first(path.string());
    assert(first.load(&error));
    assert(first.record("zz", "晨星测试", true, &error));
    assert(first.record("zz", "晨星测试", true, &error));
    assert(first.record("aa", "另一自造词", true, &error));
    eosphoros::EosphorosContext undoContext(&dictionary, nullptr, &first);
    assert(undoContext.toggleZzc().consumed);
    assert(undoContext.zzcCommand('-').consumed);
    assert(undoContext.zzcCommand('-').consumed);
    assert(undoContext.toggleZzc().consumed);
    assert(first.candidates("aa").empty());

    eosphoros::UserData second(path.string());
    assert(second.load(&error));
    assert(second.frequency("zz", "晨星测试") == 2);
    const auto custom = second.candidates("zz");
    assert(custom.size() == 1 && custom.front().text == "晨星测试");

    eosphoros::EosphorosContext context(&dictionary, nullptr, &second);
    context.type('z'); context.type('z');
    assert(!context.candidates().empty());
    assert(context.candidates().front().text == "晨星测试");
    context.space();
    assert(second.frequency("zz", "晨星测试") == 3);
    eosphoros::EosphorosContext deleteContext(&dictionary, nullptr, &second);
    deleteContext.type('z'); deleteContext.type('z');
    assert(deleteContext.deleteSelectedCustom().consumed);
    assert(second.candidates("zz").empty());
    assert(second.record("zz", "晨星测试", true, &error));
    eosphoros::EosphorosContext clearContext(&dictionary, nullptr, &second);
    assert(clearContext.toggleZzc().consumed);
    assert(clearContext.zzcCommand('!').consumed);
    assert(clearContext.zzcCommand('!').consumed);
    assert(clearContext.zzcCommand('!').consumed);
    assert(clearContext.toggleZzc().consumed);
    assert(second.candidates("zz").empty());
    std::filesystem::remove(path);
    std::cout << "native user data persistence verified\n";
    return 0;
}
