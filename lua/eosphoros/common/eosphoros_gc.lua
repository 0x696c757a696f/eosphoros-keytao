local M = {}

local MIN_EXPLICIT_STEP = 96
local pending_budget = 0
local run_count = 0

function M.step(budget, force)
    budget = tonumber(budget) or 0
    if budget > 0 then
        pending_budget = pending_budget + budget
    end
    if pending_budget <= 0 or (not force and pending_budget < MIN_EXPLICIT_STEP) then
        return false
    end
    collectgarbage("step", pending_budget)
    pending_budget = 0
    run_count = run_count + 1
    return true
end

function M.stats()
    return pending_budget, run_count
end

function M.reset()
    pending_budget = 0
    run_count = 0
end

return M
