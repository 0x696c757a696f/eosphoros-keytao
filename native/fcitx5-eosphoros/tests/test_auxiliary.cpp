#include "auxiliary.h"
#include "context.h"
#include "dictionary.h"
#include "user_data.h"

#include <algorithm>
#include <cassert>
#include <iostream>
#include <filesystem>

int main(int argc, char **argv) {
    assert(argc == 4);
    eosphoros::AuxiliaryData data;
    std::string error;
    assert(data.load(argv[1], &error));
    const auto *pronunciation = data.pronunciation("你");
    assert(pronunciation && !pronunciation->empty());
    const auto *emoji = data.emoji("你");
    assert(emoji && !emoji->empty());
    assert(std::find(emoji->begin(), emoji->end(), "🫵") != emoji->end());
    const auto *parts = data.characterParts("你");
    assert(parts && !parts->sound.empty() && !parts->rhyme.empty() &&
           !parts->stroke.empty());
    eosphoros::Dictionary dictionary;
    assert(dictionary.load(argv[2], &error));
    eosphoros::EosphorosContext context(&dictionary, &data);
    context.type('u'); context.type('n'); context.type('i');
    assert(!context.candidates().empty());
    assert(!context.candidates().front().comment.empty());
    const std::filesystem::path userPath(argv[3]);
    std::filesystem::remove(userPath);
    eosphoros::UserData userData(userPath.string());
    assert(userData.load(&error));
    eosphoros::EosphorosContext zzc(&dictionary, &data, &userData);
    assert(zzc.toggleZzc().consumed);
    for (const char key : std::string("jno")) zzc.type(key);
    assert(!zzc.candidates().empty() && zzc.candidates().front().text == "晨");
    assert(zzc.space().commits.empty());
    for (const char key : std::string("xgoi")) zzc.type(key);
    assert(!zzc.candidates().empty() && zzc.candidates().front().text == "星");
    assert(zzc.space().commits.empty());
    const auto finished = zzc.toggleZzc();
    assert(finished.commits.size() == 1 && finished.commits.front() == "晨星");
    const auto custom = userData.candidates("jnxgoo");
    assert(custom.size() == 1 && custom.front().text == "晨星");
    std::filesystem::remove(userPath);
    std::cout << "native auxiliary lookup verified\n";
    return 0;
}
