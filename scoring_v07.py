# -*- coding: utf-8 -*-
from data_v07 import QUESTIONS, TYPE_MAP, FUNCTIONS, DOMAIN_OF, SAME_DOMAIN_MIRROR

ROLE_WORDS = {
    "Ti": "自洽、可理解、说得通",
    "Te": "建构、目的、责任和结果",
    "Ni": "涌现、压缩、方向和趋势",
    "Ne": "创生、可能、新入口",
    "Si": "守恒、稳定、延续",
    "Se": "在场、现实、现场处理",
    "Fi": "本真、底线、自我统一",
    "Fe": "关联、回应、关系成立",
}


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else 0.0


def centered(values):
    avg = mean(values.values())
    return {k: v - avg for k, v in values.items()}


def _clamp(value, low=0.0, high=100.0):
    return max(low, min(high, value))


def _option_for(q, key):
    for option in q.get("options", []):
        if option.get("key") == key:
            return option
    return None


def _rank_map(scores):
    ordered = sorted(scores, key=lambda f: scores[f], reverse=True)
    return {f: i + 1 for i, f in enumerate(ordered)}, ordered


def _role_axis_bonus(chancellor, emperor, principle_scores):
    if SAME_DOMAIN_MIRROR.get(chancellor) != emperor:
        return 0.0
    return max(0.0, min(principle_scores[chancellor], principle_scores[emperor]) - 60.0) * 0.16


def _monarch_rank_penalty(monarch, ranks):
    rank = ranks[monarch]
    if rank <= 4:
        return 0.0
    if rank == 5:
        return 12.0
    if rank == 6:
        return 22.0
    return 40.0


def _level_from_high_questions(high_count):
    if high_count >= 4:
        return "高位"
    if high_count >= 2:
        return "高位倾向"
    return "低位"


