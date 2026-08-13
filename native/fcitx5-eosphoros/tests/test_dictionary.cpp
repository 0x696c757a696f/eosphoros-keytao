#include "dictionary.h"
#include "test_support.h"

#include <cstdlib>
#include <iostream>

int main(int argc, char **argv) {
    try {
        require(argc == 2, "usage: test_dictionary DICTIONARY");
        eosphoros::Dictionary dictionary;
        std::string error;
        require(dictionary.load(argv[1], &error), error);
        require(dictionary.size() == 24, "unexpected fixture size");
        require(dictionary.pageSize() == 5, "schema page size was not loaded");
        const auto &config = dictionary.topupConfig();
        require(config.topupThis == "bcdefghjklmnpqrstwxyz",
                "topup_this was not loaded");
        require(config.topupKeys == "avuio;", "topup_with was not loaded");
        require(config.minLength == 4 && config.maxLength == 6,
                "topup lengths were not loaded");
        require(config.autoClear && !config.topupCommand,
                "topup flags were not loaded");

        const auto exact = dictionary.lookup("kb");
        require(exact.size() >= 2 && exact[0].text == "阿" &&
                    exact[1].text == "安" && !exact[0].completion,
                "source-order exact lookup failed");
        const auto collision = dictionary.lookup("hyefa");
        require(collision.size() == 2 && collision[0].text == "洪山" &&
                    collision[1].text == "婚姻圣召",
                "real dictionary collision order changed");
        require(dictionary.hasPrefix("jxjd"), "prefix lookup failed");
        std::cout << "dictionary tests passed\n";
        return EXIT_SUCCESS;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
