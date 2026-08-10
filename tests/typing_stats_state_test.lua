package.path = "./lua/?.lua;./lua/?/init.lua;" .. package.path

local data_dir = assert(os.getenv("TYPING_STATS_TEST_DATA_DIR"), "missing typing stats test directory")
local legacy_path = data_dir .. "/typing_stats.txt"
local current_path = data_dir .. "/zzc_state/eosphoros_typing_stats.tsv"
local today = os.date("%Y-%m-%d")

local legacy = assert(io.open(legacy_path, "w"))
legacy:write(today, "\t2\t4\t1\t0\t0\t30\t2\n")
legacy:close()

_G.rime_api = { get_user_data_dir = function() return data_dir end }
_G.__typing_stats = nil

local notify
local context = {
    get_option = function(_, name) return name == "ascii_mode" and false end,
    commit_notifier = {
        connect = function(_, callback)
            notify = callback
            return { disconnect = function() end }
        end,
    },
}
local env = {
    engine = {
        context = context,
        schema = { schema_id = "eosphoros" },
    },
}
local key = {
    keycode = string.byte("a"),
    release = function() return false end,
    ctrl = function() return false end,
    alt = function() return false end,
    super = function() return false end,
}

local stats = require("eosphoros.typing_stats")
stats.init_processor(env)
assert(stats.processor(key, env) == 2)
assert(type(notify) == "function")
notify({ get_commit_text = function() return "天地" end })
stats.fini_processor(env)

local current = assert(io.open(current_path, "r"), "namespaced stats file was not created")
local content = current:read("*a")
current:close()
assert(content:find(today .. "\t4\t5\t2", 1, true), "legacy counters were not migrated")
assert(io.open(legacy_path, "r"), "legacy stats file should remain as a safe backup")

print("typing_stats_state_test: PASS")
