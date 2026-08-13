#pragma once

#include "dictionary.h"

#include <ctime>
#include <string>
#include <vector>

namespace eosphoros {

bool isCalculatorInput(const std::string &input);
bool isCalculatorCharacter(char value);
std::vector<Candidate> specialCandidates(const std::string &input,
                                         std::time_t now = std::time(nullptr));

} // namespace eosphoros
