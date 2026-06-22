# -*- coding: utf-8 -*-
from collections import defaultdict
from data import QUESTIONS, TYPE_MAP, PRINCIPLES

FUNCTIONS = ["Ti", "Te", "Ni", "Ne", "Si", "Se", "Fi", "Fe"]

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

        civilian_evidence = min(civilian_score, 4.20)
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

    high = (
        d["emperor"] >= 4.00
        and d["monarch_raw"] >= 3.70
        and d["marshal"] < 4.50
    )

    if high:
        level = "高位"
    else:
        level = "低位"

    risks = []
    if d["guard"] >= 4.30 and (d["guard"] >= d["monarch_raw"] or d["guard"] - d["chancellor"] >= 0.50):
        risks.append({
            "title": "护卫过高，存在异型风险",
            "body": "你的护卫功能分数明显偏高。护卫本来负责保护王国，使君主在压力下不被外部冲击打断。但当护卫过高时，它可能不再只是守门，而是开始代替君主统治。此时人格会显得稳定、成熟、克制、可控，但这种稳定可能不是君主坐稳后的合法秩序，而是护卫过度接管后的防御秩序。本结果不判定你已经成为异型，只提示：你的王国存在护卫过度接管风险。"
        })
    if d["civilian"] >= 4.50:
        risks.append({
            "title": "子民刺痛过载",
            "body": "你的子民位分数明显偏高。子民刺痛可以帮助定位王国结构，但过高时不应继续理解为君主更强，而应理解为低位压力过载。它说明某个低位入口持续叩问王国，可能让君主需要不断证明自己、解释自己或防御自己。"
        })
    if d["marshal"] >= 4.50:
        risks.append({
            "title": "元帅过激风险",
            "body": "你的元帅反相分数明显偏高。元帅是君主在极端处调用的反相兵权，它可以保护王国边界，但过高时可能意味着你太早进入截断、清算、决裂或现实撕开，而不是让君主连续统治。"
        })
    if d["emperor"] >= 4.00 and not high:
        risks.append({
            "title": "帝师强但王位连续性不足",
            "body": "你的帝师气质已经显出，但君主连续性条件尚未完全满足。也就是说，你可能已经具有解释王国秩序的高阶能力，但王位仍可能被压力、子民刺痛、护卫接管或元帅反相打断。因此本次不直接判高位，而提示：高位倾向存在，王国仍需巩固。"
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

def build_report(result):
    t = result["top_type"]
    level = result["level"]
    m = result["map"]
    d = result["detail"][t]
    p = PRINCIPLES

    monarch = m["monarch"]
    chancellor = m["chancellor"]
    guard = m["guard"]
    civilian = m["civilian"]
    emperor = m["emperor"]
    marshal = m["marshal"]

    if level == "低位":
        phase = "低位不是能力低，而是君主秩序正在建立，类似秦：重点是结束混乱、确立君主连续统治。"
        core_problem = f"当前核心问题是：{monarch} 君主能否连续坐稳王位，而不被压力、刺痛、护卫或元帅打断。"
    else:
        phase = "高位不是更激烈，而是君主已经坐稳，王国开始解释自身秩序，类似汉：重点是合法性、义理化与高阶解释。"
        core_problem = f"当前核心问题不再是 {monarch} 能不能连续统治，而是 {monarch} 王国凭什么成立、如何解释自身秩序。"

    return f"""
你的人格王国测评结果为：**{level} {t}**。

{phase}

你的王国以 **{monarch}——{p[monarch]}** 为君主，以 **{chancellor}——{p[chancellor]}** 为宰相，以 **{guard}——{p[guard]}** 为护卫，以 **{civilian}——{p[civilian]}** 为子民。帝师为 **{emperor}——{p[emperor]}**，元帅为 **{marshal}——{p[marshal]}**。

{core_problem}

本次底盘分为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。其中君主原始分 {d['monarch_raw']:.2f}，宰相分 {d['chancellor']:.2f}，护卫分 {d['guard']:.2f}，子民分 {d['civilian']:.2f}，帝师分 {d['emperor']:.2f}，元帅分 {d['marshal']:.2f}。

最终判定：**{level} {t}**。
""".strip()
