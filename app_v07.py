# -*- coding: utf-8 -*-
import uuid

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from data_v07 import QUESTIONS, TYPE_MAP, PRINCIPLES, SAME_DOMAIN_MIRROR, DOMAIN_NAMES
from scoring_v07 import compute_scores, build_report
from backend import build_submission_row, save_submission

st.set_page_config(page_title="神性论人格王国测评", page_icon="👑", layout="wide")

ANSWER_KEY_PREFIX = "answer_"
SCALE_LABELS = {1: "完全不像我", 2: "比较不像", 3: "说不清", 4: "比较像", 5: "很像我"}

if "submission_id" not in st.session_state:
    st.session_state["submission_id"] = str(uuid.uuid4())
if "current_section_index" not in st.session_state:
    st.session_state["current_section_index"] = 0
if "scroll_to_questionnaire_top" not in st.session_state:
    st.session_state["scroll_to_questionnaire_top"] = False
if "answers" not in st.session_state:
    st.session_state["answers"] = {}

for q in QUESTIONS:
    st.session_state["answers"].setdefault(q["qid"], None)


def _answer_key(qid: str, suffix: str = "") -> str:
    return f"{ANSWER_KEY_PREFIX}{qid}{suffix}"


def _is_answered(q, answer):
    if q.get("question_type") == "pair":
        return answer in ["A", "B"]
    if q.get("question_type") == "best_worst":
        return isinstance(answer, dict) and answer.get("best") and answer.get("worst") and answer.get("best") != answer.get("worst")
    if q.get("question_type") == "scale":
        return isinstance(answer, int) and 1 <= answer <= 5
    return answer is not None


def _sync_widget_answers():
    store = st.session_state["answers"]
    for q in QUESTIONS:
        qid = q["qid"]
        if q.get("question_type") == "pair":
            widget_key = _answer_key(qid)
            if widget_key in st.session_state:
                store[qid] = st.session_state.get(widget_key)
        elif q.get("question_type") == "best_worst":
            best_key = _answer_key(qid, "_best")
            worst_key = _answer_key(qid, "_worst")
            if best_key in st.session_state or worst_key in st.session_state:
                store[qid] = {"best": st.session_state.get(best_key), "worst": st.session_state.get(worst_key)}
        elif q.get("question_type") == "scale":
            widget_key = _answer_key(qid)
            if widget_key in st.session_state:
                store[qid] = st.session_state.get(widget_key)


def _short_section_name(section: str) -> str:
    return section.split("：", 1)[1] if "：" in section else section


def _option_label(option):
    return f"{option['key']}. {option['text']}"


def _mixed_labels(q):
    mode = q.get("mode", "priority")
    if mode == "failure":
        return "最不能接受：", "相对还能忍受："
    if mode == "appeal":
        return "最打动：", "相对最不打动："
    return "最优先保住：", "相对可以先放一放："


