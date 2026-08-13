#include "context.h"
#include "dictionary.h"
#include "topup.h"

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

void require(bool value, const std::string &message) {
    if (!value) {
        throw std::runtime_error(message);
    }
}

std::vector<std::string> split(const std::string &text, char delimiter) {
    std::vector<std::string> result;
    std::istringstream stream(text);
    std::string item;
    while (std::getline(stream, item, delimiter)) {
        result.push_back(item);
    }
    if (!text.empty() && text.back() == delimiter) {
        result.emplace_back();
    }
    return result;
}

void append(std::vector<std::string> &target,
            const std::vector<std::string> &values) {
    target.insert(target.end(), values.begin(), values.end());
}

void runTrace(const eosphoros::Dictionary &dictionary, const std::string &name,
              const std::string &keys, const std::string &expectedCommits,
              const std::string &expectedInput) {
    eosphoros::Context context(&dictionary);
    std::vector<std::string> commits;
    for (const auto &key : split(keys, ' ')) {
        eosphoros::KeyResult result;
        if (key == "SPACE") {
            result = context.space();
        } else if (key == "ENTER") {
            result = context.enter();
        } else if (key == "BACKSPACE") {
            result = context.backspace();
        } else if (key == "ESCAPE") {
            result = context.escape();
        } else if (key.size() == 1 && key[0] >= '1' && key[0] <= '9') {
            result = context.select(static_cast<std::size_t>(key[0] - '1'));
        } else {
            require(key.size() == 1, name + ": invalid golden key");
            result = context.type(key[0]);
        }
        append(commits, result.commits);
    }
    const auto expected = expectedCommits == "-"
                              ? std::vector<std::string>{}
                              : split(expectedCommits, '|');
    require(commits == expected, name + ": commits differ");
    require(context.input() == (expectedInput == "-" ? "" : expectedInput),
            name + ": final input differs");
}

} // namespace

int main(int argc, char **argv) {
    try {
        require(argc == 3, "usage: test_core DICTIONARY GOLDEN_TSV");
        eosphoros::Dictionary dictionary;
        std::string error;
        require(dictionary.load(argv[1], &error), error);
        require(dictionary.size() == 8, "unexpected fixture size");

        const auto exact = dictionary.lookup("kb");
        require(exact.size() >= 2 && exact[0].text == "阿" &&
                    exact[1].text == "安" && !exact[0].completion,
                "source-order exact lookup failed");
        require(dictionary.hasPrefix("jxjd"), "prefix lookup failed");

        eosphoros::TopupPolicy topup;
        require(topup.decide("abcd", 'x', true) ==
                    eosphoros::TopupAction::CommitAndStartNext,
                "four-code fixed topup failed");
        require(topup.decide("abc", 'x', true) ==
                    eosphoros::TopupAction::Continue,
                "short code must not top up");
        require(topup.decide("abca", 'i', true) ==
                    eosphoros::TopupAction::Continue,
                "two topup keys must continue");

        std::ifstream golden(argv[2]);
        require(golden.good(), "cannot open golden traces");
        std::string line;
        while (std::getline(golden, line)) {
            if (line.empty() || line[0] == '#') {
                continue;
            }
            const auto fields = split(line, '\t');
            require(fields.size() == 4, "invalid golden trace row");
            runTrace(dictionary, fields[0], fields[1], fields[2], fields[3]);
        }

        // State must be per input context, not shared by the engine.
        eosphoros::Context first(&dictionary);
        eosphoros::Context second(&dictionary);
        first.type('a');
        second.type('j');
        require(first.input() == "a" && second.input() == "j",
                "input contexts leaked state");
        std::cout << "native core tests passed\n";
        return EXIT_SUCCESS;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
