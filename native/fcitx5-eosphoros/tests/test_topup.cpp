#include "test_support.h"
#include "topup.h"

#include <cstdlib>
#include <iostream>

int main() {
    try {
        eosphoros::TopupPolicy topup;
        require(topup.process("abcd", 'x', {true, true, 0}).action ==
                    eosphoros::TopupAction::CommitAndStartNext,
                "four-code fixed topup failed");
        require(topup.process("abc", 'x', {true, true, 0}).action ==
                    eosphoros::TopupAction::Continue,
                "short code must not top up");
        require(topup.process("abca", 'i', {true, true, 0}).action ==
                    eosphoros::TopupAction::Continue,
                "two topup keys must continue");
        require(topup.process("abca", 'x', {true, true, 0}).action ==
                    eosphoros::TopupAction::CommitAndStartNext,
                "topup-to-non-topup transition failed");
        require(topup.process("aaiv", 'x', {true, true, 0}).action ==
                    eosphoros::TopupAction::CommitAndStartNext,
                "real auxiliary-code topup failed");
        require(topup.process("ba", 'x', {true, true, 0}).action ==
                    eosphoros::TopupAction::CommitAndStartNext,
                "real topup-key transition failed");
        require(topup.process("zzzz", 'x', {}).action ==
                    eosphoros::TopupAction::ClearAndStartNext,
                "empty topup must clear and start the next code");

        eosphoros::TopupConfig noClear;
        noClear.autoClear = false;
        eosphoros::TopupPolicy hold(noClear);
        require(hold.process("zzzz", 'x', {}).action ==
                    eosphoros::TopupAction::HoldAndConsume,
                "disabled auto_clear must preserve input and consume the key");
        std::cout << "topup tests passed\n";
        return EXIT_SUCCESS;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
