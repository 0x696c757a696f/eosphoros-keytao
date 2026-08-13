#include "auxiliary.h"
#include "context.h"
#include "dictionary.h"

#include <algorithm>
#include <cassert>
#include <iostream>

int main(int argc, char **argv) {
    assert(argc == 3);
    eosphoros::AuxiliaryData data;
    std::string error;
    assert(data.load(argv[1], &error));
    const auto *pronunciation = data.pronunciation("你");
    assert(pronunciation && !pronunciation->empty());
    const auto *emoji = data.emoji("你");
    assert(emoji && !emoji->empty());
    assert(std::find(emoji->begin(), emoji->end(), "🫵") != emoji->end());
    eosphoros::Dictionary dictionary;
    assert(dictionary.load(argv[2], &error));
    eosphoros::EosphorosContext context(&dictionary, &data);
    context.type('u'); context.type('n'); context.type('i');
    assert(!context.candidates().empty());
    assert(!context.candidates().front().comment.empty());
    std::cout << "native auxiliary lookup verified\n";
    return 0;
}