def _kingdom_role_rows(result):
    m = result["map"]
    d = result["detail"][result["top_type"]]
    adviser = SAME_DOMAIN_MIRROR[m["monarch"]]
    strategist = SAME_DOMAIN_MIRROR[m["guard"]]
    scores = result.get("principle_scores", {})
    behavior = result.get("behavior_scores", {})
    return [
        {"王国位次": "君主", "结构面向": "核心原则", "功能": m["monarch"], "关键词": PRINCIPLES[m["monarch"]], "原则分": round(scores.get(m["monarch"], d.get("monarch_raw", 0)), 2), "行为分": round(behavior.get(m["monarch"], 0), 2), "补充": "君主主要看原则分是否在前列"},
        {"王国位次": "宰相", "结构面向": "施政原则", "功能": m["chancellor"], "关键词": PRINCIPLES[m["chancellor"]], "原则分": round(d["chancellor"], 2), "行为分": round(d.get("chancellor_behavior", behavior.get(m["chancellor"], 0)), 2), "补充": "宰相需兼看原则偏好与行为可用"},
        {"王国位次": "护卫", "结构面向": "稳定/守门", "功能": m["guard"], "关键词": PRINCIPLES[m["guard"]], "原则分": round(d["guard"], 2), "行为分": round(d.get("guard_behavior", behavior.get(m["guard"], 0)), 2), "补充": "护卫更看自然行为可用性"},
        {"王国位次": "子民", "结构面向": "反面压力", "功能": m["civilian"], "关键词": PRINCIPLES[m["civilian"]], "原则分": round(d["civilian"], 2), "行为分": round(d.get("civilian_behavior", behavior.get(m["civilian"], 0)), 2), "补充": "子民压力可能抬高原则分；行为分低更符合子民位"},
        {"王国位次": "谏臣", "结构面向": "君主镜像 / 提醒位", "功能": adviser, "关键词": PRINCIPLES[adviser], "原则分": round(scores.get(adviser, 0), 2), "行为分": round(behavior.get(adviser, 0), 2), "补充": "由君主镜像推定"},
        {"王国位次": "帝师", "结构面向": f"解释方式 / {result['level']}", "功能": m["emperor"], "关键词": PRINCIPLES[m["emperor"]], "原则分": round(d["emperor"], 2), "行为分": round(d.get("emperor_behavior", behavior.get(m["emperor"], 0)), 2), "补充": f"高低位辅助题 B 数：{result.get('high_count', 0)}"},
        {"王国位次": "谋士", "结构面向": "护卫镜像 / 隐性策略位", "功能": strategist, "关键词": PRINCIPLES[strategist], "原则分": round(scores.get(strategist, 0), 2), "行为分": round(behavior.get(strategist, 0), 2), "补充": "由护卫镜像推定"},
        {"王国位次": "元帅", "结构面向": "极限手段", "功能": m["marshal"], "关键词": PRINCIPLES[m["marshal"]], "原则分": round(d["marshal"], 2), "行为分": round(d.get("marshal_behavior", behavior.get(m["marshal"], 0)), 2), "补充": "由王国模板推出，不直接询问极端反应"},
    ]


def _go_to_section(index: int):
    _sync_widget_answers()
    st.session_state["current_section_index"] = max(0, min(index, len(sections) - 1))
    st.session_state["scroll_to_questionnaire_top"] = True
    st.rerun()


_sync_widget_answers()

st.title("神性论人格王国测评 v0.7")
st.caption("八大结构原则取舍版｜非医学、非心理诊断")

with st.expander("测评说明", expanded=True):
    st.markdown("""
本版从八大结构原则出发，但新增了“自然行为事实题”。

原则题主要判断你认为世界怎样才成立；行为事实题主要看某个原则在日常里是否自然可用，尤其用于区分子民位压力和真正稳定能力。
""")

sections = []
for q in QUESTIONS:
    if q["module"] not in sections:
        sections.append(q["module"])
questions_by_section = {section: [q for q in QUESTIONS if q["module"] == section] for section in sections}

st.markdown('<span id="questionnaire-top"></span>', unsafe_allow_html=True)
if st.session_state.get("scroll_to_questionnaire_top"):
    st.session_state["scroll_to_questionnaire_top"] = False
    components.html("""
        <script>
        function scrollToQuestionnaireTop() {
            try {
                const doc = window.parent.document;
                const target = doc.getElementById('questionnaire-top');
                if (target) target.scrollIntoView({behavior: 'auto', block: 'start'});
            } catch(e) {}
        }
        setTimeout(scrollToQuestionnaireTop, 50);
        setTimeout(scrollToQuestionnaireTop, 200);
        </script>
        """, height=0)

st.divider()
st.subheader("开始作答")

current_idx = max(0, min(st.session_state["current_section_index"], len(sections) - 1))
st.session_state["current_section_index"] = current_idx
current_section = sections[current_idx]