def _scale_to_score(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return _clamp((value - 1.0) / 4.0 * 100.0)


def compute_scores(answers):
    domains = ["T", "N", "S", "F"]
    domain_raw = {d: 0.0 for d in domains}
    domain_max = {d: 0.0 for d in domains}
    direction_raw = {f: 0.0 for f in FUNCTIONS}
    direction_max = {f: 0.0 for f in FUNCTIONS}
    mixed_raw = {f: 0.0 for f in FUNCTIONS}
    mixed_appearances = {f: 0.0 for f in FUNCTIONS}
    behavior_raw = {f: 0.0 for f in FUNCTIONS}
    behavior_max = {f: 0.0 for f in FUNCTIONS}
    behavior_values = {f: [] for f in FUNCTIONS}
    high_count = 0

    for q in QUESTIONS:
        qid = q["qid"]
        qtype = q.get("question_type")
        module_key = q.get("module_key")
        answer = answers.get(qid)

        if qtype == "pair":
            option = _option_for(q, answer) if answer else None

            if module_key == "B":
                for candidate in q.get("options", []):
                    for key in candidate.get("scores", {}):
                        if key in FUNCTIONS:
                            behavior_max[key] += 1
                if option:
                    for key, value in option.get("scores", {}).items():
                        if key in FUNCTIONS:
                            behavior_raw[key] += value
                continue

            for candidate in q.get("options", []):
                for key in candidate.get("scores", {}):
                    if key in domains:
                        domain_max[key] += 1
                    elif key in FUNCTIONS:
                        direction_max[key] += 1
            if option:
                for key, value in option.get("scores", {}).items():
                    if key in domains:
                        domain_raw[key] += value
                    elif key in FUNCTIONS:
                        direction_raw[key] += value
                    elif key == "high":
                        high_count += int(value)

        elif qtype == "best_worst":
            for option in q.get("options", []):
                principle = option.get("principle")
                if principle in FUNCTIONS:
                    mixed_appearances[principle] += 1
            if isinstance(answer, dict):
                best_option = _option_for(q, answer.get("best")) if answer.get("best") else None
                worst_option = _option_for(q, answer.get("worst")) if answer.get("worst") else None
                if best_option and best_option.get("principle") in FUNCTIONS:
                    mixed_raw[best_option["principle"]] += 2
                if worst_option and worst_option.get("principle") in FUNCTIONS:
                    mixed_raw[worst_option["principle"]] -= 1

        elif qtype == "scale":
            score = _scale_to_score(answer)
            if score is not None:
                for f in q.get("scores", {}):
                    if f in FUNCTIONS:
                        behavior_values[f].append(score)

    domain_scores = {}
    for d in domains:
        max_count = domain_max[d] or 1
        domain_scores[d] = _clamp(50 + (domain_raw[d] - max_count / 2) * (60 / max_count), 20, 80)

    direction_scores = {}
    for f in FUNCTIONS:
        max_count = direction_max[f]
        direction_scores[f] = (direction_raw[f] / max_count * 100) if max_count else 50.0

    mixed_scores = {}
    for f in FUNCTIONS:
        app = mixed_appearances[f]
        mixed_scores[f] = ((mixed_raw[f] + app) / (3 * app) * 100) if app else 50.0
        mixed_scores[f] = _clamp(mixed_scores[f])

    behavior_scores = {}
    for f in FUNCTIONS:
        if behavior_max[f]:
            behavior_scores[f] = behavior_raw[f] / behavior_max[f] * 100
        elif behavior_values[f]:
            behavior_scores[f] = mean(behavior_values[f])
        else:
            behavior_scores[f] = 50.0
    behavior_centered = centered(behavior_scores)

    principle_base = {}
    principle_scores = {}
    for f in FUNCTIONS:
        domain = DOMAIN_OF[f]
        principle_base[f] = 0.75 * domain_scores[domain] + 0.25 * direction_scores[f]
        principle_scores[f] = 0.70 * principle_base[f] + 0.30 * mixed_scores[f]

    principle_centered = centered(principle_scores)
    ranks, principle_order = _rank_map(principle_scores)

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

    for type_name, m in TYPE_MAP.items():
        monarch = m["monarch"]
        chancellor = m["chancellor"]
        guard = m["guard"]
        civilian = m["civilian"]
        emperor = m["emperor"]
        marshal = m["marshal"]
        adviser = SAME_DOMAIN_MIRROR[monarch]
        strategist = SAME_DOMAIN_MIRROR[guard]

        civilian_fit = 100 - behavior_scores[civilian]
        role_axis_bonus = _role_axis_bonus(chancellor, emperor, principle_scores)
        rank_penalty = _monarch_rank_penalty(monarch, ranks)

        score = (
            0.30 * principle_scores[monarch]
            + 0.16 * principle_scores[chancellor]
            + 0.10 * behavior_scores[chancellor]
            + 0.10 * behavior_scores[guard]
            + 0.12 * principle_scores[emperor]
            + 0.08 * civilian_fit
            + 0.06 * principle_scores[adviser]
            + 0.04 * behavior_scores[strategist]
            + 0.04 * principle_scores[marshal]
            + role_axis_bonus
            - rank_penalty
        )
        type_scores[type_name] = score
        branch_scores[type_name] = 0.45 * principle_scores[chancellor] + 0.35 * behavior_scores[chancellor] + 0.20 * behavior_scores[guard]
        branch_scores_centered[type_name] = 0.45 * principle_centered[chancellor] + 0.35 * behavior_centered[chancellor] + 0.20 * behavior_centered[guard]

        detail[type_name] = {
            "monarch_raw": principle_scores[monarch],
            "monarch_axis": principle_scores[monarch],
            "monarch_axis_centered": principle_centered[monarch],
            "monarch_behavior": behavior_scores[monarch],
            "monarch_marshal": principle_scores[marshal],
            "chancellor": principle_scores[chancellor],
            "chancellor_behavior": behavior_scores[chancellor],
            "chancellor_centered": principle_centered[chancellor],
            "guard": principle_scores[guard],
            "guard_behavior": behavior_scores[guard],
            "guard_centered": principle_centered[guard],
            "civilian": principle_scores[civilian],
            "civilian_behavior": behavior_scores[civilian],
            "civilian_fit": civilian_fit,
            "civilian_positive": principle_scores[civilian],
            "civilian_aversion": 100 - principle_scores[civilian],
            "latent_civilian": principle_scores[civilian],
            "emperor": principle_scores[emperor],
            "emperor_behavior": behavior_scores[emperor],
            "emperor_centered": principle_centered[emperor],
            "marshal": principle_scores[marshal],
            "marshal_behavior": behavior_scores[marshal],
            "branch_score": branch_scores[type_name],
            "branch_score_centered": branch_scores_centered[type_name],
            "core_type_score": score,
            "core_type_score_centered": 0.0,
            "role_axis_bonus": role_axis_bonus,
            "monarch_rank_penalty": rank_penalty,
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
    level = _level_from_high_questions(high_count)
    near_types = [t for t in ordered_types[1:] if top_score - type_scores[t] <= 4.0]
    near_cross_monarch_types = [t for t in near_types if TYPE_MAP[t]["monarch"] != top_monarch]

    risks = []
    if ranks[top_monarch] > 4:
        risks.append({"title": "君主原则不在前列", "body": "当前最高候选的君主原则没有排进前四，说明结果可能被宰相、帝师或护卫等强位抬高，需要谨慎理解。"})
    if overall_gap < 2.5:
        risks.append({"title": "近邻类型分数很接近", "body": "前几名王国模板分差距很小，建议结合八原则分、行为可用分和王国位次一起看。"})
    if near_cross_monarch_types:
        risks.append({"title": "存在跨君主近邻候选", "body": "有不同君主的候选类型与当前结果接近，说明结构可能处在相邻王国边界。"})
    if d.get("civilian_behavior", 50) >= 70:
        risks.append({"title": "子民行为可用性偏高", "body": "当前候选的子民位行为可用分偏高，可能说明该类型并非最稳，或该子民位已经高度整合。"})

    if overall_gap >= 5.0 and ranks[top_monarch] <= 3:
        confidence = "高"
    elif overall_gap >= 2.5 and ranks[top_monarch] <= 4:
        confidence = "中"
    else:
        confidence = "低"

    return {
        "positions": positions,
        "principle_scores": principle_scores,
        "principle_order": principle_order,
        "domain_scores": domain_scores,
        "direction_scores": direction_scores,
        "mixed_scores": mixed_scores,
        "behavior_scores": behavior_scores,
        "behavior_centered": behavior_centered,
        "high_count": high_count,
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
    level = result["level"]
    m = result["map"]
    d = result["detail"][t]
    near_types = result.get("near_types", [])[:3]
    near_note = f"\n\n近邻候选包括：**{'、'.join(near_types)}**。" if near_types else ""
    top_principles = "、".join(f"{f}({result['principle_scores'][f]:.1f})" for f in result.get("principle_order", [])[:4])

    return f"""
这次结果显示，你当前最接近：**{level} {t}**。

整体来看，{_chain_sentence(m['monarch'], m['chancellor'], m['guard'], m['civilian'], m['emperor'], m['marshal'])}

八原则前四为：**{top_principles}**。{near_note}

本次王国模板分为 **{d['score']:.2f}**，置信度为 **{result['confidence']}**。v0.7.3 同时使用“原则偏好分”和“君主—子民轴行为分”：原则题主要判断王国核心，行为轴题主要帮助区分子民、护卫和宰相，避免把子民压力误当成稳定能力。
""".strip()
