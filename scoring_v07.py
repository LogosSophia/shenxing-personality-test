# -*- coding: utf-8 -*-
from data_v07 import (
    QUESTIONS,
    TYPE_MAP,
    FUNCTIONS,
    DOMAIN_OF,
    DOMAIN_NAMES,
    SAME_DOMAIN_MIRROR,
    COLLAB_NAMES,
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
    "guard": "护卫表示你如何保护并维持自己的王国秩序。",
    "civilian": "子民表示压力更多从什么地方来。",
    "emperor": "帝师表示你怎么解释你的秩序。",
    "marshal": "元帅表示你最后的手段。",
}

COLLAB_KEYS = ["TN", "TS", "NF", "SF"]
DOMAIN_KEYS = ["T", "N", "S", "F"]


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


def _adviser_fit(monarch_behavior, adviser_behavior):
    """谏臣是君主合法性的追问位：不宜太低，也不宜接近/压过君主。"""
    if adviser_behavior >= monarch_behavior - 5:
        return 35.0
    if 20 <= adviser_behavior <= 60:
        return 100.0
    if adviser_behavior < 20:
        return 75.0
    if adviser_behavior <= 75:
        return 85.0
    return 55.0


def _confidence(overall_gap, monarch_gap, branch_gap, role_legality, chancellor_action, domain_fit):
    gap = min(overall_gap, monarch_gap, branch_gap)
    if gap >= 10 and role_legality >= 75 and chancellor_action >= 50 and domain_fit >= 45:
        return "高"
    if gap >= 5 and role_legality >= 60 and chancellor_action >= 25:
        return "中"
    return "低"