nav_cols = st.columns(len(sections))
for i, section in enumerate(sections):
    label = f"{i + 1}. {_short_section_name(section)}"
    if i == current_idx:
        nav_cols[i].button(label, disabled=True, use_container_width=True, key=f"nav_current_{i}")
    elif nav_cols[i].button(label, use_container_width=True, key=f"nav_top_{i}"):
        _go_to_section(i)

st.markdown(f"### {current_idx + 1}/{len(sections)}　{current_section}")
if current_section.startswith("第三部分"):
    st.info("每题需要选两个，且不能相同。一个代表最优先，另一个代表相对可以先放一放。")
if current_section.startswith("第四部分"):
    st.info("这一部分只问日常事实，不要按理想中的自己作答；选你平时自然会不会这样。")

for q in questions_by_section[current_section]:
    qid = q["qid"]
    st.markdown(f"**{qid}. {q['front_text']}**")
    stored = st.session_state["answers"].get(qid)
    options = q.get("options", [])

    if q.get("question_type") == "pair":
        labels = [_option_label(option) for option in options]
        keys = [option["key"] for option in options]
        selected = st.radio("选择更接近你的一个：", options=keys, index=keys.index(stored) if stored in keys else None, format_func=lambda key: labels[keys.index(key)], key=_answer_key(qid))
        st.session_state["answers"][qid] = selected

    elif q.get("question_type") == "best_worst":
        keys = [option["key"] for option in options]
        labels = [_option_label(option) for option in options]
        stored = stored if isinstance(stored, dict) else {}
        best_label, worst_label = _mixed_labels(q)
        col_best, col_worst = st.columns(2)
        with col_best:
            best = st.radio(best_label, options=keys, index=keys.index(stored.get("best")) if stored.get("best") in keys else None, format_func=lambda key: labels[keys.index(key)], key=_answer_key(qid, "_best"))
        with col_worst:
            worst = st.radio(worst_label, options=keys, index=keys.index(stored.get("worst")) if stored.get("worst") in keys else None, format_func=lambda key: labels[keys.index(key)], key=_answer_key(qid, "_worst"))
        st.session_state["answers"][qid] = {"best": best, "worst": worst}
        if best and worst and best == worst:
            st.warning("这一题的两个选择不能相同。")

    elif q.get("question_type") == "scale":
        scale_options = [1, 2, 3, 4, 5]
        selected = st.radio("这句话有多像你的日常事实？", options=scale_options, index=scale_options.index(stored) if stored in scale_options else None, format_func=lambda x: f"{x}｜{SCALE_LABELS[x]}", key=_answer_key(qid), horizontal=True)
        st.session_state["answers"][qid] = selected
    st.write("")

section_answered_count = sum(1 for q in questions_by_section[current_section] if _is_answered(q, st.session_state["answers"].get(q["qid"])))
section_total_count = len(questions_by_section[current_section])
st.caption(f"本部分已作答 {section_answered_count}/{section_total_count} 题")

prev_col, progress_col, next_col = st.columns([1, 2, 1])
with prev_col:
    if current_idx > 0:
        if st.button("上一页", use_container_width=True):
            _go_to_section(current_idx - 1)
    else:
        st.button("上一页", disabled=True, use_container_width=True)
with next_col:
    if current_idx < len(sections) - 1:
        if st.button("下一页", type="primary", use_container_width=True):
            _go_to_section(current_idx + 1)
    else:
        st.button("已到最后一部分", disabled=True, use_container_width=True)

answered_count = sum(1 for q in QUESTIONS if _is_answered(q, st.session_state["answers"].get(q["qid"])))
total_count = len(QUESTIONS)
with progress_col:
    st.progress(answered_count / total_count, text=f"总进度 {answered_count}/{total_count} 题")

with st.expander("题库导出", expanded=False):
    rows = []
    for q in QUESTIONS:
        option_text = " / ".join(_option_label(option) for option in q.get("options", [])) if q.get("options") else "1—5：完全不像我—很像我"
        rows.append({"题号": q["qid"], "部分": q["module"], "题型": q["question_type"], "题目": q["front_text"], "选项": option_text})
    question_df = pd.DataFrame(rows)
    st.download_button("导出题库 CSV", data=question_df.to_csv(index=False).encode("utf-8-sig"), file_name="神性论人格王国测评题库_v0.7.csv", mime="text/csv")

