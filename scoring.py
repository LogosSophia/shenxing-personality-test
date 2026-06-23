# -*- coding: utf-8 -*-
from collections import defaultdict
from data import QUESTIONS, TYPE_MAP, PRINCIPLES

FUNCTIONS = ["Ti", "Te", "Ni", "Ne", "Si", "Se", "Fi", "Fe"]
OPPOSITE = {
    "Ti": "Fe", "Fe": "Ti",
    "Te": "Fi", "Fi": "Te",
    "Ni": "Se", "Se": "Ni",
    "Ne": "Si", "Si": "Ne",
}

# 元帅由君主轴决定，同一君主下的两个底盘元帅相同；它辅助确定君主，而不是辅助区分同君主底盘。
MARSHAL_BY_MONARCH = {}
for _type_name, _type_map in TYPE_MAP.items():
    _monarch = _type_map["monarch"]
    _marshal = _type_map["marshal"]
    if _monarch in MARSHAL_BY_MONARCH and MARSHAL_BY_MONARCH[_monarch] != _marshal:
        raise ValueError(f"Inconsistent marshal mapping for monarch {_monarch}")
    MARSHAL_BY_MONARCH[_monarch] = _marshal

ROLE_WORDS = {
    "Ti": "清楚、自洽、讲得通",
    "Te": "结果、责任、推进",
    "Ni": "未来线、深层方向、终局感",
    "Ne": "可能性、出口、新连接",
    "Si": "经验、稳定、延续",
    "Se": "当下、身体、现场和现实后果",
    "Fi": "真心、底线、自我统一",
    "Fe": "关系、回应、连接",
}


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else 0.0


def centered(values):
    avg = mean(values.values())
    return {k: v - avg for k, v in values.items()}


def _level_from_emperor(emperor_score, emperor_centered):
    """帝师三档：绝对显露 + 相对突出，避免单纯高分/低分作答风格污染。"""
    if emperor_score >= 4.00 and emperor_centered >= 0.15:
        return "高位"
    if emperor_score >= 3.75 or emperor_centered >= 0.30:
        return "高位倾向"
    return "低位"


