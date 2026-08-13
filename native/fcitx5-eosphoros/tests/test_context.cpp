#include "context.h"
#include "dictionary.h"
#include "key_handler.h"
#include "test_support.h"

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

namespace {

void append(std::vector<std::string> &target,
            const std::vector<std::string> &values) {
    target.insert(target.end(), values.begin(), values.end());
}

void runTrace(const eosphoros::Dictionary &dictionary,
              const std::vector<std::string> &fields) {
    const auto &name = fields[0];
    const auto &evidence = fields[1];
    require(!evidence.empty(), name + ": golden trace has no source evidence");
    eosphoros::EosphorosContext context(&dictionary);
    eosphoros::KeyHandler handler;
    std::vector<std::string> commits;
    for (const auto &key : split(fields[2], ' ')) {
        eosphoros::LogicalKey logical;
        if (key == "SPACE") {
            logical.kind = eosphoros::KeyKind::Space;
        } else if (key == "ENTER") {
            logical.kind = eosphoros::KeyKind::Enter;
        } else if (key == "BACKSPACE") {
            logical.kind = eosphoros::KeyKind::Backspace;
        } else if (key == "ESCAPE") {
            logical.kind = eosphoros::KeyKind::Escape;
        } else if (key == "UP") {
            logical.kind = eosphoros::KeyKind::Up;
        } else if (key == "DOWN") {
            logical.kind = eosphoros::KeyKind::Down;
        } else if (key == "PAGE_UP") {
            logical.kind = eosphoros::KeyKind::PageUp;
        } else if (key == "PAGE_DOWN") {
            logical.kind = eosphoros::KeyKind::PageDown;
        } else if (key.size() == 1 && key[0] >= '1' && key[0] <= '9') {
            logical.kind = eosphoros::KeyKind::Select;
            logical.index = static_cast<std::size_t>(key[0] - '1');
        } else {
            require(key.size() == 1, name + ": invalid golden key");
            logical.kind = eosphoros::KeyKind::Code;
            logical.code = key[0];
        }
        append(commits, handler.handle(context, logical).commits);
    }
    const auto expectedCommits = fields[3] == "-"
                                     ? std::vector<std::string>{}
                                     : split(fields[3], '|');
    require(commits == expectedCommits, name + ": commits differ");
    require(context.input() == (fields[4] == "-" ? "" : fields[4]),
            name + ": final preedit differs");
    const auto actualFirst = context.candidates().empty()
                                 ? std::string{}
                                 : context.candidates().front().text;
    require(actualFirst == (fields[5] == "-" ? "" : fields[5]),
            name + ": first candidate differs");
}

} // namespace

int main(int argc, char **argv) {
    try {
        require(argc == 3, "usage: test_context DICTIONARY GOLDEN_TSV");
        eosphoros::Dictionary dictionary;
        std::string error;
        require(dictionary.load(argv[1], &error), error);
        std::ifstream golden(argv[2]);
        require(golden.good(), "cannot open golden traces");
        std::string line;
        while (std::getline(golden, line)) {
            if (line.empty() || line[0] == '#') {
                continue;
            }
            const auto fields = split(line, '\t');
            require(fields.size() == 6, "invalid golden trace row");
            runTrace(dictionary, fields);
        }

        eosphoros::EosphorosContext first(&dictionary);
        eosphoros::EosphorosContext second(&dictionary);
        first.type('a');
        second.type('j');
        require(first.input() == "a" && second.input() == "j",
                "input contexts leaked state");
        std::cout << "context golden tests passed\n";
        return EXIT_SUCCESS;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