st.divider()
st.subheader("非计分对照题")
col1, col2 = st.columns(2)
with col1:
    mbti_past = st.text_input("你过往最常测出的 MBTI 类型是？", placeholder="例如 INTJ")
with col2:
    mbti_self = st.text_input("你自认为最接近的 MBTI 类型是？", placeholder="例如 INTJ")

if st.button("生成测评结果", type="primary"):
    _sync_widget_answers()
    answers = dict(st.session_state["answers"])
    missing = [q["qid"] for q in QUESTIONS if not _is_answered(q, answers.get(q["qid"]))]
    if missing:
        st.error(f"还有 {len(missing)} 题未作答或混战题两个选择相同。请完成全部题目后再生成结果。")
        with st.expander("查看未完成题号"):
            st.write("、".join(missing))
        st.stop()

    result = compute_scores(answers)
    report = build_report(result)
    submission_row = build_submission_row(answers=answers, result=result, mbti_past=mbti_past, mbti_self=mbti_self, submission_id=st.session_state["submission_id"])
    save_status = save_submission(submission_row)

    st.divider()
    st.header(f"{result['level']} {result['top_type']}")
    st.subheader("人格王国位次与分数")
    st.dataframe(pd.DataFrame(_kingdom_role_rows(result)), use_container_width=True, hide_index=True)

    st.subheader("八原则分与行为可用分")
    principle_rows = []
    for f in result.get("principle_order", []):
        p = result["positions"][f]
        principle_rows.append({"排名": int(p["Rank"]), "原则": f, "关键词": PRINCIPLES[f], "原则分": round(p["PrincipleScore"], 2), "行为分": round(p["BehaviorScore"], 2), "四域": DOMAIN_NAMES[p["Domain"]], "四域分": round(p["DomainScore"], 2), "域内分": round(p["DirectionScore"], 2), "混战分": round(p["MixedScore"], 2)})
    st.dataframe(pd.DataFrame(principle_rows), use_container_width=True, hide_index=True)

    st.subheader("报告说明")
    st.markdown(report)

    if save_status["ok"] and save_status["backend"] == "google_sheets":
        st.caption("答卷已记录。")

    if result["risks"]:
        st.subheader("补充提示")
        for risk in result["risks"]:
            st.warning(f"**{risk['title']}**\n\n{risk['body']}")

    if mbti_past or mbti_self:
        st.info(f"对照信息：过往常测 MBTI：{mbti_past or '未填写'}；自认为接近：{mbti_self or '未填写'}。")

    with st.expander("查看详细数据（可选）"):
        st.subheader("候选类型")
        candidate_rows = []
        for candidate_type, display_score in result["ordered_types"]:
            cd = result["detail"][candidate_type]
            candidate_rows.append({"类型": candidate_type, "王国模板分": round(display_score, 3), "君主": TYPE_MAP[candidate_type]["monarch"], "君主原则分": round(cd["monarch_raw"], 3), "宰相": TYPE_MAP[candidate_type]["chancellor"], "宰相行为分": round(cd.get("chancellor_behavior", 0), 3), "护卫": TYPE_MAP[candidate_type]["guard"], "护卫行为分": round(cd.get("guard_behavior", 0), 3), "子民": TYPE_MAP[candidate_type]["civilian"], "子民行为分": round(cd.get("civilian_behavior", 0), 3), "君主排名惩罚": round(cd.get("monarch_rank_penalty", 0), 3)})
        st.dataframe(pd.DataFrame(candidate_rows), use_container_width=True, hide_index=True)

        st.subheader("四域分")
        st.dataframe(pd.DataFrame([{"四域": k, "名称": DOMAIN_NAMES[k], "分数": round(v, 3)} for k, v in result.get("domain_scores", {}).items()]), use_container_width=True, hide_index=True)