def compute_scores(answers):
    """answers: dict[qid] -> 1..5"""
    buckets = defaultdict(list)
    for q in QUESTIONS:
        qid = q["qid"]
        key = q["scoring_key"]
        if qid in answers:
            buckets[key].append(float(answers[qid]))

    pos = {}
    core_positive = {}
    core_aversion = {}
    civilian_evidence = {}
    chancellor_raw = {}
    guard_raw = {}
    emperor_raw = {}
    marshal_raw = {}

    for f in FUNCTIONS:
        core_positive[f] = mean(buckets[f"{f}_CorePositive"])
        core_aversion[f] = mean(buckets[f"{f}_CoreAversion"])
        # 子民证据：不主动拥抱该功能 + 讨厌被迫进入该功能。
        civilian_evidence[f] = 0.45 * (6.0 - core_positive[f]) + 0.55 * core_aversion[f]
        chancellor_raw[f] = mean(buckets[f"{f}_Chancellor"])
        guard_raw[f] = mean(buckets[f"{f}_Guard"])
        emperor_raw[f] = mean(buckets[f"{f}_EmperorTeacher"])
        marshal_raw[f] = mean(buckets[f"{f}_Marshal"])
        pos[f] = {
            "CorePositive": core_positive[f],
            "CoreAversion": core_aversion[f],
            "CivilianEvidence": civilian_evidence[f],
            "Chancellor": chancellor_raw[f],
            "Guard": guard_raw[f],
            "EmperorTeacher": emperor_raw[f],
            "Marshal": marshal_raw[f],
        }

    cp_c = centered(core_positive)
    civ_c = centered(civilian_evidence)
    ch_c = centered(chancellor_raw)
    guard_c = centered(guard_raw)
    emperor_c = centered(emperor_raw)
    marshal_c = centered(marshal_raw)

    monarch_axis = {}
    monarch_axis_centered = {}
    for f in FUNCTIONS:
        opposite = OPPOSITE[f]
        marshal_for_monarch = MARSHAL_BY_MONARCH[f]
        # 君主轴：正面拥抱君主 + 反面不愿面对其子民 + 极端处元帅确认。
        # 元帅是君主面对子民压力时的最后手段，因此辅助确定君主；它不参与同君主两个底盘的分支裁决。
        monarch_axis[f] = (
            0.40 * core_positive[f]
            + 0.45 * civilian_evidence[opposite]
            + 0.15 * marshal_raw[marshal_for_monarch]
        )
        monarch_axis_centered[f] = (
            0.40 * cp_c[f]
            + 0.45 * civ_c[opposite]
            + 0.15 * marshal_c[marshal_for_monarch]
        )

    monarch_order = sorted(
        FUNCTIONS,
        key=lambda f: (monarch_axis_centered[f], monarch_axis[f]),
        reverse=True,
    )
    chosen_monarch = monarch_order[0]
    second_monarch = monarch_order[1]
    monarch_gap = monarch_axis_centered[chosen_monarch] - monarch_axis_centered[second_monarch]

    detail = {}
    type_scores = {}
    branch_scores = {}
    branch_scores_centered = {}

    for t, m in TYPE_MAP.items():
        monarch = m["monarch"]
        chancellor = m["chancellor"]
        guard = m["guard"]
        civilian = m["civilian"]
        emperor = m["emperor"]
        marshal = m["marshal"]

        chancellor_score = chancellor_raw[chancellor]
        guard_score = guard_raw[guard]
        civilian_score = civilian_evidence[civilian]
        marshal_score = marshal_raw[marshal]
        emperor_score = emperor_raw[emperor]

        # 底盘分支：君主确定后，宰相必须先被锚定。
        # 护卫只能轻微校正稳定方式，不能用护卫强行推出宰相；否则高位结构会被误判成相邻底盘。
        chancellor_anchor = 0.65 * chancellor_score + 0.35 * core_positive[chancellor]
        chancellor_anchor_centered = 0.65 * ch_c[chancellor] + 0.35 * cp_c[chancellor]
        branch_score = 0.90 * chancellor_anchor + 0.10 * guard_score
        branch_score_centered = 0.90 * chancellor_anchor_centered + 0.10 * guard_c[guard]
        branch_scores[t] = branch_score
        branch_scores_centered[t] = branch_score_centered

        # 展示用接近度：君主轴优先，分支为辅。
        score = 0.68 * monarch_axis[monarch] + 0.32 * branch_score
        type_scores[t] = score

        detail[t] = {
            "monarch_raw": core_positive[monarch],
            "monarch_aversion": core_aversion[monarch],
            "monarch_axis": monarch_axis[monarch],
            "monarch_axis_centered": monarch_axis_centered[monarch],
            "monarch_marshal": marshal_raw[MARSHAL_BY_MONARCH[monarch]],
            "chancellor": chancellor_score,
            "chancellor_centered": ch_c[chancellor],
            "chancellor_anchor": chancellor_anchor,
            "chancellor_anchor_centered": chancellor_anchor_centered,
            "guard": guard_score,
            "guard_centered": guard_c[guard],
            "civilian": civilian_score,
            "civilian_positive": core_positive[civilian],
            "civilian_aversion": core_aversion[civilian],
            "latent_civilian": max(civilian_score, guard_score - 0.50),
            "emperor": emperor_score,
            "emperor_centered": emperor_c[emperor],
            "marshal": marshal_score,
            "branch_score": branch_score,
            "branch_score_centered": branch_score_centered,
            "score": score,
        }

    same_monarch_candidates = [t for t, m in TYPE_MAP.items() if m["monarch"] == chosen_monarch]
    candidate_order = sorted(
        same_monarch_candidates,
        key=lambda t: (branch_scores_centered[t], branch_scores[t]),
        reverse=True,
    )
    top_type = candidate_order[0]
    second_same_monarch = candidate_order[1]
    branch_gap = branch_scores_centered[top_type] - branch_scores_centered[second_same_monarch]

    # 16型底盘分按综合接近度展示；最终判型仍先看君主轴，再看同君主分支。
    overall_order = sorted(
        TYPE_MAP.keys(),
        key=lambda t: (type_scores[t], branch_scores_centered[t], monarch_axis_centered[TYPE_MAP[t]["monarch"]]),
        reverse=True,
    )
    ordered = [(t, type_scores[t]) for t in overall_order]
    overall_gap = type_scores[overall_order[0]] - type_scores[overall_order[1]] if len(overall_order) > 1 else 0.0
    near_types = [
        t for t in overall_order[1:]
        if type_scores[top_type] - type_scores[t] <= 0.10
    ]
    near_cross_monarch_types = [
        t for t in near_types
        if TYPE_MAP[t]["monarch"] != chosen_monarch
    ]

    d = detail[top_type]
    m = TYPE_MAP[top_type]

    level = _level_from_emperor(d["emperor"], d["emperor_centered"])
    is_high = level == "高位"

    risks = []

    if monarch_gap < 0.08:
        risks.append({
            "title": "核心判断区分度较低",
            "body": "你在几个核心判断之间的差距很小，结果更适合理解为当前最接近的结构，而不是绝对定型。建议结合详细数据里的前几名候选一起看。",
        })

    if branch_gap < 0.08:
        risks.append({
            "title": "做事分支区分度较低",
            "body": "当前核心判断确定后，两个相邻底盘候选的做事方式和稳定方式差距不大，因此底盘分支需要谨慎理解。",
        })

    if overall_gap < 0.08 and near_types:
        risks.append({
            "title": "近邻类型分数很接近",
            "body": "本次前几名底盘分差距很小，说明结构可能处在相邻类型边界，或部分高位功能正在抬高相邻底盘。建议重点参考人格王国位次，而不是只看标题类型。",
        })

    if near_cross_monarch_types:
        risks.append({
            "title": "存在跨君主近邻候选",
            "body": "有不同君主的候选类型与当前结果分数很接近。若本人长期自我认同或外部观察明显更接近近邻候选，应优先结合位次结构复核，而不是硬判单一类型。",
        })

    guard_takeover = (
        d["guard"] >= 4.30
        and d["guard_centered"] >= 0.35
        and d["guard_centered"] - d["chancellor_centered"] >= 0.35
    )
    if guard_takeover:
        if is_high:
            risks.append({
                "title": "稳定方式很强，可能形成高防御型结构",
                "body": "你的稳定方式分数明显偏高。它能帮助你挡住外界冲击，但也可能让你更容易隔离、过滤或转译压力，使真实压力不容易直接被看见。",
            })
        else:
            risks.append({
                "title": "稳定方式偏强，核心判断可能被防御遮住",
                "body": "你的稳定方式分数明显偏高。这不代表不好，但说明你在受压时可能先进入防御和稳定程序，而不是直接回到自己的核心判断。",
            })

    if d["civilian"] >= 4.50:
        risks.append({
            "title": "反面压力比较明显",
            "body": "你对某类状态的排斥或不愿面对比较明显。它不一定会直接表现为痛苦，也可能转成防御、行动、解释或极端反应。",
        })
    elif d["latent_civilian"] >= 4.20 and d["guard"] >= 4.00 and d["civilian"] < 4.20:
        risks.append({
            "title": "压力可能被稳定方式压住",
            "body": "你的反面压力分不算过高，但稳定方式分较高。因此不能简单理解为压力很轻，更可能是压力已经被隔离、过滤或转成了别的形式。",
        })

    if d["marshal"] >= 4.50:
        risks.append({
            "title": "极端反应较强",
            "body": "你在极度受压时的强烈反应比较明显。它可能表现为对外决裂、强烈否定，也可能表现为自责或自我攻击。需要留意这类反应是否过早出现。",
        })

    if overall_gap < 0.05 or near_cross_monarch_types:
        confidence = "低"
    elif monarch_gap >= 0.20 and branch_gap >= 0.15 and overall_gap >= 0.08:
        confidence = "高"
    elif monarch_gap >= 0.10 and branch_gap >= 0.08:
        confidence = "中"
    else:
        confidence = "低"

    gap = min(monarch_gap, branch_gap, overall_gap)

    return {
        "positions": pos,
        "monarch_axis": monarch_axis,
        "monarch_axis_centered": monarch_axis_centered,
        "chosen_monarch": chosen_monarch,
        "second_monarch": second_monarch,
        "branch_scores": branch_scores,
        "branch_scores_centered": branch_scores_centered,
        "type_scores": type_scores,
        "detail": detail,
        "ordered_types": ordered,
        "top_type": top_type,
        "second_type": second_same_monarch,
        "level": level,
        "confidence": confidence,
        "gap": gap,
        "monarch_gap": monarch_gap,
        "branch_gap": branch_gap,
        "overall_gap": overall_gap,
        "near_types": near_types,
        "near_cross_monarch_types": near_cross_monarch_types,
        "map": m,
        "risks": risks,
    }


