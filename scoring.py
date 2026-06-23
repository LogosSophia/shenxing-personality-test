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

        # v0.5: 子民压力可能被护卫压住。
        # 显性子民分低，不一定代表子民压力低；若同一王国的护卫很高，说明压力可能已被过滤/转译。
        latent_civilian = max(civilian_score, guard_score - 0.50)

        # 子民与元帅是定位证据，不应因过载而无限线性加分。
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

    # 高低位只判帝师气质是否显露；护卫、子民、元帅不拦截高位，只进入变体/风险提示。
    high = d["emperor"] >= 4.00
    level = "高位" if high else "低位"

    risks = []

    guard_takeover = d["guard"] >= 4.30 and (
        d["guard"] >= d["monarch_raw"] or d["guard"] - d["chancellor"] >= 0.50
    )
    if guard_takeover:
        if high:
            risks.append({
                "title": "高位异型倾向：护卫型高位变体",
                "body": "你的护卫功能分数明显偏高。高位不代表护卫不能强；相反，护卫过强可能形成一种高位变体：王国已经有解释自身秩序的能力，但守门结构可能开始改写王国的外在表现，使人格显得更稳定、克制、封闭或防御化。本结果不判定你已经成为异型，只提示：存在护卫型高位变体倾向。",
            })
        else:
            risks.append({
                "title": "护卫强势，王位可能被防御结构遮蔽",
                "body": "你的护卫功能分数明显偏高。低位阶段的护卫强势不直接称为异型；它更像是王位尚未完全显露时，守门结构过度用力，可能让人格看起来稳定、克制或成熟，但这种稳定未必来自君主连续统治。",
            })

    if d["civilian"] >= 4.50:
        if high:
            risks.append({
                "title": "高位但子民裂口明显",
                "body": "你的子民位分数明显偏高。高位说明帝师气质已经显露，但不代表子民追债消失。这个结果提示：你的王国已经能解释自身秩序，同时仍有一个低位原则强烈叩问王国，形成明显裂口。",
            })
        else:
            risks.append({
                "title": "子民追债过载",
                "body": "你的子民位分数明显偏高。子民可以帮助定位王国结构，但过高时说明某个低位入口持续叩问王国，可能让君主需要不断证明自己、解释自己或防御自己。",
            })
    elif d["latent_civilian"] >= 4.20 and d["guard"] >= 4.00 and d["civilian"] < 4.20:
        risks.append({
            "title": "子民压力可能被护卫压住",
            "body": "你的显性子民分不算过高，但护卫分较高，因此不能简单理解为子民压力很轻。更可能的情况是：低位压力已经被护卫系统隔离、过滤或转译，所以表面刺痛下降，但防御系统被迫升高。",
        })

    if d["marshal"] >= 4.50:
        if high:
            risks.append({
                "title": "高位元帅强势，战时兵权明显",
                "body": "你的元帅反相分数明显偏高。高位不代表元帅低，也不代表没有兵权；它说明帝师已经显露，但王国在极限处调用战时兵权的能力很强。需要进一步观察的是：这套兵权是否被帝师纳入解释和节制，还是容易过早出兵或转向自我清算。",
            })
        else:
            risks.append({
                "title": "元帅过激，君主连续性容易被打断",
                "body": "你的元帅反相分数明显偏高。低位阶段元帅过强，可能意味着王国在受压时容易过早进入截断、清算、决裂、现实撕开或自我定罪，使君主连续统治被战时兵权打断。",
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
        f"你的主线偏向 **{monarch}：{ROLE_WORDS[monarch]}**；"
        f"低位压力会从 **{civilian}：{ROLE_WORDS[civilian]}** 处追问你；"
        f"你的护卫会用 **{guard}：{ROLE_WORDS[guard]}** 来隔离、过滤或转译压力；"
        f"帝师则以 **{emperor}：{ROLE_WORDS[emperor]}** 为这条主线提供解释和辩护；"
        f"极端时，元帅可能以 **{marshal}：{ROLE_WORDS[marshal]}** 的方式向外出兵，或转向自我清算。"
    )


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
        phase = "低位不是能力低，而是帝师气质尚未显露：王国正在建立君主连续统治，但还没有充分解释自身秩序。"
        core_problem = f"当前核心问题是：{monarch} 君主如何连续坐稳王位，并等待 {emperor} 帝师气质显露。"
    else:
        phase = "高位不是更激烈，也不是更温和，而是帝师气质已经显露：王国开始解释自身秩序。"
        core_problem = f"当前核心问题不再只是 {monarch} 能不能统治，而是 {monarch} 王国如何经由 {emperor} 帝师解释自身合法性。"

    chain = _chain_sentence(monarch, chancellor, guard, civilian, emperor, marshal)
    latent_note = ""
    if d["latent_civilian"] > d["civilian"] + 0.25:
        latent_note = f"\n\n注意：你的显性子民分为 {d['civilian']:.2f}，但结合护卫分后，潜在子民压力约为 {d['latent_civilian']:.2f}。这说明压力可能已经被护卫系统过滤或转译，不能只按表面子民分理解。"

    return f"""
你的人格王国测评结果为：**{level} {t}**。

{phase}

你的王国以 **{monarch}——{p[monarch]}** 为君主，以 **{chancellor}——{p[chancellor]}** 为宰相，以 **{guard}——{p[guard]}** 为护卫，以 **{civilian}——{p[civilian]}** 为子民。帝师为 **{emperor}——{p[emperor]}**，元帅为 **{marshal}——{p[marshal]}**。

{core_problem}

动态链条：{chain}{latent_note}

本次底盘分为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。其中君主原始分 {d['monarch_raw']:.2f}，宰相分 {d['chancellor']:.2f}，护卫分 {d['guard']:.2f}，子民分 {d['civilian']:.2f}，潜在子民压力 {d['latent_civilian']:.2f}，帝师分 {d['emperor']:.2f}，元帅分 {d['marshal']:.2f}。

最终判定：**当前最接近：{level} {t}**。
""".strip()
