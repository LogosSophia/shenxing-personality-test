# -*- coding: utf-8 -*-
import uuid

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from data_v07 import (
    QUESTIONS,
    TYPE_MAP,
    PRINCIPLES,
    SAME_DOMAIN_MIRROR,
    DOMAIN_NAMES,
    COLLAB_NAMES,
    HIGH_PAIR_NAMES,
)
from scoring_v07 import compute_scores, build_report
from backend_v07 import build_submission_row, save_submission

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
    qtype = q.get("question_type")
    if qtype == "pair":
        return answer in ["A", "B"]
    if qtype == "single_choice":
        return answer in [option.get("key") for option in q.get("options", [])]
    if qtype == "best_worst":
        return isinstance(answer, dict) and answer.get("best") and answer.get("worst") and answer.get("best") != answer.get("worst")
    if qtype == "scale":
        return isinstance(answer, int) and 1 <= answer <= 5
    return answer is not None


def _sync_widget_answers():
    store = st.session_state["answers"]
    for q in QUESTIONS:
        qid = q["qid"]
        qtype = q.get("question_type")
        if qtype in ["pair", "single_choice", "scale"]:
            widget_key = _answer_key(qid)
            if widget_key in st.session_state:
                store[qid] = st.session_state.get(widget_key)
        elif qtype == "best_worst":
            best_key = _answer_key(qid, "_best")
            worst_key = _answer_key(qid, "_worst")
            if best_key in st.session_state or worst_key in st.session_state:
                store[qid] = {"best": st.session_state.get(best_key), "worst": st.session_state.get(worst_key)}


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
    behavior = result.get("behavior_scores", {})
    return [
        {"王国位次": "君主", "含义": "以什么方式认识世界", "功能": m["monarch"], "关键词": PRINCIPLES[m["monarch"]], "主判来源": "君主—子民互斥轴", "分数": round(d.get("monarch_behavior", 0), 2), "补充": "自然发动的一端；其反面为子民"},
        {"王国位次": "宰相", "含义": "最顺的组织方式", "功能": m["chancellor"], "关键词": PRINCIPLES[m["chancellor"]], "主判来源": COLLAB_NAMES.get(d.get("chancellor_collab_key", ""), "宰相动作"), "分数": round(d.get("chancellor", 0), 2), "补充": "君主确定后最自然的动作通道"},
        {"王国位次": "护卫", "含义": "保护并维持王国秩序", "功能": m["guard"], "关键词": PRINCIPLES[m["guard"]], "主判来源": "由主型推出；护卫题只测维持机制强度", "分数": f"{result.get('guard_score', 0)}/{result.get('guard_total', 8)}", "补充": result.get("guard_status", "")},
        {"王国位次": "子民", "含义": "压力更多从什么地方来", "功能": m["civilian"], "关键词": PRINCIPLES[m["civilian"]], "主判来源": "君主反面", "分数": round(100 - behavior.get(m["civilian"], 50), 2), "补充": "行为轴越低，越符合子民压力位"},
        {"王国位次": "谏臣", "含义": "君主镜像 / 提醒位", "功能": adviser, "关键词": PRINCIPLES[adviser], "主判来源": "君主镜像", "分数": round(behavior.get(adviser, 0), 2), "补充": "由君主镜像推定"},
        {"王国位次": "帝师", "含义": "怎么解释自己的秩序", "功能": m["emperor"], "关键词": PRINCIPLES[m["emperor"]], "主判来源": HIGH_PAIR_NAMES.get(d.get("emperor_high_key", ""), "双高协同"), "分数": f"{d.get('high_hits', 0)}/4", "补充": f"{result['level']}；双高题参与高位链条容错"},
        {"王国位次": "谋士", "含义": "护卫镜像 / 隐性策略位", "功能": strategist, "关键词": PRINCIPLES[strategist], "主判来源": "护卫镜像", "分数": round(behavior.get(strategist, 0), 2), "补充": "由护卫镜像推定"},
        {"王国位次": "元帅", "含义": "最后的手段", "功能": m["marshal"], "关键词": PRINCIPLES[m["marshal"]], "主判来源": "王国模板", "分数": round(behavior.get(m["marshal"], 0), 2), "补充": "由王国模板推出，不直接询问极端反应"},
    ]


def _go_to_section(index: int):
    _sync_widget_answers()
    st.session_state["current_section_index"] = max(0, min(index, len(sections) - 1))
    st.session_state["scroll_to_questionnaire_top"] = True
    st.rerun()


_sync_widget_answers()

st.title("神性论人格王国测评 v0.8")
st.caption("结构版｜君主—子民轴 + 宰相动作轴 + 四域容错｜非医学、非心理诊断")

