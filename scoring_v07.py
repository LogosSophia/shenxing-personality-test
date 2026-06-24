# -*- coding: utf-8 -*-
from data_v07 import (
    QUESTIONS,
    TYPE_MAP,
    FUNCTIONS,
    DOMAIN_OF,
    DOMAIN_NAMES,
    SAME_DOMAIN_MIRROR,
    COLLAB_NAMES,
    HIGH_PAIR_NAMES,
)

ROLE_WORDS = {
    "Ti": "自洽、可理解、说得通",
    "Te": "建构、目的、责任和结果",
    "Ni": "主线、收敛、终局感",
    "Ne": "发散、可能、新入口",
    "Si": "重复、不变、可复现的稳定基底",
    "Se": "现场、即兴、现实反馈",
    "Fi": "本真、底线、自我统一",
    "Fe": "关联、回应、关系成立",
}

ROLE_EXPLAINS = {
    "monarch": "君主表示你以什么样的方式认识世界。",
    "chancellor": "宰相表示你最顺的组织方式。",
    "guard": "护卫表示你怎么处理冲突。",
    "civilian": "子民表示压力更多从什么地方来。",
    "emperor": "帝师表示你怎么解释你的秩序。",
    "marshal": "元帅表示你最后的手段。",
}

COLLAB_KEYS = ["TN", "TS", "NF", "SF"]
HIGH_KEYS = ["A", "B", "C", "D"]
HIGH_KEY_BY_DOMAIN = {"T": "A", "F": "B", "N": "C", "S": "D"}


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else 0.0


def centered(values):
    avg = mean(values.values())
    return {k: v - avg for k, v in values.items()}


def _option_for(q, key):
    for option in q.get("options", []):
        if option.get("key") == key:
            return option
    return None


def _rank_map(scores):
    ordered = sorted(scores, key=lambda f: scores[f], reverse=True)
    return {f: i + 1 for i, f in enumerate(ordered)}, ordered


def _collab_key(f1, f2):
    domains = {DOMAIN_OF[f1], DOMAIN_OF[f2]}
    if domains == {"T", "N"}:
        return "TN"
    if domains == {"T", "S"}:
        return "TS"
    if domains == {"N", "F"}:
        return "NF"
    if domains == {"S", "F"}:
        return "SF"
    return ""


def _guard_viability(score):
    """护卫不要求异常高；50 分以上视为可用，0 分才明显扣。"""
    return max(0.0, min(100.0, score * 2.0))


def _level_from_high_hits(hits):
    if hits >= 3:
        return "高位"
    if hits >= 2:
        return "高位倾向"
    return "低位"


def _variant_risk(score):
    if score >= 7:
        return "高"
    if score >= 6:
        return "中"
    return "低"


def _guard_status(score):
    if score <= 2:
        return "护卫偏低"
    if score <= 5:
        return "护卫正常"
    if score == 6:
        return "护卫偏强"
    return "护卫强"


def _confidence(overall_gap, monarch_gap, branch_gap, monarch_score, chancellor_action, guard_viability):
    gap = min(overall_gap, monarch_gap, branch_gap)
    if gap >= 10 and monarch_score >= 75 and chancellor_action >= 50 and guard_viability >= 50:
        return "高"
    if gap >= 5 and monarch_score >= 50 and chancellor_action >= 25:
        return "中"
    return "低"