def compute_scores(answers):
    axis_raw = {f: 0.0 for f in FUNCTIONS}
    axis_max = {f: 0.0 for f in FUNCTIONS}
    collab_raw = {k: 0.0 for k in COLLAB_KEYS}
    collab_total = 0.0
    stress_raw = {k: 0.0 for k in COLLAB_KEYS}
    stress_total = 0.0
    domain_raw = {k: 0.0 for k in DOMAIN_KEYS}
    domain_total = 0.0
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

        elif qtype == "single_choice" and module_key == "X":
            stress_total += 1
            if option:
                for key, value in option.get("scores", {}).items():
                    if key in stress_raw:
                        stress_raw[key] += value

        elif qtype == "single_choice" and module_key == "D":
            domain_total += 1
            if option:
                for key, value in option.get("scores", {}).items():
                    if key in domain_raw:
                        domain_raw[key] += value

        elif qtype == "pair" and module_key == "G":
            guard_total += 1
            if option:
                guard_score += int(option.get("scores", {}).get("guard", 0))

    behavior_scores = {}
    for f in FUNCTIONS:
        behavior_scores[f] = axis_raw[f] / axis_max[f] * 100 if axis_max[f] else 50.0
    behavior_centered = centered(behavior_scores)

    collab_scores = {k: (collab_raw[k] / collab_total * 100 if collab_total else 0.0) for k in COLLAB_KEYS}
    stress_scores = {k: (stress_raw[k] / stress_total * 100 if stress_total else 0.0) for k in COLLAB_KEYS}

    behavior_domain_scores = {}
    for domain in DOMAIN_KEYS:
        fs = [f for f in FUNCTIONS if DOMAIN_OF[f] == domain]
        behavior_domain_scores[domain] = mean([behavior_scores[f] for f in fs])
    domain_scores = {k: (domain_raw[k] / domain_total * 100 if domain_total else behavior_domain_scores[k]) for k in DOMAIN_KEYS}

    # v0.8 中，“principle_scores”作为兼容字段，实际含义是君主—子民行为轴分。
    principle_scores = dict(behavior_scores)
    principle_centered = dict(behavior_centered)
    ranks, principle_order = _rank_map(principle_scores)
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
    stress_branch_scores = {}
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
        stress_key = _collab_key(monarch, guard)
        chancellor_action = collab_scores.get(collab_key, 0.0)
        stress_action = stress_scores.get(stress_key, 0.0)
        monarch_behavior = behavior_scores[monarch]
        adviser_behavior = behavior_scores[adviser]
        civilian_behavior = behavior_scores[civilian]
        adviser_legality_fit = _adviser_fit(monarch_behavior, adviser_behavior)
        civilian_pressure_fit = 100.0 - civilian_behavior

        # 第一部分只定君主—子民主轴：君主要高，子民要低；谏臣是合法性追问位，区间合理即可。
        # 宰相、帝师、护卫、元帅不从第一部分直接定强弱，主要由后续动作/域/压力模块解释。
        role_legality = 0.62 * monarch_behavior + 0.30 * civilian_pressure_fit + 0.08 * adviser_legality_fit
        illegal_high = mean([adviser_behavior, civilian_behavior])

        # 四域主要校验“君主域”，宰相域由动作题补足。
        domain_monarch = domain_scores[DOMAIN_OF[monarch]]
        domain_chancellor = domain_scores[DOMAIN_OF[chancellor]]
        domain_fit = 0.70 * domain_monarch + 0.30 * domain_chancellor

        # v0.8.4：不再测高位；主型只由君主—子民合法性、宰相动作、四域底色、压力协同判断。
        score = 0.50 * role_legality + 0.30 * chancellor_action + 0.15 * domain_fit + 0.05 * stress_action
        type_scores[type_name] = score
        branch_scores[type_name] = chancellor_action
        branch_scores_centered[type_name] = chancellor_action - mean(collab_scores.values())
        stress_branch_scores[type_name] = stress_action

        detail[type_name] = {
            "monarch_raw": monarch_behavior,
            "monarch_axis": role_legality,
            "monarch_axis_centered": role_legality - 50.0,
            "monarch_behavior": monarch_behavior,
            "adviser": adviser_legality_fit,
            "adviser_behavior": adviser_behavior,
            "adviser_suppression_fit": adviser_legality_fit,
            "illegal_high": illegal_high,
            "monarch_marshal": behavior_scores[marshal],
            "chancellor": chancellor_action,
            "chancellor_behavior": behavior_scores[chancellor],
            "chancellor_centered": chancellor_action - mean(collab_scores.values()),
            "chancellor_collab_key": collab_key,
            "stress_collab_key": stress_key,
            "stress_collab_score": stress_action,
            "domain_fit": domain_fit,
            "domain_monarch": domain_monarch,
            "domain_chancellor": domain_chancellor,
            "guard": guard_pct,
            "guard_behavior": behavior_scores[guard],
            "guard_centered": guard_pct - 50.0,
            "guard_score_raw": guard_score,
            "guard_score_total": guard_total,
            "guard_status": _guard_status(guard_score),
            "civilian": civilian_pressure_fit,
            "civilian_behavior": civilian_behavior,
            "civilian_fit": civilian_pressure_fit,
            "civilian_positive": behavior_scores[civilian],
            "civilian_aversion": civilian_pressure_fit,
            "latent_civilian": behavior_scores[civilian],
            "emperor": behavior_scores[emperor],
            "emperor_behavior": behavior_scores[emperor],
            "emperor_centered": behavior_scores[emperor] - 50.0,
            "emperor_high_key": "",
            "high_hits": 0,
            "marshal": behavior_scores[marshal],
            "marshal_behavior": behavior_scores[marshal],
            "branch_score": branch_scores[type_name],
            "branch_score_centered": branch_scores_centered[type_name],
            "hierarchy_score": 0.0,
            "hierarchy_bonus": 0.0,
            "core_type_score": score,
            "core_type_score_centered": 0.0,
            "role_axis_bonus": 0.0,
            "monarch_rank_penalty": illegal_high,
            "adviser_legality_fit": adviser_legality_fit,
            "strategist": strategist,
            "strategist_behavior": behavior_scores[strategist],
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
    level = "未知"
    variant_risk = _variant_risk(guard_score)
    road = "未知"
    ending = "未知"
    near_types = [t for t in ordered_types[1:] if top_score - type_scores[t] <= 5.0]
    near_cross_monarch_types = [t for t in near_types if TYPE_MAP[t]["monarch"] != top_monarch]

    risks = []
    if d.get("monarch_behavior", 0) < 75:
        risks.append({"title": "君主轴不够明显", "body": "当前候选的君主行为轴没有拉开到很高，主型可能需要更多样本题确认。"})
    if d.get("civilian_behavior", 0) >= 50:
        risks.append({"title": "子民位不够低", "body": "当前候选的子民行为轴没有明显压低，说明压力位可能尚未拉开，或主型存在近邻误差。"})
    adviser_behavior = d.get("adviser_behavior", 50)
    monarch_behavior = d.get("monarch_behavior", 50)
    if adviser_behavior < 15:
        risks.append({"title": "谏臣偏低", "body": "谏臣是追问君主合法性的镜像位。偏低不必然否定主型，但可能说明合法性审查尚未显形。"})
    elif adviser_behavior >= monarch_behavior - 5 or adviser_behavior > 80:
        risks.append({"title": "谏臣偏高", "body": "谏臣接近或压过君主时，可能出现镜像反压、主型边界或高整合样本，需要结合宰相动作和四域再判断。"})
    if d.get("domain_monarch", 0) < 50:
        risks.append({"title": "君主域底色不支持", "body": "当前候选的君主所在四域底色不够强，说明这个君主可能只是单功能高分，而不是稳定主权。"})
    if d.get("stress_collab_score", 0) < 50:
        risks.append({"title": "压力协同不典型", "body": "压力中的协同方式没有明显落在当前候选的君主—护卫组合上，镜像类型或异型结构需要留意。"})
    if branch_gap < 5.0:
        risks.append({"title": "宰相动作近邻", "body": "同一君主下的两个候选宰相分差较小，说明动作偏好还不够稳定。"})
    if overall_gap < 5.0:
        risks.append({"title": "近邻类型分数很接近", "body": "前几名结构分差距较小，建议结合君主—子民轴、宰相动作、四域底色和压力协同一起看。"})
    if near_cross_monarch_types:
        risks.append({"title": "存在跨君主近邻候选", "body": "有不同君主的候选类型与当前结果接近，说明君主轴可能处在边界。"})
    if guard_score >= 6:
        risks.append({"title": "护卫强，存在异型风险", "body": "护卫维持机制分较高，说明你已经形成明显的保存、保险或隔离机制，外显气质可能被护卫改写。"})
    elif guard_score <= 2:
        risks.append({"title": "护卫偏低", "body": "护卫维持机制分较低，说明保存、稳定、防漂移或隔离机制尚未稳定成型。"})

    confidence = _confidence(overall_gap, monarch_gap, branch_gap, d.get("monarch_axis", 0), d.get("chancellor", 0), d.get("domain_fit", 0))

    return {
        "positions": positions,
        "principle_scores": principle_scores,
        "principle_order": principle_order,
        "domain_scores": domain_scores,
        "behavior_domain_scores": behavior_domain_scores,
        "direction_scores": direction_scores,
        "mixed_scores": mixed_scores,
        "behavior_scores": behavior_scores,
        "behavior_centered": behavior_centered,
        "collab_scores": collab_scores,
        "stress_scores": stress_scores,
        "high_pair_scores": {},
        "high_count": 0,
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
        "stress_branch_scores": stress_branch_scores,
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
    domain_order = "、".join(f"{k}({v:.1f})" for k, v in sorted(result.get("domain_scores", {}).items(), key=lambda item: item[1], reverse=True))
    collab_key = d.get("chancellor_collab_key", "")
    collab_label = COLLAB_NAMES.get(collab_key, collab_key)
    stress_key = d.get("stress_collab_key", "")
    stress_label = COLLAB_NAMES.get(stress_key, stress_key)

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
护卫表示你如何保护并维持自己的王国秩序。它不只是防御冲突，也包括保存成果、稳定边界、承接压力、过滤风险，防止君主—宰相的运转被外部压力、内部漂移或未处理的裂口打断。本次护卫维持机制为：**{result.get('guard_score', 0)}/{result.get('guard_total', 8)}，{result.get('guard_status', '')}**。压力中的君主—护卫协同为：**{stress_label}**。

**子民｜{m['civilian']}**  
子民表示压力更多从什么地方来。你的压力裂口更容易出现在 **{m['civilian']}（{ROLE_WORDS[m['civilian']]}）** 所代表的方向。这里的子民分是反向压力分：该功能行为轴越低，子民符合度越高。

**帝师｜{m['emperor']}**  
帝师表示你怎么解释自己的秩序。当前版本不再用题目直接测高位或双高，帝师主要由王国模板推出，并作为解释资源观察。

**元帅｜{m['marshal']}**  
元帅表示你最后的手段。它不是日常状态，而是在极端压力、王国秩序无法正常运转时，可能被调用出来的最后手段。

君主—子民行为轴前四为：**{axis_order}**。四域底色为：**{domain_order}**。{near_note}

本次结构分为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。v0.8.4 主型使用“君主—子民行为轴”“宰相动作偏好轴”“四域底色”和轻量“压力协同分”共同判断；第一部分只用于判断君主—子民主轴，不直接判定宰相、护卫、帝师或元帅强弱；高位暂不计分，统一显示为未知。
""".strip()