with st.expander("测评说明", expanded=True):
    st.markdown("""
本版直接测结构位置，同时保留域级容错：

1. **君主—子民互斥行为轴**：判断你自然从哪里发动，以及哪一端更像压力位。  
2. **宰相动作偏好轴**：判断君主确定之后，你最自然进入哪一种协作动作。  
3. **双高协同题**：判断宰相—帝师是否双高，并参与高位链条容错。  
4. **四域底色题**：判断 T/N/S/F 哪个域整体更活，防止单功能误判。  
5. **护卫维持机制题**：判断保存、保险、防漂移、稳定边界等护卫机制强度。  
6. **压力协同题**：轻量判断压力下的君主—护卫协同，防止把低分功能直接等同为子民。
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
if current_section.startswith("第一部分"):
    st.info("这一部分只问自然行为轴，不要按理想中的自己作答；选你平时更自然靠近哪一端。")
if current_section.startswith("第二部分"):
    st.info("这一部分问动作偏好：当你已经认定一件事重要后，下一步自然怎么做。四个选项对应四种协作通道。")
if current_section.startswith("第三部分"):
    st.info("这一部分判断宰相—帝师是否双高，会用于高位链条容错。")
if current_section.startswith("第四部分"):
    st.info("这一部分是四域底色题，只判断 T/N/S/F 哪个域整体更活，用来增加容错。")
if current_section.startswith("第五部分"):
    st.info("这一部分判断护卫维持机制：保存、保险、防漂移、稳定边界。每题符合记 1 分；护卫是谁由主型推出。")
if current_section.startswith("第六部分"):
    st.info("这一部分判断压力中的君主—护卫协同，避免把低分功能直接等同为子民。")

for q in questions_by_section[current_section]:
    qid = q["qid"]
    st.markdown(f"**{qid}. {q['front_text']}**")
    stored = st.session_state["answers"].get(qid)
    options = q.get("options", [])
    qtype = q.get("question_type")

    if qtype in ["pair", "single_choice"]:
        labels = [_option_label(option) for option in options]
        keys = [option["key"] for option in options]
        selected = st.radio("选择更接近你的一个：", options=keys, index=keys.index(stored) if stored in keys else None, format_func=lambda key: labels[keys.index(key)], key=_answer_key(qid))
        st.session_state["answers"][qid] = selected

    elif qtype == "best_worst":
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

    elif qtype == "scale":
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
    st.download_button("导出题库 CSV", data=question_df.to_csv(index=False).encode("utf-8-sig"), file_name="神性论人格王国测评题库_v0.8.csv", mime="text/csv")

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
        st.error(f"还有 {len(missing)} 题未作答。请完成全部题目后再生成结果。")
        with st.expander("查看未完成题号"):
            st.write("、".join(missing))
        st.stop()

    result = compute_scores(answers)
    report = build_report(result)
    submission_row = build_submission_row(answers=answers, result=result, mbti_past=mbti_past, mbti_self=mbti_self, submission_id=st.session_state["submission_id"])
    save_status = save_submission(submission_row)

    st.divider()
    st.header(f"人格王国：{result['top_type']}")
    summary_cols = st.columns(4)
    summary_cols[0].metric("位阶", result.get("level", "未知"))
    summary_cols[1].metric("异型风险", result.get("variant_risk", "低"))
    summary_cols[2].metric("道路", result.get("road", "未知"))
    summary_cols[3].metric("终局", result.get("ending", "未知"))

    st.subheader("人格王国位次与分数")
    st.dataframe(pd.DataFrame(_kingdom_role_rows(result)), use_container_width=True, hide_index=True)

    st.subheader("君主—子民行为轴")
    axis_rows = []
    for f in result.get("principle_order", []):
        p = result["positions"][f]
        axis_rows.append({"排名": int(p["Rank"]), "功能": f, "关键词": PRINCIPLES[f], "行为轴分": round(p["BehaviorScore"], 2), "四域": DOMAIN_NAMES[p["Domain"]]})
    st.dataframe(pd.DataFrame(axis_rows), use_container_width=True, hide_index=True)

    st.subheader("宰相动作、双高、四域与护卫")
    collab_rows = [{"协作通道": k, "名称": COLLAB_NAMES[k], "分数": round(v, 2)} for k, v in result.get("collab_scores", {}).items()]
    st.dataframe(pd.DataFrame(collab_rows), use_container_width=True, hide_index=True)
    high_rows = [{"双高项": k, "名称": HIGH_PAIR_NAMES[k], "命中率": round(v, 2)} for k, v in result.get("high_pair_scores", {}).items()]
    st.dataframe(pd.DataFrame(high_rows), use_container_width=True, hide_index=True)
    domain_rows = [{"四域": k, "名称": DOMAIN_NAMES[k], "分数": round(v, 2)} for k, v in result.get("domain_scores", {}).items()]
    st.dataframe(pd.DataFrame(domain_rows), use_container_width=True, hide_index=True)
    st.caption(f"护卫维持机制：{result.get('guard_score', 0)}/{result.get('guard_total', 8)}｜{result.get('guard_status', '')}")

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
            candidate_rows.append({
                "类型": candidate_type,
                "结构分": round(display_score, 3),
                "君主": TYPE_MAP[candidate_type]["monarch"],
                "君主轴分": round(cd.get("monarch_behavior", 0), 3),
                "宰相": TYPE_MAP[candidate_type]["chancellor"],
                "动作通道": cd.get("chancellor_collab_key", ""),
                "宰相动作分": round(cd.get("chancellor", 0), 3),
                "四域支持": round(cd.get("domain_fit", 0), 3),
                "压力协同": cd.get("stress_collab_key", ""),
                "压力协同分": round(cd.get("stress_collab_score", 0), 3),
                "护卫": TYPE_MAP[candidate_type]["guard"],
                "护卫分": f"{cd.get('guard_score_raw', 0)}/{cd.get('guard_score_total', 8)}",
                "子民": TYPE_MAP[candidate_type]["civilian"],
                "子民行为轴分": round(cd.get("civilian_behavior", 0), 3),
                "双高命中": f"{cd.get('high_hits', 0)}/4",
            })
        st.dataframe(pd.DataFrame(candidate_rows), use_container_width=True, hide_index=True)
