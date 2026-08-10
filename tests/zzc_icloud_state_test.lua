package.path = "./lua/?.lua;./lua/?/init.lua;" .. package.path

local data_dir = assert(os.getenv("ZZC_TEST_DATA_DIR"), "missing ZZZC test data directory")
_G.rime_api = {
    get_user_data_dir = function() return data_dir end,
}

local core = require("eosphoros.zzc.eosphoros_zzc_core")

local function read_all(path)
    local file = assert(io.open(path, "rb"))
    local content = file:read("*a")
    file:close()
    return content:gsub("\r\n", "\n")
end

local items = {
    { text = "甲", parts = { s = "a", y = "b", p = "a", code = "aba" } },
    { text = "乙", parts = { s = "c", y = "d", p = "i", code = "cdi" } },
}

assert(core.undo_all_pending())
assert(core.save_word_at_code(
    items,
    "abcd",
    nil,
    function() return nil end,
    function() return {} end
))
local flush_ok, flush_changed = core.flush_runtime_ops()
assert(flush_ok and flush_changed, "flush must clear a non-empty runtime batch")

for _, name in ipairs({ "runtime_ops.tsv", "runtime_exact.tsv" }) do
    local content = read_all(data_dir .. "/zzc_state/" .. name)
    assert(content == "\n", name .. " must use one newline for a logical empty state")
end
assert(core.undo_all_pending())
local effective = read_all(data_dir .. "/zzc_state/effective_state.tsv")
assert(effective == "\n", "effective_state.tsv must use one newline for a logical empty state")

print("zzc_icloud_state_test: PASS")
