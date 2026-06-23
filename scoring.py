# -*- coding: utf-8 -*-
from collections import defaultdict
from data import QUESTIONS, TYPE_MAP, PRINCIPLES

FUNCTIONS = ["Ti", "Te", "Ni", "Ne", "Si", "Se", "Fi", "Fe"]

ROLE_WORDS = {
    "Ti": "清楚、自洽、讲得通",
    "Te": "结果、责任、推进",
    "Ni": "未来线、深层方向、终局感",
    "Ne": "可能性、出口、新连接",
    "Si": "过去经验、连续性、留住之物",
    "Se": "当下、身体、现场和现实后果",
    "Fi": "真心、底线、自我统一",
    "Fe": "关系、回应、共同处境",
}


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else 0.0


def compute_scores(answers):
    """answers: dict[qid] -> 1..5"""
    buckets = defaultdict(list)
    for q in QUESTIONS:
        qid = q["qid"]
        key = q["scoring_key"]
        if qid in answers:
            buckets[key].append(float(answers[qid]))

    pos = {}
    for f in FUNCTIONS:
        pos[f] = {
            "MonarchRaw": mean(buckets[f"{f}_MonarchRaw"]),
            "Chancellor": mean(buckets[f"{f}_Chancellor"]),
            "Guard": mean(buckets[f"{f}_Guard"]),
            "Civilian": mean(buckets[f"{f}_Civilian"]),
            "EmperorTeacher": mean(buckets[f"{f}_EmperorTeacher"]),
            "Marshal": mean(buckets[f"{f}_Marshal"]),
        }

    type_scores = {}
    detail = {}
    for t, m in TYPE_MAP.items():
        monarch = m["monarch"]
        chancellor = m["chancellor"]
        guard = m["guard"]
        civilian = m["civilian"]
        emperor = m["emperor"]
        marshal = m["marshal"]

        monarch_raw = pos[monarch]["MonarchRaw"]
        chancellor_score = pos[chancellor]["Chancellor"]
        guard_score = pos[guard]["Guard"]
        civilian_score = pos[civilian]["Civilian"]
        marshal_score = pos[marshal]["Marshal"]
        emperor_score = pos[emperor]["EmperorTeacher"]

        # v0.5: 压力可能被稳定方式压住；显性压力低，不一定代表压力不存在。
        latent_civilian = max(civilian_score, guard_score - 0.50)
        civilian_evidence = min(latent_civilian, 4.20)
        marshal_evidence = min(marshal_score, 4.20)

        score = (
            0.40 * monarch_raw
            + 0.20 * chancellor_score
            + 0.15 * guard_score
            + 0.15 * civilian_evidence
            + 0.10 * marshal_evidence
        )
        type_scores[t] = score
        detail[t] = {
            "monarch_raw": monarch_raw,
            "chancellor": chancellor_score,
            "guard": guard_score,
            "civilian": civilian_score,
            "latent_civilian": latent_civilian,
            "civilian_evidence": civilian_evidence,
            "emperor": emperor_score,
            "marshal": marshal_score,
            "marshal_evidence": marshal_evidence,
            "score": score,
        }

    ordered = sorted(type_scores.items(), key=lambda x: x[1], reverse=True)
    top_type, top_score = ordered[0]
    second_type, second_score = ordered[1]
    d = detail[top_type]
    m = TYPE_MAP[top_type]

    # 高低位只看解释方式是否显露。
    high = d["emperor"] >= 4.00
    level = "高位" if high else "低位"

    risks = []

    guard_takeover = d["guard"] >= 4.30 and (
        d["guard"] >= d["monarch_raw"] or d["guard"] - d["chancellor"] >= 0.50
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
        if high:
            risks.append({
                "title": "压力来源比较明显",
                "body": "你的压力来源分数明显偏高。即使你已经能解释自己的核心判断，也仍然会被某类问题反复追问。",
            })
        else:
            risks.append({
                "title": "压力来源过载",
                "body": "你的压力来源分数明显偏高。这说明某类问题会持续追问你，让你需要不断证明、解释或防御自己。",
            })
    elif d["latent_civilian"] >= 4.20 and d["guard"] >= 4.00 and d["civilian"] < 4.20:
        risks.append({
            "title": "压力可能被稳定方式压住",
            "body": "你的显性压力分不算过高，但稳定方式分较高。因此不能简单理解为压力很轻，更可能是压力已经被隔离、过滤或转成了别的形式。",
        })

    if d["marshal"] >= 4.50:
        if high:
            risks.append({
                "title": "极端反应较强",
                "body": "你在极度受压时的强烈反应比较明显。它可能表现为对外决裂、强烈否定，也可能表现为自责或自我攻击。需要留意这类反应是否过早出现。",
            })
        else:
            risks.append({
                "title": "极端反应容易打断自己",
                "body": "你在极度受压时可能较快进入强烈否定、决裂、清算或自我攻击，使原本的核心判断难以连续稳定地运作。",
            })

    gap = top_score - second_score
    if gap >= 0.30:
        confidence = "高"
    elif gap >= 0.15:
        confidence = "中"
    else:
        confidence = "低"

    return {
        "positions": pos,
        "type_scores": type_scores,
        "detail": detail,
        "ordered_types": ordered,
        "top_type": top_type,
        "second_type": second_type,
        "level": level,
        "confidence": confidence,
        "gap": gap,
        "map": m,
        "risks": risks,
    }


def _chain_sentence(monarch, chancellor, guard, civilian, emperor, marshal):
    return (
        f"你的核心判断偏向 **{ROLE_WORDS[monarch]}**；"
        f"做事时更容易依靠 **{ROLE_WORDS[chancellor]}**；"
        f"压力常从 **{ROLE_WORDS[civilian]}** 处出现；"
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
            f"\n\n另外，你的显性压力分为 {d['civilian']:.2f}，"
            f"但结合稳定方式后，隐藏压力指标约为 {d['latent_civilian']:.2f}。"
            "这说明有些压力可能已经被你过滤、隔离或转成了别的形式。"
        )

    return f"""
这次结果显示，你当前最接近：**{level} {t}**。

{phase}

整体来看，{chain}{latent_note}

本次总体接近度为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。如果置信度不是“高”，说明你和相邻结构之间有重叠，结果更适合理解为“当前最接近”，而不是绝对定型。
""".strip()
