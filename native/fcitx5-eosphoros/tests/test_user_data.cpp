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
    std::filesystem::remove(path);
    std::cout << "native user data persistence verified\n";
    return 0;
}
