#include "special.h"
#include "test_support.h"

#include <cstdlib>
#include <ctime>
#include <iostream>

int main() {
    try {
        const auto arithmetic = eosphoros::specialCandidates("=2+3*4");
        require(arithmetic.size() == 2 && arithmetic[0].text == "14" &&
                    arithmetic[1].text == "2+3*4=14",
                "calculator precedence failed");
        require(eosphoros::specialCandidates("=1/0").empty(),
                "calculator accepted division by zero");
        require(eosphoros::specialCandidates("=system(1)").empty(),
                "calculator accepted non-arithmetic input");

        std::tm fixed{};
        fixed.tm_year = 126;
        fixed.tm_mon = 0;
        fixed.tm_mday = 4;
        fixed.tm_hour = 5;
        fixed.tm_min = 6;
        fixed.tm_sec = 7;
        fixed.tm_isdst = -1;
        const auto timestamp = std::mktime(&fixed);
        const auto date = eosphoros::specialCandidates("rq", timestamp);
        require(date.size() == 3 && date[0].text == "2026-01-04" &&
                    date[1].text == "2026年1月4日" &&
                    date[2].text == "20260104",
                "date formats or non-padded Chinese date changed");
        const auto clock = eosphoros::specialCandidates("jkdm", timestamp);
        require(clock.size() == 1 && clock[0].text == "05:06:07",
                "time format failed");
        std::cout << "special candidate tests passed\n";
        return EXIT_SUCCESS;
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
