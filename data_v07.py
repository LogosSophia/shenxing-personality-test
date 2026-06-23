# -*- coding: utf-8 -*-
"""神性论人格王国测评 v0.7 数据表。

v0.7 不再直接询问宰相/护卫/帝师/元帅自述。
题目只测八大结构原则的取舍，再由王国模板归位。
"""

PRINCIPLES = {
    "Ti": "自洽性与逻辑性（可理解性）",
    "Te": "建构性与目的性",
    "Ni": "涌现性与压缩性",
    "Ne": "创生性与可能性",
    "Si": "守恒性和不变性",
    "Se": "在场性和现实性",
    "Fi": "本真性和统一性",
    "Fe": "关联性和互系性",
}

TYPE_MAP = {
    "INTP": {"monarch": "Ti", "chancellor": "Ne", "guard": "Si", "civilian": "Fe", "emperor": "Ni", "marshal": "Fi"},
    "ENTP": {"monarch": "Ne", "chancellor": "Ti", "guard": "Fe", "civilian": "Si", "emperor": "Te", "marshal": "Se"},
    "ISTP": {"monarch": "Ti", "chancellor": "Se", "guard": "Ni", "civilian": "Fe", "emperor": "Si", "marshal": "Fi"},
    "ESTP": {"monarch": "Se", "chancellor": "Ti", "guard": "Fe", "civilian": "Ni", "emperor": "Te", "marshal": "Ne"},
    "INFP": {"monarch": "Fi", "chancellor": "Ne", "guard": "Si", "civilian": "Te", "emperor": "Ni", "marshal": "Ti"},
    "ENFP": {"monarch": "Ne", "chancellor": "Fi", "guard": "Te", "civilian": "Si", "emperor": "Fe", "marshal": "Se"},
    "ISFP": {"monarch": "Fi", "chancellor": "Se", "guard": "Ni", "civilian": "Te", "emperor": "Si", "marshal": "Ti"},
    "ESFP": {"monarch": "Se", "chancellor": "Fi", "guard": "Te", "civilian": "Ni", "emperor": "Fe", "marshal": "Ne"},
    "INTJ": {"monarch": "Ni", "chancellor": "Te", "guard": "Fi", "civilian": "Se", "emperor": "Ti", "marshal": "Si"},
    "ENTJ": {"monarch": "Te", "chancellor": "Ni", "guard": "Se", "civilian": "Fi", "emperor": "Ne", "marshal": "Fe"},
    "INFJ": {"monarch": "Ni", "chancellor": "Fe", "guard": "Ti", "civilian": "Se", "emperor": "Fi", "marshal": "Si"},
    "ENFJ": {"monarch": "Fe", "chancellor": "Ni", "guard": "Se", "civilian": "Ti", "emperor": "Ne", "marshal": "Te"},
    "ISTJ": {"monarch": "Si", "chancellor": "Te", "guard": "Fi", "civilian": "Ne", "emperor": "Ti", "marshal": "Ni"},
    "ESTJ": {"monarch": "Te", "chancellor": "Si", "guard": "Ne", "civilian": "Fi", "emperor": "Se", "marshal": "Fe"},
    "ISFJ": {"monarch": "Si", "chancellor": "Fe", "guard": "Ti", "civilian": "Ne", "emperor": "Fi", "marshal": "Ni"},
    "ESFJ": {"monarch": "Fe", "chancellor": "Si", "guard": "Ne", "civilian": "Ti", "emperor": "Se", "marshal": "Te"},
}

FUNCTIONS = ["Ti", "Te", "Ni", "Ne", "Si", "Se", "Fi", "Fe"]
DOMAIN_OF = {"Ti": "T", "Te": "T", "Ni": "N", "Ne": "N", "Si": "S", "Se": "S", "Fi": "F", "Fe": "F"}
DOMAIN_NAMES = {"T": "可理解 / 可建构", "N": "方向 / 可能", "S": "守恒 / 现实", "F": "本真 / 关联"}
SAME_DOMAIN_MIRROR = {"Ti": "Te", "Te": "Ti", "Ni": "Ne", "Ne": "Ni", "Si": "Se", "Se": "Si", "Fi": "Fe", "Fe": "Fi"}

MODULES = {"D": "第一部分：四域强度", "I": "第二部分：域内方向", "M": "第三部分：八原则混战", "H": "第四部分：高低位辅助"}

def _pair(qid, module_key, prompt, a_text, a_scores, b_text, b_scores, principle=""):
    return {"qid": qid, "module": MODULES[module_key], "module_key": module_key, "question_type": "pair", "front_text": prompt, "position": "原则取舍", "dimension": principle, "principle": PRINCIPLES.get(principle, ""), "scoring_key": module_key, "options": [{"key": "A", "text": a_text, "scores": a_scores}, {"key": "B", "text": b_text, "scores": b_scores}]}

def _mixed(qid, prompt, options):
    return {"qid": qid, "module": MODULES["M"], "module_key": "M", "question_type": "best_worst", "front_text": prompt, "position": "八原则混战", "dimension": "", "principle": "", "scoring_key": "Mixed", "options": options}

