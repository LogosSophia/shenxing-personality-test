# -*- coding: utf-8 -*-
"""神性论人格王国测评 v0.8 结构题库。"""

PRINCIPLES = {
    "Ti": "自洽性与逻辑性（可理解性）",
    "Te": "建构性与目的性",
    "Ni": "收敛性、主线与终局感",
    "Ne": "发散性、可能性与新入口",
    "Si": "重复、不变、可复现的稳定基底",
    "Se": "现场、即兴、现实反馈与当下调整",
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
DOMAIN_NAMES = {"T": "思考 / 建构", "N": "主线 / 可能", "S": "稳定 / 现场", "F": "本真 / 关系"}
SAME_DOMAIN_MIRROR = {"Ti": "Te", "Te": "Ti", "Ni": "Ne", "Ne": "Ni", "Si": "Se", "Se": "Si", "Fi": "Fe", "Fe": "Fi"}

COLLAB_NAMES = {
    "TN": "TN：抽象结构 + 判断推进",
    "TS": "TS：现实步骤 + 执行处理",
    "NF": "NF：意义可能 + 价值/关系",
    "SF": "SF：具体体验 + 稳定安顿",
}

HIGH_PAIR_NAMES = {
    "A": "T双高：思考 + 做事",
    "B": "F双高：做自己 + 爱他人",
    "C": "N双高：主线收敛 + 可能发散",
    "D": "S双高：固定稳定 + 现场即兴",
}

MODULES = {
    "A": "第一部分：君主—子民互斥行为轴",
    "B": "第二部分：宰相动作偏好轴",
    "C": "第三部分：双高协同",
    "G": "第四部分：护卫防御机制",
}


def _pair(qid, module_key, prompt, a_text, a_scores, b_text, b_scores, dimension=""):
    return {
        "qid": qid,
        "module": MODULES[module_key],
        "module_key": module_key,
        "question_type": "pair",
        "front_text": prompt,
        "position": "二选一",
        "dimension": dimension,
        "principle": "",
        "scoring_key": module_key,
        "options": [
            {"key": "A", "text": a_text, "scores": a_scores},
            {"key": "B", "text": b_text, "scores": b_scores},
        ],
    }


def _single(qid, module_key, prompt, options, dimension=""):
    return {
        "qid": qid,
        "module": MODULES[module_key],
        "module_key": module_key,
        "question_type": "single_choice",
        "front_text": prompt,
        "position": "四选一",
        "dimension": dimension,
        "principle": "",
        "scoring_key": module_key,
        "options": options,
    }


def _guard(qid, prompt):
    return _pair(qid, "G", prompt, "符合", {"guard": 1}, "不符合", {"guard": 0}, "护卫防御")


QUESTIONS = [
    _pair("A01", "A", "当别人说话含混或前后不一致时，我更自然会：", "先看哪里概念不清、逻辑不通。", {"Ti": 1}, "先顺着对方的情绪和意思，让交流继续下去。", {"Fe": 1}, "Ti / Fe"),
    _pair("A02", "A", "遇到问题时，我更自然会：", "先独自想清楚它到底哪里不对。", {"Ti": 1}, "先和人沟通，看彼此感受与关系怎么接上。", {"Fe": 1}, "Ti / Fe"),
    _pair("A03", "A", "压力来时，我更自然会：", "先定目标、步骤、责任，把事情推进。", {"Te": 1}, "先确认这是不是我真正愿意承认和接受的。", {"Fi": 1}, "Te / Fi"),
    _pair("A04", "A", "做选择时，我更看重：", "这件事能不能形成结果、秩序和推进。", {"Te": 1}, "这件事有没有违背我的真实意愿和底线。", {"Fi": 1}, "Te / Fi"),
    _pair("A05", "A", "事情刚开始时，我更自然会：", "先抓住它的主线，看它最后会收束到哪里。", {"Ni": 1}, "先进入现场，根据当下反馈边做边改。", {"Se": 1}, "Ni / Se"),
    _pair("A06", "A", "局面混乱时，我更自然会：", "先抽离出来，把主线和终局重新收束清楚。", {"Ni": 1}, "先动手处理眼前发生的现实问题。", {"Se": 1}, "Ni / Se"),
    _pair("A07", "A", "遇到新问题时，我更自然会：", "立刻想到别的可能、入口或玩法。", {"Ne": 1}, "先回到固定模式、重复方式和可复现的方法里。", {"Si": 1}, "Ne / Si"),
    _pair("A08", "A", "不确定时，我更容易：", "换角度、换路径，打开更多选择。", {"Ne": 1}, "维持固定节奏和不变状态，让自己先稳住。", {"Si": 1}, "Ne / Si"),

    _single("B01", "B", "当我已经认定一件事重要后，我下一步最自然会：", [
        {"key": "A", "text": "先整理它的结构、判断标准和推进逻辑。", "scores": {"TN": 1}},
        {"key": "B", "text": "先落到具体步骤、工具、流程和现实反馈。", "scores": {"TS": 1}},
        {"key": "C", "text": "先展开它的意义、可能性、人的理解和价值感。", "scores": {"NF": 1}},
        {"key": "D", "text": "先落到具体感受、生活处境、关系安顿和实际体验。", "scores": {"SF": 1}},
    ], "宰相动作"),
    _single("B02", "B", "局面混乱时，我最先想抓住：", [
        {"key": "A", "text": "哪里的判断不清，整体结构怎么重新理顺。", "scores": {"TN": 1}},
        {"key": "B", "text": "哪个现实环节卡住了，先处理哪个步骤。", "scores": {"TS": 1}},
        {"key": "C", "text": "还有哪些可能路径，大家为什么要继续靠近它。", "scores": {"NF": 1}},
        {"key": "D", "text": "谁受到了影响，生活和关系怎么先稳定下来。", "scores": {"SF": 1}},
    ], "宰相动作"),
    _single("B03", "B", "解释一件事时，我更自然会讲：", [
        {"key": "A", "text": "它的逻辑结构、判断依据和推进方式。", "scores": {"TN": 1}},
        {"key": "B", "text": "它的具体做法、现实条件和执行反馈。", "scores": {"TS": 1}},
        {"key": "C", "text": "它的意义、可能性、价值感和理解方式。", "scores": {"NF": 1}},
        {"key": "D", "text": "它对具体生活、感受、关系和体验的影响。", "scores": {"SF": 1}},
    ], "宰相动作"),
    _single("B04", "B", "新局面开始时，我更自然从哪里切入：", [
        {"key": "A", "text": "先建立判断框架和推进结构。", "scores": {"TN": 1}},
        {"key": "B", "text": "先看工具、流程、步骤和现场条件。", "scores": {"TS": 1}},
        {"key": "C", "text": "先看它能展开成什么意义和可能。", "scores": {"NF": 1}},
        {"key": "D", "text": "先看人的状态、实际体验和生活落点。", "scores": {"SF": 1}},
    ], "宰相动作"),

    _single("C01", "C", "在真实做事时，我最常能同时做到：", [
        {"key": "A", "text": "保持思路清楚，同时把事情推进成结果。", "scores": {"A": 1}},
        {"key": "B", "text": "守住真实自我，同时照顾他人的感受。", "scores": {"B": 1}},
        {"key": "C", "text": "抓住主线收束，同时保留可能展开。", "scores": {"C": 1}},
        {"key": "D", "text": "保持固定节奏，同时进入现场处理变化。", "scores": {"D": 1}},
    ], "双高协同"),
    _single("C02", "C", "局面混乱时，我更能同时抓住：", [
        {"key": "A", "text": "哪里不对，以及下一步怎么做。", "scores": {"A": 1}},
        {"key": "B", "text": "我不能违背什么，以及别人需要怎样被回应。", "scores": {"B": 1}},
        {"key": "C", "text": "事情的主线，以及新的转机。", "scores": {"C": 1}},
        {"key": "D", "text": "稳定经验，以及现场反馈。", "scores": {"D": 1}},
    ], "双高协同"),
    _single("C03", "C", "推进事情时，我更自然能同时保持：", [
        {"key": "A", "text": "判断清楚和执行有力。", "scores": {"A": 1}},
        {"key": "B", "text": "真实意愿和关系连接。", "scores": {"B": 1}},
        {"key": "C", "text": "主线方向和开放可能。", "scores": {"C": 1}},
        {"key": "D", "text": "稳定节奏和现实应变。", "scores": {"D": 1}},
    ], "双高协同"),
    _single("C04", "C", "复盘或解释自己时，我更自然会同时说明：", [
        {"key": "A", "text": "逻辑依据和现实成效。", "scores": {"A": 1}},
        {"key": "B", "text": "真实动机和对他人的影响。", "scores": {"B": 1}},
        {"key": "C", "text": "主线走向和可能变化。", "scores": {"C": 1}},
        {"key": "D", "text": "经验基础和现场事实。", "scores": {"D": 1}},
    ], "双高协同"),

    _guard("G01", "当某类压力反复出现后，我会形成一套固定的处理办法；它未必是我喜欢的方式，但确实能让我不被那类问题拖住。"),
    _guard("G02", "我压力大时有私人的排解方法，哪怕我知道它不一定好，也很难马上找到理由停止。"),
    _guard("G03", "有些事情一旦刺到我，我会很快进入一种“处理模式”，先把问题隔离、压住或转化掉。"),
    _guard("G04", "面对曾经让我很难承受的压力，我现在通常不会直接被它击穿，而是会自动启动某种应对方式。"),
    _guard("G05", "我并不总是认同自己应对压力的方式，但关键时刻我还是会用，因为它有效。"),
    _guard("G06", "压力越大，我越容易变得不像平时的自己：更冷、更硬、更会处理问题，或者更封闭。"),
    _guard("G07", "有些防御方式已经变成习惯了，即使危险过去，我也会继续维持一段时间。"),
    _guard("G08", "别人有时会误以为我用来保护自己的那套方式就是我的本性。"),
]