def compute_scores(answers):
    axis_raw = {f: 0.0 for f in FUNCTIONS}
    axis_max = {f: 0.0 for f in FUNCTIONS}
    collab_raw = {k: 0.0 for k in COLLAB_KEYS}
    collab_total = 0.0
    high_raw = {k: 0.0 for k in HIGH_KEYS}
    high_total = 0.0
    guard_score = 0
    guard_total = 0

    for q in QUESTIONS:
        qid = q["qid"]
        qtype = q.get("question_type")
        module_key = q.get("module_key")
        answer = answers.get(qid)
        option = _option_for(q, answer) if answer else None

        if qtype == "pair" and module_key == "A":
            for candidate in q.get("options", []):
                for key in candidate.get("scores", {}):
                    if key in FUNCTIONS:
                        axis_max[key] += 1
            if option:
                for key, value in option.get("scores", {}).items():
                    if key in FUNCTIONS:
                        axis_raw[key] += value

        elif qtype == "single_choice" and module_key == "B":
            collab_total += 1
            if option:
                for key, value in option.get("scores", {}).items():
                    if key in collab_raw:
                        collab_raw[key] += value

        elif qtype == "single_choice" and module_key == "C":
            high_total += 1
            if option:
                for key, value in option.get("scores", {}).items():
                    if key in high_raw:
                        high_raw[key] += value

        elif qtype == "pair" and module_key == "G":
            guard_total += 1
            if option:
                guard_score += int(option.get("scores", {}).get("guard", 0))

    behavior_scores = {}
    for f in FUNCTIONS:
        behavior_scores[f] = axis_raw[f] / axis_max[f] * 100 if axis_max[f] else 50.0
    behavior_centered = centered(behavior_scores)

    collab_scores = {k: (collab_raw[k] / collab_total * 100 if collab_total else 0.0) for k in COLLAB_KEYS}
    high_pair_scores = {k: (high_raw[k] / high_total * 100 if high_total else 0.0) for k in HIGH_KEYS}

    # v0.8 中，“principle_scores”作为兼容字段，实际含义是君主—子民行为轴分。
    principle_scores = dict(behavior_scores)
    principle_centered = dict(behavior_centered)
    ranks, principle_order = _rank_map(principle_scores)

    domain_scores = {}
    for domain in ["T", "N", "S", "F"]:
        fs = [f for f in FUNCTIONS if DOMAIN_OF[f] == domain]
        domain_scores[domain] = mean([behavior_scores[f] for f in fs])
    direction_scores = dict(behavior_scores)
    mixed_scores = {f: 50.0 for f in FUNCTIONS}

    positions = {
        f: {
            "PrincipleScore": principle_scores[f],
            "PrincipleCentered": principle_centered[f],
            "BehaviorScore": behavior_scores[f],
            "BehaviorCentered": behavior_centered[f],
            "Domain": DOMAIN_OF[f],
            "DomainScore": domain_scores[DOMAIN_OF[f]],
            "DirectionScore": direction_scores[f],
            "MixedScore": mixed_scores[f],
            "Rank": ranks[f],
        }
        for f in FUNCTIONS
    }

    detail = {}
    type_scores = {}
    branch_scores = {}
    branch_scores_centered = {}
    guard_pct = guard_score / guard_total * 100 if guard_total else 0.0

    for type_name, m in TYPE_MAP.items():
        monarch = m["monarch"]
        chancellor = m["chancellor"]
        guard = m["guard"]
        civilian = m["civilian"]
        emperor = m["emperor"]
        marshal = m["marshal"]
        adviser = SAME_DOMAIN_MIRROR[monarch]
        strategist = SAME_DOMAIN_MIRROR[guard]

        collab_key = _collab_key(monarch, chancellor)
        chancellor_action = collab_scores.get(collab_key, 0.0)
        monarch_axis = behavior_scores[monarch]
        civilian_behavior = behavior_scores[civilian]
        civilian_fit = 100.0 - civilian_behavior
        monarch_pair_fit = 0.70 * monarch_axis + 0.30 * civilian_fit
        high_key = HIGH_KEY_BY_DOMAIN[DOMAIN_OF[chancellor]]
        high_hits = int(high_raw.get(high_key, 0))
        high_fit = high_pair_scores.get(high_key, 0.0)
        guard_viability = _guard_viability(behavior_scores[guard])

        # 主型：君主—子民轴定主权，宰相动作定组织方式，护卫可用度压低镜像误判。
        # 护卫不要求很高；50 分已视为可用，但 0 分会明显削弱该王国。
        score = 0.52 * monarch_pair_fit + 0.33 * chancellor_action + 0.15 * guard_viability
        type_scores[type_name] = score
        branch_scores[type_name] = chancellor_action
        branch_scores_centered[type_name] = chancellor_action - mean(collab_scores.values())

        detail[type_name] = {
            "monarch_raw": monarch_axis,
            "monarch_axis": monarch_pair_fit,
            "monarch_axis_centered": monarch_pair_fit - 50.0,
            "monarch_behavior": monarch_axis,
            "monarch_marshal": behavior_scores[marshal],
            "chancellor": chancellor_action,
            "chancellor_behavior": behavior_scores[chancellor],
            "chancellor_centered": chancellor_action - mean(collab_scores.values()),
            "chancellor_collab_key": collab_key,
            "guard": guard_pct,
            "guard_behavior": behavior_scores[guard],
            "guard_viability": guard_viability,
            "guard_centered": guard_pct - 50.0,
            "guard_score_raw": guard_score,
            "guard_score_total": guard_total,
            "guard_status": _guard_status(guard_score),
            "civilian": civilian_fit,
            "civilian_behavior": civilian_behavior,
            "civilian_fit": civilian_fit,
            "civilian_positive": behavior_scores[civilian],
            "civilian_aversion": 100.0 - behavior_scores[civilian],
            "latent_civilian": behavior_scores[civilian],
            "emperor": high_fit,
            "emperor_behavior": behavior_scores[emperor],
            "emperor_centered": high_fit - 50.0,
            "emperor_high_key": high_key,
            "high_hits": high_hits,
            "marshal": behavior_scores[marshal],
            "marshal_behavior": behavior_scores[marshal],
            "branch_score": branch_scores[type_name],
            "branch_score_centered": branch_scores_centered[type_name],
            "hierarchy_score": 50.0,
            "hierarchy_bonus": 0.0,
            "core_type_score": score,
            "core_type_score_centered": 0.0,
            "role_axis_bonus": 0.0,
            "monarch_rank_penalty": 0.0,
            "score": score,
        }

    score_avg = mean(type_scores.values())
    for t in detail:
        detail[t]["core_type_score_centered"] = type_scores[t] - score_avg

    ordered_types = sorted(TYPE_MAP.keys(), key=lambda t: type_scores[t], reverse=True)
    top_type = ordered_types[0]
    second_type = ordered_types[1]
    top_score = type_scores[top_type]
    overall_gap = top_score - type_scores[second_type]
    m = TYPE_MAP[top_type]
    top_monarch = m["monarch"]
    second_monarch = next((TYPE_MAP[t]["monarch"] for t in ordered_types if TYPE_MAP[t]["monarch"] != top_monarch), top_monarch)
    second_monarch_score = next((type_scores[t] for t in ordered_types if TYPE_MAP[t]["monarch"] != top_monarch), top_score)
    monarch_gap = top_score - second_monarch_score
    same_monarch_candidates = [t for t in ordered_types if TYPE_MAP[t]["monarch"] == top_monarch]
    second_same_monarch = same_monarch_candidates[1] if len(same_monarch_candidates) > 1 else top_type
    branch_gap = top_score - type_scores[second_same_monarch]

    d = detail[top_type]
    level = _level_from_high_hits(d.get("high_hits", 0))
    variant_risk = _variant_risk(guard_score)
    road = "未知"
    ending = "未知"
    near_types = [t for t in ordered_types[1:] if top_score - type_scores[t] <= 5.0]
    near_cross_monarch_types = [t for t in near_types if TYPE_MAP[t]["monarch"] != top_monarch]

    risks = []
    if d.get("monarch_behavior", 0) < 75:
        risks.append({"title": "君主轴不够明显", "body": "当前候选的君主—子民互斥轴没有拉开到很高，主型可能需要更多样本题确认。"})
    if d.get("guard_viability", 0) < 50:
        risks.append({"title": "护卫可用度偏低", "body": "当前候选王国的护卫在行为轴上偏低，若该项长期成立，可能说明镜像候选更稳，或护卫尚未成型。"})
    if branch_gap < 5.0:
        risks.append({"title": "宰相动作近邻", "body": "同一君主下的两个候选宰相分差较小，说明动作偏好还不够稳定。"})
    if overall_gap < 5.0:
        risks.append({"title": "近邻类型分数很接近", "body": "前几名结构分差距较小，建议结合君主轴分和宰相动作分一起看。"})
    if near_cross_monarch_types:
        risks.append({"title": "存在跨君主近邻候选", "body": "有不同君主的候选类型与当前结果接近，说明君主轴可能处在边界。"})
    if guard_score >= 6:
        risks.append({"title": "护卫强，存在异型风险", "body": "护卫防御机制分较高，说明你可能已经形成明显防御方式，外显气质可能被护卫改写。"})
    elif guard_score <= 2:
        risks.append({"title": "护卫偏低", "body": "护卫防御机制分较低，说明子民压力可能更容易直接暴露，防御方式尚未稳定成型。"})

    confidence = _confidence(overall_gap, monarch_gap, branch_gap, d.get("monarch_behavior", 0), d.get("chancellor", 0), d.get("guard_viability", 0))

    return {
        "positions": positions,
        "principle_scores": principle_scores,
        "principle_order": principle_order,
        "domain_scores": domain_scores,
        "direction_scores": direction_scores,
        "mixed_scores": mixed_scores,
        "behavior_scores": behavior_scores,
        "behavior_centered": behavior_centered,
        "collab_scores": collab_scores,
        "high_pair_scores": high_pair_scores,
        "high_count": d.get("high_hits", 0),
        "guard_score": guard_score,
        "guard_total": guard_total,
        "guard_status": _guard_status(guard_score),
        "variant_risk": variant_risk,
        "road": road,
        "ending": ending,
        "chosen_monarch": top_monarch,
        "second_monarch": second_monarch,
        "monarch_axis": principle_scores,
        "monarch_axis_centered": principle_centered,
        "branch_scores": branch_scores,
        "branch_scores_centered": branch_scores_centered,
        "type_scores": type_scores,
        "detail": detail,
        "ordered_types": [(t, type_scores[t]) for t in ordered_types],
        "top_type": top_type,
        "second_type": second_type,
        "level": level,
        "confidence": confidence,
        "gap": min(overall_gap, monarch_gap, branch_gap),
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
        f"君主为 **{monarch}（{ROLE_WORDS[monarch]}）**；"
        f"宰相为 **{chancellor}（{ROLE_WORDS[chancellor]}）**；"
        f"护卫为 **{guard}（{ROLE_WORDS[guard]}）**；"
        f"子民为 **{civilian}（{ROLE_WORDS[civilian]}）**；"
        f"帝师为 **{emperor}（{ROLE_WORDS[emperor]}）**；"
        f"元帅为 **{marshal}（{ROLE_WORDS[marshal]}）**。"
    )