QUESTIONS = [
    _pair("D01", "D", "以下两种判断都合理，但你更自然先看哪一个？", "一件事是否清楚、讲得通、能被检查。", {"T": 1}, "一件事是否有方向、是否能打开更深的可能。", {"N": 1}),
    _pair("D02", "D", "一个想法更容易吸引你的是：", "它结构清楚，不是散乱的一团。", {"T": 1}, "它有展开空间，不会很快被说完。", {"N": 1}),
    _pair("D03", "D", "面对一套旧办法，你更在意：", "它现在是否说得清、安排得明白。", {"T": 1}, "它是否经过时间验证、还能稳定延续。", {"S": 1}),
    _pair("D04", "D", "你更容易承认一件事成立，是因为：", "它有清楚的理由、规则或责任。", {"T": 1}, "它有可靠的经验、节奏或延续。", {"S": 1}),
    _pair("D05", "D", "当道理/责任和感受/关系发生冲突时，你更容易先承认：", "即使感受上不舒服，只要道理和责任清楚，它仍然有道理。", {"T": 1}, "即使道理和责任说得通，如果它伤到真心或关系，我也很难接受。", {"F": 1}),
    _pair("D06", "D", "你更怕一种局面变成：", "混乱、说不通、没人负责。", {"T": 1}, "冷硬、失真、人与人之间接不上。", {"F": 1}),
    _pair("D07", "D", "你更在意一件事：", "后面会走向哪里。", {"N": 1}, "是否稳定、可靠、能延续。", {"S": 1}),
    _pair("D08", "D", "面对一个听起来有意义但还不稳定的方向：", "只要方向有意义，我愿意继续看。", {"N": 1}, "如果不能落在稳定经验里，我会保留。", {"S": 1}),
    _pair("D09", "D", "你做判断时，更容易先看：", "它背后的趋势、可能和走向。", {"N": 1}, "它是否真诚，是否照顾到人的感受和关系。", {"F": 1}),
    _pair("D10", "D", "哪种感觉更像“变空了”？", "一件事看不到更深走向或新可能。", {"N": 1}, "一件事失去真实感或关系感。", {"F": 1}),
    _pair("D11", "D", "你更信任：", "稳定、熟悉、经过时间沉淀的东西。", {"S": 1}, "真诚、贴近内心、能让人接上的东西。", {"F": 1}),
    _pair("D12", "D", "当稳定节奏和人的真实/关系发生冲突时，你更倾向于：", "先保住稳定节奏，让事情不要散掉。", {"S": 1}, "先保住真实感和关系连接，让人不要断掉。", {"F": 1}),
    _pair("I01", "I", "Ti / Te：你更难放下哪一个？", "事情能推进，但核心道理说不通，我会卡住。", {"Ti": 1}, "事情还能讨论，但责任清楚、结果能落地，我会先推进。", {"Te": 1}, "Ti"),
    _pair("I02", "I", "Ti / Te：哪种失败更让你难受？", "做成了，但里面的逻辑是乱的。", {"Ti": 1}, "讲清了，但事情没有结果。", {"Te": 1}, "Ti"),
    _pair("I03", "I", "Ti / Te：你更习惯先问：", "前提、边界和理由是否成立？", {"Ti": 1}, "目标、路径和责任是否成立？", {"Te": 1}, "Ti"),
    _pair("I04", "I", "Ni / Ne：你更自然的动作是：", "把复杂信息压成一个真正的方向。", {"Ni": 1}, "让一个局面继续生成新的可能。", {"Ne": 1}, "Ni"),
    _pair("I05", "I", "Ni / Ne：你更不喜欢：", "一直分散展开，最后不知道通向哪里。", {"Ni": 1}, "太早收束定向，新的入口都被关掉。", {"Ne": 1}, "Ni"),
    _pair("I06", "I", "Ni / Ne：你更常在意：", "一件事背后真正的走向。", {"Ni": 1}, "一件事还能怎样变化、怎样展开。", {"Ne": 1}, "Ni"),
    _pair("I07", "I", "Si / Se：你更相信：", "经过时间沉淀、可以延续下来的东西。", {"Si": 1}, "当下正在发生、可以直接处理的现实。", {"Se": 1}, "Si"),
    _pair("I08", "I", "Si / Se：你更愿意：", "把稳定经验继续打磨得更可靠。", {"Si": 1}, "直接进入现场，在现实反馈里调整。", {"Se": 1}, "Si"),
    _pair("I09", "I", "Si / Se：你更自然觉得一个东西“有重量”，是因为：", "它承接了过去。", {"Si": 1}, "它能进入现实处理。", {"Se": 1}, "Si"),
    _pair("I10", "I", "Fi / Fe：你更不能接受：", "自己内在过不去、变得不像自己。", {"Fi": 1}, "关系断裂、无人回应、彼此接不上。", {"Fe": 1}, "Fi"),
    _pair("I11", "I", "Fi / Fe：哪种选择更难认同？", "背离真实的自己，即使有好处。", {"Fi": 1}, "让关系场破裂，即使理由充分。", {"Fe": 1}, "Fi"),
    _pair("I12", "I", "Fi / Fe：你更会先问：", "这是不是我真正认可的？", {"Fi": 1}, "这是否还能让人与人继续连接？", {"Fe": 1}, "Fi"),
    _mixed("M01", "面对一个重要计划，请选“最不能放下”和“最能暂时放下”：", [{"key": "A", "text": "它必须说得通，不能自相矛盾。", "principle": "Ti"}, {"key": "B", "text": "它必须有目标、责任和结果。", "principle": "Te"}, {"key": "C", "text": "它必须有清楚的长期方向。", "principle": "Ni"}, {"key": "D", "text": "它必须保留新的可能和调整空间。", "principle": "Ne"}]),
    _mixed("M02", "面对一个重要关系或团队，请选“最不能放下”和“最能暂时放下”：", [{"key": "A", "text": "它必须有稳定经验和可延续的节奏。", "principle": "Si"}, {"key": "B", "text": "它必须能进入现实行动，而不是停在想法里。", "principle": "Se"}, {"key": "C", "text": "它不能让我违背真实的自己。", "principle": "Fi"}, {"key": "D", "text": "它不能让人彼此孤立、无人回应。", "principle": "Fe"}]),
    _mixed("M03", "当一件事出现问题时，请选“最先想保住”和“最能暂时放下”：", [{"key": "A", "text": "逻辑和边界不能乱。", "principle": "Ti"}, {"key": "B", "text": "责任和推进不能断。", "principle": "Te"}, {"key": "C", "text": "方向和趋势不能丢。", "principle": "Ni"}, {"key": "D", "text": "可能和出口不能封死。", "principle": "Ne"}]),
    _mixed("M04", "当局面开始失控时，请选“最先想保住”和“最能暂时放下”：", [{"key": "A", "text": "过去积累下来的秩序和经验。", "principle": "Si"}, {"key": "B", "text": "现场还能不能直接处理。", "principle": "Se"}, {"key": "C", "text": "自己内在是否还统一。", "principle": "Fi"}, {"key": "D", "text": "人和人之间是否还能接上。", "principle": "Fe"}]),
    _mixed("M05", "你更容易被哪种说法打动？请选“最打动”和“最能暂时放下”：", [{"key": "A", "text": "这个说法自洽，前提清楚。", "principle": "Ti"}, {"key": "B", "text": "这个方案能落地，责任明确。", "principle": "Te"}, {"key": "C", "text": "这条路背后有真正的方向。", "principle": "Ni"}, {"key": "D", "text": "这个想法还能继续展开。", "principle": "Ne"}]),
    _mixed("M06", "你更容易被哪种说法打动？请选“最打动”和“最能暂时放下”：", [{"key": "A", "text": "这是经过时间验证的做法。", "principle": "Si"}, {"key": "B", "text": "这能立刻进入现实处理。", "principle": "Se"}, {"key": "C", "text": "这没有背叛真实的自己。", "principle": "Fi"}, {"key": "D", "text": "这能让关系重新接上。", "principle": "Fe"}]),
    _mixed("M07", "哪种失败最让你觉得“这件事不成立”？请选“最不能接受”和“最能暂时放下”：", [{"key": "A", "text": "里面根本说不通。", "principle": "Ti"}, {"key": "B", "text": "最后没有结果、没人负责。", "principle": "Te"}, {"key": "C", "text": "完全看不出它通向哪里。", "principle": "Ni"}, {"key": "D", "text": "它把新的可能都封死了。", "principle": "Ne"}]),
    _mixed("M08", "哪种失败最让你觉得“这件事不成立”？请选“最不能接受”和“最能暂时放下”：", [{"key": "A", "text": "它切断了原本的延续和积累。", "principle": "Si"}, {"key": "B", "text": "它离现实太远，不能真正处理。", "principle": "Se"}, {"key": "C", "text": "它让人背离自己。", "principle": "Fi"}, {"key": "D", "text": "它让关系断裂、无人回应。", "principle": "Fe"}]),
    _pair("H01", "H", "面对自己的倾向，你更像：", "直接按自己的倾向行动，不太需要把它解释成一套完整说法。", {"high": 0}, "会自然想把自己的倾向解释清楚，让它在更高层面站得住。", {"high": 1}),
    _pair("H02", "H", "你更在意：", "自己知道怎么选就够了，不一定要形成一套说法。", {"high": 0}, "自己的判断能被定性、说明、安放进一套更大的理解里。", {"high": 1}),
    _pair("H03", "H", "你做选择时，更像：", "回应眼前情况。", {"high": 0}, "维护某种自己认定的原则或道路。", {"high": 1}),
    _pair("H04", "H", "你更常见的顺序是：", "先行动、先反应，之后再理解自己为什么这样。", {"high": 0}, "先试图理解这件事在自己生命里意味着什么，再决定怎么行动。", {"high": 1}),
]
