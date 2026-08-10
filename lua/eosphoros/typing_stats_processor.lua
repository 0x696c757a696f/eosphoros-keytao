local stats = require("eosphoros.typing_stats")

return {
    init = stats.init_processor,
    func = stats.processor,
    fini = stats.fini_processor,
}
