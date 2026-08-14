package.path = table.concat({
    "./lua/?.lua",
    "./lua/?/init.lua",
    package.path,
}, ";")

local tests = {}

local function test(name, fn)
    tests[#tests + 1] = { name = name, fn = fn }
end

local function assert_equal(actual, expected, message)
    if actual ~= expected then
        error((message or "values differ")
            .. ": expected " .. tostring(expected)
            .. ", got " .. tostring(actual), 2)
    end
end

local function unload(prefix)
    for name in pairs(package.loaded) do
        if name:sub(1, #prefix) == prefix then
            package.loaded[name] = nil
        end
    end
end

local function candidate(candidate_type, start_pos, end_pos, text, comment)
    return {
        type = candidate_type,
        start = start_pos,
        _end = end_pos,
        text = text,
        comment = comment or "",
    }
end

local function base_env(options)
    options = options or {}
    local properties = {}
    local context = {
        input = options.input or "",
        get_option = function(_, name)
            if name == "jisuanqi" then return true end
            if name == "completion" then return options.completion == true end
            return false
        end,
        get_property = function(_, name)
            return properties[name] or ""
        end,
        set_property = function(_, name, value)
            properties[name] = value
        end,
    }
    local config = {
        get_bool = function(_, path)
            if path == "translator/enable_sentence" then return false end
            return nil
        end,
        get_int = function() return nil end,
        get_string = function() return nil end,
        get_list = function() return nil end,
    }
    return {
        engine = {
            context = context,
            schema = {
                schema_id = "eosphoros",
                config = config,
            },
        },
    }
end

test("lazy translator leaves English i input to the main table", function()
    unload("eosphoros")
    _G.Candidate = candidate
    local yielded = {}
    _G.yield = function(cand) yielded[#yielded + 1] = cand end

    local translator = require("eosphoros.eosphoros_core")
    local env = base_env()
    local seg = { start = 0, _end = 4 }

    translator.func("=1+1", seg, env)
    assert_equal(tostring(yielded[2] and yielded[2].text), "2", "calculator result")

    yielded = {}
    translator.func("rq", seg, env)
    if #yielded == 0 then error("time translator yielded no candidates") end

    yielded = {}
    translator.func("i", seg, env)
    assert_equal(#yielded, 0, "English prefix must not yield history candidates")

    unload("eosphoros")
    local saved_debug = debug
    _G.debug = nil
    local ok, err = pcall(function()
        local fallback = require("eosphoros.eosphoros_core")
        local fallback_env = base_env()
        fallback_env.engine.schema.schema_id = "custom_schema"
        fallback.func("rq", seg, fallback_env)
    end)
    _G.debug = saved_debug
    if not ok then error("loader fallback failed: " .. tostring(err)) end
end)

test("Chinese Gregorian dates do not pad month or day", function()
    unload("eosphoros")
    _G.Candidate = candidate
    local yielded = {}
    _G.yield = function(cand) yielded[#yielded + 1] = cand end

    local translator = require("eosphoros.eosphoros_time_core")
    translator.func("=20260104", { start = 0, _end = 9 }, base_env())

    assert_equal(yielded[1] and yielded[1].text, "2026年1月4日", "official Chinese date")
end)

test("ZZC candidates stay ahead of ordinary multi-character candidates", function()
    unload("eosphoros.eosphoros_completion")
    package.loaded["eosphoros.zzc.eosphoros_zzc_core"] = {
        zzc_cover_for_input = function() return nil end,
        zzc_completion_rows_for_prefix = function() return nil end,
    }
    _G.Candidate = candidate

    local yielded = {}
    _G.yield = function(cand) yielded[#yielded + 1] = cand end
    local completion = require("eosphoros.eosphoros_completion")
    local env = base_env({ input = "adfytoceek" })
    completion.init(env)

    local candidates = {
        candidate("phrase", 0, 10, "普通多字词", "词组"),
        candidate("zzc_code_choice", 0, 10, "☯造词组合", "编码"),
    }
    local input = {
        iter = function()
            local index = 0
            return function()
                index = index + 1
                return candidates[index]
            end
        end,
    }

    completion.func(input, env)
    assert_equal(yielded[1] and yielded[1].type, "zzc_code_choice", "first candidate type")
    assert_equal(yielded[2] and yielded[2].type, "phrase", "second candidate type")
    completion.fini(env)
end)

test("ZZC state preserves an empty replacement buffer placeholder", function()
    unload("eosphoros.zzc.eosphoros_zzc_state")
    local state_module = require("eosphoros.zzc.eosphoros_zzc_state")
    local state = state_module.new()
    state.active = true
    state.stage = "collect"
    state.mode = "replace"
    state.target_code = "abcd"
    state.display_word = "原词"

    local properties = {}
    local ctx = {
        set_property = function(_, name, value) properties[name] = value end,
        get_property = function(_, name) return properties[name] or "" end,
    }
    local core = {
        set_state_items = function() end,
        set_current_stage = function() end,
        buffer_word = function() return "" end,
        serialize_items = function() return "" end,
        deserialize_items = function() return {} end,
        items_from_text = function(text) return { { text = text } } end,
    }

    state_module.sync(ctx, state, core)
    assert_equal(properties[state_module.fields.word], "", "replacement placeholder word")

    properties[state_module.fields.word] = "原词"
    properties[state_module.fields.display] = "原词"
    properties[state_module.fields.items] = ""
    local restored = state_module.new()
    if not state_module.restore_from_context(ctx, restored, core) then
        error("replacement state was not restored")
    end
    assert_equal(#restored.items, 0, "replacement placeholder items")
end)

test("typing statistics uses the shared cache registry", function()
    unload("eosphoros.typing_stats")
    unload("eosphoros.common.eosphoros_cache_registry")
    local registry = require("eosphoros.common.eosphoros_cache_registry")
    require("eosphoros.typing_stats")
    local found = false
    for _, name in ipairs(registry.names()) do
        if name == "typing_stats" then found = true end
    end
    if not found then error("typing_stats cleaner was not registered") end
end)

test("platform adapter tolerates missing APIs and manages notifier connections", function()
    unload("eosphoros.common.eosphoros_platform")
    local saved_api = _G.rime_api
    _G.rime_api = nil
    local platform = require("eosphoros.common.eosphoros_platform")
    assert_equal(platform.user_data_dir(), nil, "missing user data API")

    _G.rime_api = { get_user_data_dir = function() error("unsupported") end }
    assert_equal(platform.user_data_dir(), nil, "failing user data API")
    _G.rime_api = { get_user_data_dir = function() return "/tmp/rime" end }
    assert_equal(platform.user_data_dir(), "/tmp/rime", "user data directory")

    local disconnected = false
    local notifier = {
        connect = function(_, callback)
            callback("connected")
            return { disconnect = function() disconnected = true end }
        end,
    }
    local observed = nil
    local connection = platform.safe_connect(notifier, function(value) observed = value end)
    assert_equal(observed, "connected", "notifier callback")
    platform.safe_disconnect(connection)
    assert_equal(disconnected, true, "notifier disconnect")
    _G.rime_api = saved_api
end)

test("explicit garbage collection batches small cleanup requests", function()
    unload("eosphoros.common.eosphoros_gc")
    local gc = require("eosphoros.common.eosphoros_gc")
    gc.reset()
    assert_equal(gc.step(40), false, "first small request")
    local pending, runs = gc.stats()
    assert_equal(pending, 40, "pending GC budget")
    assert_equal(runs, 0, "GC run count before threshold")
    assert_equal(gc.step(56), true, "threshold request")
    pending, runs = gc.stats()
    assert_equal(pending, 0, "pending GC budget after run")
    assert_equal(runs, 1, "GC run count after threshold")
    assert_equal(gc.step(1, true), true, "forced GC request")
end)

test("modular input processor components load from the eosphoros namespace", function()
    local modules = {
        "eosphoros.input.eosphoros_key_event",
        "eosphoros.input.eosphoros_processor_state",
        "eosphoros.input.eosphoros_commit_guard",
        "eosphoros.input.eosphoros_ascii_input",
        "eosphoros.input.eosphoros_direct_symbols",
        "eosphoros.input.eosphoros_punctuation",
        "eosphoros.input.eosphoros_topup",
    }
    for _, name in ipairs(modules) do
        if type(require(name)) ~= "table" then
            error(name .. " did not return a module table")
        end
    end
    local processor = require("eosphoros.eosphoros_processor")
    assert_equal(type(processor.init), "function", "processor init")
    assert_equal(type(processor.func), "function", "processor func")
    assert_equal(type(processor.fini), "function", "processor fini")
end)

test("Rime-Ice emoji overlay is available through the lazy Lua provider", function()
    unload("eosphoros.eosphoros_opencc_data")
    local data = require("eosphoros.eosphoros_opencc_data")
    data.set_context("", "eosphoros")
    local provider = data.create_provider("eosphoros_emoji_extra", "raw")
    assert_equal(provider:fetch("嗅"), "嗅 👃", "extra emoji char")
    assert_equal(provider:fetch("熬夜"), "熬夜 🫩", "extra emoji phrase")
    assert_equal(provider:fetch("指纹"), "指纹 🫆", "extra emoji alias")
    provider:release()
end)

test("new Rime-Ice emoji is appended to the actual candidate stream", function()
    unload("eosphoros.eosphoros_opencc_filter")
    unload("eosphoros.eosphoros_opencc_data")
    local data = require("eosphoros.eosphoros_opencc_data")
    local filter = require("eosphoros.eosphoros_opencc_filter")
    data.set_context("", "eosphoros")

    local segment = {
        tag = "abc",
        has_tag = function(self, tag) return self.tag == tag end,
    }
    local context = {
        input = "abcd",
        composition = { back = function() return segment end },
        get_option = function(_, name) return name == "emoji_cn" end,
        is_composing = function() return true end,
    }
    local function emoji_rule(dataset)
        return {
            triggers = { "emoji_cn" },
            tags = { abc = true },
            prefix = "emoji/",
            mode = "append",
            comment_mode = "none",
            split_mode = "emoji",
            provider = data.create_provider(dataset, "raw"),
            lookup_cache_prefix = dataset .. "\0raw\0emoji/\0",
        }
    end
    local env = {
        chain = true,
        split_pattern = "([^|]+)",
        comment_format = "〔%s〕",
        rules = {
            emoji_rule("eosphoros_emoji"),
            emoji_rule("eosphoros_emoji_extra"),
        },
        _reverse_tags = { "reverse_lookup" },
        _reverse_prefixes = {},
        engine = {
            context = context,
            schema = { page_size = 5 },
        },
    }
    local source_candidates = { candidate("phrase", 0, 4, "熬夜", "") }
    local input = {
        iter = function()
            local index = 0
            return function()
                index = index + 1
                return source_candidates[index]
            end
        end,
    }
    local yielded = {}
    _G.Candidate = candidate
    _G.yield = function(cand) yielded[#yielded + 1] = cand end

    filter.func(input, env)

    assert_equal(yielded[1] and yielded[1].text, "熬夜", "source candidate")
    assert_equal(yielded[2] and yielded[2].text, "🫩", "appended new emoji")
    assert_equal(#yielded, 2, "candidate count")
    filter.fini(env)
end)

test("ZZC operation chain recursively fills a deleted short-code gap", function()
    local chain = require("eosphoros.zzc.eosphoros_zzc_chain")
    local dictionary = {
        abcd = { "原四码词" },
        abcda = { "候补五码词" },
        abcdao = { "候补六码词" },
    }
    local records, warning = chain.plan_delete({ "原四码词" }, "abcd", function(code)
        return dictionary[code] or {}
    end)

    assert_equal(warning, nil, "chain warning")
    assert_equal(records[1].op, "delete", "delete operation")
    assert_equal(records[2].op, "move", "first compact operation")
    assert_equal(records[2].word, "候补五码词", "first compact word")
    assert_equal(records[2].code, "abcd", "first compact target")
    assert_equal(records[4].op, "move", "recursive compact operation")
    assert_equal(records[4].word, "候补六码词", "recursive compact word")
    assert_equal(records[4].code, "abcda", "recursive compact target")
end)

test("calculator equal key ignores auto-repeat until key release", function()
    unload("eosphoros.input.eosphoros_punctuation")
    local punctuation = require("eosphoros.input.eosphoros_punctuation")
    local context = {
        input = "=",
        push_input = function(self, text) self.input = self.input .. text end,
    }
    local env = { engine = { context = context } }
    local function equal_event(is_release)
        return {
            keycode = 61,
            release = function() return is_release end,
            ctrl = function() return false end,
            alt = function() return false end,
            super = function() return false end,
            repr = function() return "=" end,
        }
    end
    local opts = { jisuanqi = true, direct_symbols = false, smarttwo = false }

    punctuation.process(equal_event(true), env, "equal", false, "=", opts)
    assert_equal(
        punctuation.process(equal_event(false), env, "equal", false, "=", opts),
        1,
        "second equal press"
    )
    punctuation.process(equal_event(false), env, "equal", false, "=", opts)
    assert_equal(context.input, "==", "auto-repeat must not append another equal")
    punctuation.process(equal_event(true), env, "equal", false, "=", opts)
    punctuation.process(equal_event(false), env, "equal", false, "=", opts)
    assert_equal(context.input, "===", "new press after release may append equal")
end)

local failed = 0
for _, item in ipairs(tests) do
    local ok, err = xpcall(item.fn, debug.traceback)
    if ok then
        io.write("PASS ", item.name, "\n")
    else
        failed = failed + 1
        io.stderr:write("FAIL ", item.name, "\n", err, "\n")
    end
end

if failed > 0 then
    os.exit(1)
end

io.write(string.format("PASS %d tests\n", #tests))
