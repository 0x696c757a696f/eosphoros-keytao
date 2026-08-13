#include "dictionary.h"
#include "test_support.h"

#include <cstdlib>
#include <iostream>

int main(int argc, char **argv) {
    try {
        require(argc == 2, "usage: test_production_dictionary DICTIONARY");
        eosphoros::Dictionary dictionary;
        std::string error;
        require(dictionary.load(argv[1], &error), error);
        require(dictionary.size() > 1000000,
                "production dictionary is unexpectedly incomplete");
        require(dictionary.lookup("jxjdoo").front().text == "晨星键道",
                "main namespace lookup failed");
        require(dictionary.lookup("ihello", eosphoros::Mode::English).front().text == "hello",
                "English namespace lookup failed");
        require(dictionary.lookup("uni", eosphoros::Mode::ReversePinyin).front().text == "你",
                "Pinyin namespace lookup failed");
        const auto liangfen = dictionary.lookup("vlyly", eosphoros::Mode::ReverseLiangfen);
        require(liangfen.size() >= 2 && liangfen[0].text == "龖" &&
                    liangfen[1].text == "龘",
                "Liangfen namespace lookup failed");
        require(dictionary.lookup("odsovouviavvvavavvvovouviavvvavavvvovouviavvvavavvv", eosphoros::Mode::ReverseGBK)
                    .front().text == "龘",
                "GBK namespace lookup failed");
        std::cout << "production dictionary smoke tests passed\n";
        return EXIT_SUCCESS;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