def build_report(result):
    t = result["top_type"]
    m = result["map"]
    d = result["detail"][t]
    near_types = result.get("near_types", [])[:3]
    near_note = f"\n\n近邻候选包括：**{'、'.join(near_types)}**。" if near_types else ""
    axis_order = "、".join(f"{f}({result['behavior_scores'][f]:.1f})" for f in result.get("principle_order", [])[:4])
    collab_key = d.get("chancellor_collab_key", "")
    collab_label = COLLAB_NAMES.get(collab_key, collab_key)
    high_key = d.get("emperor_high_key", "")
    high_label = HIGH_PAIR_NAMES.get(high_key, high_key)

    return f"""
**人格王国：{t}**  
**位阶：{result['level']}**  
**异型风险：{result.get('variant_risk', '低')}**  
**道路：{result.get('road', '未知')}**  
**终局：{result.get('ending', '未知')}**

你的王国结构显示，你更接近 **{t}**。

**君主｜{m['monarch']}**  
君主表示你以什么样的方式认识世界。你的核心认识方式更接近 **{m['monarch']}（{ROLE_WORDS[m['monarch']]}）**：你会自然从它出发判断世界、捕捉问题，并决定什么东西真正成立。

**宰相｜{m['chancellor']}**  
宰相表示你最顺的组织方式。当你已经认定一件事重要之后，你更容易用 **{m['chancellor']}（{ROLE_WORDS[m['chancellor']]}）** 的方式把它组织起来、推进下去，或让它形成可运转的结构。本次宰相动作通道为：**{collab_label}**。

**护卫｜{m['guard']}**  
护卫表示你怎么处理冲突。它不一定是你最喜欢的部分，但当压力逼近、局面失控、弱点被触碰时，你会倾向于用 **{m['guard']}（{ROLE_WORDS[m['guard']]}）** 来保护王国，让自己不被压力直接击穿。本次护卫防御机制为：**{result.get('guard_score', 0)}/{result.get('guard_total', 8)}，{result.get('guard_status', '')}**。

**子民｜{m['civilian']}**  
子民表示压力更多从什么地方来。你的压力裂口更容易出现在 **{m['civilian']}（{ROLE_WORDS[m['civilian']]}）** 所代表的方向：它可能不是你完全不在意的东西，反而常常是你想处理、想补上、但自然不顺的位置。

**帝师｜{m['emperor']}**  
帝师表示你怎么解释自己的秩序。当你需要把自己的判断说清楚、上升成一套更高层的解释时，**{m['emperor']}（{ROLE_WORDS[m['emperor']]}）** 可能作为你的解释方式或高位资源出现。本次双高协同为：**{high_label}**，命中 **{d.get('high_hits', 0)}/4**。

**元帅｜{m['marshal']}**  
元帅表示你最后的手段。它不是日常状态，而是在极端压力、王国秩序无法正常运转时，可能被调用出来的最后手段。

君主—子民行为轴前四为：**{axis_order}**。{near_note}

本次结构分为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。v0.8 主型使用“君主—子民互斥行为轴”“宰相动作偏好轴”和“护卫可用度”共同压缩镜像误判；双高题只判断位阶，护卫题只判断防御机制与异型风险，不参与主型判定。
""".strip()
