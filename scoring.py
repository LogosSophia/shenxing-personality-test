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
    marshal_c = centered(marshal_raw)

    monarch_axis = {}
    monarch_axis_centered = {}
    for f in FUNCTIONS:
        opposite = OPPOSITE[f]
        # 君主轴：正面拥抱君主 + 反面不愿面对其子民。
        monarch_axis[f] = 0.45 * core_positive[f] + 0.55 * civilian_evidence[opposite]
        monarch_axis_centered[f] = 0.45 * cp_c[f] + 0.55 * civ_c[opposite]

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

        # 底盘分支：君主确定后，主要看宰相，其次护卫，元帅只作极端确认；帝师不参与底盘判定。
        branch_score = 0.70 * chancellor_score + 0.20 * guard_score + 0.10 * marshal_score
        branch_score_centered = 0.70 * ch_c[chancellor] + 0.20 * guard_c[guard] + 0.10 * marshal_c[marshal]
        branch_scores[t] = branch_score
        branch_scores_centered[t] = branch_score_centered

        # 展示用接近度：君主轴优先，分支为辅。
        score = 0.65 * monarch_axis[monarch] + 0.35 * branch_score
        type_scores[t] = score

        detail[t] = {
            "monarch_raw": core_positive[monarch],
            "monarch_aversion": core_aversion[monarch],
            "monarch_axis": monarch_axis[monarch],
            "monarch_axis_centered": monarch_axis_centered[monarch],
            "chancellor": chancellor_score,
            "guard": guard_score,
            "civilian": civilian_score,
            "civilian_positive": core_positive[civilian],
            "civilian_aversion": core_aversion[civilian],
            "latent_civilian": max(civilian_score, guard_score - 0.50),
            "emperor": emperor_score,
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

    # 排序展示：先按君主轴，再按分支支持度。这样不会再让不同君主的类型用纯线性总分一锅比较。
    ordered_types = sorted(
        TYPE_MAP.keys(),
        key=lambda t: (
            monarch_axis_centered[TYPE_MAP[t]["monarch"]],
            branch_scores_centered[t],
            type_scores[t],
        ),
        reverse=True,
    )
    ordered = [(t, type_scores[t]) for t in ordered_types]

    d = detail[top_type]
    m = TYPE_MAP[top_type]

    high = d["emperor"] >= 4.00
    level = "高位" if high else "低位"

    risks = []

    if monarch_gap < 0.08:
        risks.append({
            "title": "核心判断区分度较低",
            "body": "你在几个核心判断之间的差距很小，结果更适合理解为当前最接近的结构，而不是绝对定型。建议结合详细数据里的前几名候选一起看。",
        })

    if branch_gap < 0.08:
        risks.append({
            "title": "做事分支区分度较低",
            "body": "当前核心判断确定后，两个相邻底盘候选的做事方式、稳定方式和极端反应差距不大，因此底盘分支需要谨慎理解。",
        })

    guard_takeover = d["guard"] >= 4.30 and (
        d["guard"] >= d["monarch_axis"] or d["guard"] - d["chancellor"] >= 0.50
    )
    if guard_takeover:
        if high:
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

    if monarch_gap >= 0.20 and branch_gap >= 0.15:
        confidence = "高"
    elif monarch_gap >= 0.10 and branch_gap >= 0.08:
        confidence = "中"
    else:
        confidence = "低"

    gap = min(monarch_gap, branch_gap)

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

    return f"""
这次结果显示，你当前最接近：**{level} {t}**。

{phase}

整体来看，{chain}{latent_note}

本次总体接近度为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。这次判型先看核心判断与反面压力构成的主轴，再用做事方式和稳定方式确定底盘分支，最后再看解释方式判断高低位。
""".strip()