def _chain_sentence(monarch, chancellor, guard, civilian, emperor, marshal):
    return (
        f"你的核心判断偏向 **{ROLE_WORDS[monarch]}**；"
        f"做事时更容易依靠 **{ROLE_WORDS[chancellor]}**；"
        f"最不喜欢被迫面对的反面压力偏向 **{ROLE_WORDS[civilian]}**；"
        f"你会用 **{ROLE_WORDS[guard]}** 来让自己稳定，或把压力处理成自己能承受的形式；"
        f"你会用 **{ROLE_WORDS[emperor]}** 为自己的判断寻找解释；"
        f"压力到极端时，**{ROLE_WORDS[marshal]}** 可能成为你的强烈反应。"
    )


def build_report(result):
    t = result["top_type"]
    level = result["level"]
    m = result["map"]
    d = result["detail"][t]

    monarch = m["monarch"]
    chancellor = m["chancellor"]
    guard = m["guard"]
    civilian = m["civilian"]
    emperor = m["emperor"]
    marshal = m["marshal"]

    if level == "低位":
        phase = "这里的低位不是能力低，而是解释方式还没有充分显露：你的核心判断正在形成和巩固。"
    elif level == "高位倾向":
        phase = "这里的高位倾向不是更好或更成熟，而是解释方式已经开始显露，但还不宜直接判为稳定高位。"
    else:
        phase = "这里的高位不是更好、更健康或更温和，而是你已经会为自己的核心判断寻找一套解释。"

    chain = _chain_sentence(monarch, chancellor, guard, civilian, emperor, marshal)
    latent_note = ""
    if d["latent_civilian"] > d["civilian"] + 0.25:
        latent_note = (
            f"\n\n另外，你的反面压力分为 {d['civilian']:.2f}，"
            f"但结合稳定方式后，隐藏压力指标约为 {d['latent_civilian']:.2f}。"
            "这说明有些压力可能已经被你过滤、隔离或转成了别的形式。"
        )

    near_note = ""
    near_types = result.get("near_types", [])[:3]
    if near_types:
        near_note = f"\n\n近邻候选包括：**{'、'.join(near_types)}**。这些类型与当前结果分数很接近，应结合王国位次一起看。"

    return f"""
这次结果显示，你当前最接近：**{level} {t}**。

{phase}

整体来看，{chain}{latent_note}{near_note}

本次总体接近度为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。这次判型先看核心判断、反面压力和极端反应构成的主轴，再用做事方式和稳定方式确定底盘分支，最后再看解释方式判断高低位。
""".strip()
