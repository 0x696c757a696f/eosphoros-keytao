#include "special.h"

#include <cmath>
#include <cstdio>
#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>

namespace eosphoros {
namespace {

class Calculator {
public:
    explicit Calculator(const std::string &source) : source_(source) {}

    double parse() {
        const auto value = expression();
        skipSpaces();
        if (position_ != source_.size() || !std::isfinite(value)) {
            throw std::runtime_error("invalid expression");
        }
        return value;
    }

private:
    void skipSpaces() {
        while (position_ < source_.size() && source_[position_] == ' ') {
            ++position_;
        }
    }

    bool take(char value) {
        skipSpaces();
        if (position_ < source_.size() && source_[position_] == value) {
            ++position_;
            return true;
        }
        return false;
    }

    double expression() {
        auto value = term();
        while (true) {
            if (take('+')) value += term();
            else if (take('-')) value -= term();
            else return value;
        }
    }

    double term() {
        auto value = power();
        while (true) {
            if (take('*')) value *= power();
            else if (take('/')) {
                const auto divisor = power();
                if (divisor == 0) throw std::runtime_error("division by zero");
                value /= divisor;
            } else if (take('%')) {
                const auto divisor = power();
                if (divisor == 0) throw std::runtime_error("division by zero");
                value = std::fmod(value, divisor);
            } else return value;
        }
    }

    double power() {
        auto value = unary();
        if (take('^')) value = std::pow(value, power());
        return value;
    }

    double unary() {
        if (take('+')) return unary();
        if (take('-')) return -unary();
        return primary();
    }

    double primary() {
        if (take('(')) {
            const auto value = expression();
            if (!take(')')) throw std::runtime_error("missing parenthesis");
            return value;
        }
        skipSpaces();
        const auto start = position_;
        bool dot = false;
        while (position_ < source_.size()) {
            const auto value = source_[position_];
            if (value >= '0' && value <= '9') ++position_;
            else if (value == '.' && !dot) { dot = true; ++position_; }
            else break;
        }
        if (start == position_) throw std::runtime_error("number expected");
        return std::stod(source_.substr(start, position_ - start));
    }

    const std::string &source_;
    std::size_t position_ = 0;
};

std::tm localTime(std::time_t now) {
    std::tm result{};
#ifdef _WIN32
    localtime_s(&result, &now);
#else
    localtime_r(&now, &result);
#endif
    return result;
}

std::string format(const std::tm &time, const char *pattern) {
    std::ostringstream out;
    out << std::put_time(&time, pattern);
    return out.str();
}

std::string number(double value) {
    if (std::abs(value - std::round(value)) < 1e-12 &&
        std::abs(value) <= static_cast<double>(std::numeric_limits<long long>::max())) {
        return std::to_string(static_cast<long long>(std::llround(value)));
    }
    std::ostringstream out;
    out << std::setprecision(15) << value;
    return out.str();
}

} // namespace

bool isCalculatorInput(const std::string &input) {
    return !input.empty() && input.front() == '=';
}

bool isCalculatorCharacter(char value) {
    return (value >= '0' && value <= '9') || value == '.' || value == '+' ||
           value == '-' || value == '*' || value == '/' || value == '%' ||
           value == '^' || value == '(' || value == ')' || value == ' ';
}

std::vector<Candidate> specialCandidates(const std::string &input,
                                         std::time_t now) {
    if (isCalculatorInput(input)) {
        if (input.size() == 1) return {};
        try {
            const auto value = number(Calculator(input.substr(1)).parse());
            return {{value, input, false, "答案"},
                    {input.substr(1) + "=" + value, input, false, "等式"}};
        } catch (const std::exception &) {
            return {};
        }
    }

    const auto time = localTime(now);
    if (input == "rq") {
        const auto iso = format(time, "%Y-%m-%d");
        const auto compact = format(time, "%Y%m%d");
        const auto chinese = std::to_string(time.tm_year + 1900) + "年" +
                             std::to_string(time.tm_mon + 1) + "月" +
                             std::to_string(time.tm_mday) + "日";
        return {{iso, input, false, "日期"},
                {chinese, input, false, "日期"},
                {compact, input, false, "日期"}};
    }
    if (input == "eo") {
        const auto clock = format(time, "%H:%M:%S");
        return {{format(time, "%Y-%m-%d") + " " + clock, input, false, "日期时间"},
                {clock, input, false, "时间"}};
    }
    if (input == "jkdm") {
        return {{format(time, "%H:%M:%S"), input, false, "时间"}};
    }
    if (input == "xq" || input == "xgqk") {
        static const char *weekdays[] = {"星期日", "星期一", "星期二", "星期三",
                                         "星期四", "星期五", "星期六"};
        static const char *shortWeekdays[] = {"周日", "周一", "周二", "周三",
                                              "周四", "周五", "周六"};
        return {{weekdays[time.tm_wday], input, false, "星期"},
                {shortWeekdays[time.tm_wday], input, false, "星期"}};
    }
    return {};
}

} // namespace eosphoros
