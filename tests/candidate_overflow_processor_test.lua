package.path = "./lua/?.lua;./lua/?/init.lua;" .. package.path

package.preload["eosphoros.input.eosphoros_key_event"] = function()
    return {
        effective_caps_on = function() return false end,
        digit_char = function(repr) return repr end,
    }
end

package.preload["eosphoros.input.eosphoros_commit_guard"] = function()
    return {
        commit_overflow_digit = function(ctx, _, digit)
            ctx.digit = digit
            return true
        end,
    }
end

local processor = require("eosphoros.eosphoros_candidate_overflow_processor").func
local ctx = {
    get_option = function() return false end,
}
local env = { engine = { context = ctx } }

local function key(repr, shift)
    return {
        keycode = 0,
        repr = function() return repr end,
        release = function() return false end,
        ctrl = function() return false end,
        alt = function() return false end,
        super = function() return false end,
        shift = function() return shift end,
    }
end

assert(processor(key("6", false), env) == 1)
assert(ctx.digit == "6")
assert(processor(key("6", true), env) == 2)

print("candidate_overflow_processor_test: PASS")
