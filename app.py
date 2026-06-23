# -*- coding: utf-8 -*-
import random
import uuid

import streamlit as st
import pandas as pd

from data import QUESTIONS, TYPE_MAP, PRINCIPLES
from scoring import compute_scores, build_report
from backend import build_submission_row, save_submission

st.set_page_config(page_title="神性论人格王国测评", page_icon="👑", layout="wide")

if "submission_id" not in st.session_state:
    st.session_state["submission_id"] = str(uuid.uuid4())
if "shuffle_seed" not in st.session_state:
    st.session_state["shuffle_seed"] = str(uuid.uuid4())

st.title("神性论人格王国测评")
st.caption("人格结构研究与自我理解工具｜非医学、非心理诊断")

with st.expander("测评说明", expanded=True):
    st.markdown("""
本测评用于观察一个人的核心判断方式、做事方式、稳定方式、解释方式和极端反应。  
它不是医学或心理诊断，也不判断人生高低、成败或好坏。

作答说明：

- 1 = 完全不符合
- 2 = 不太符合
- 3 = 说不清 / 一半一半
- 4 = 比较符合
- 5 = 非常符合

第一部分会同时询问你自然喜欢、认可的东西，以及你最不喜欢被迫面对的状态。请尽量按真实经验作答，不需要选择“更好看”的答案。

生成结果时，系统会默认记录本次匿名答卷与计算结果，用于后续题库校准和模型改进。本页面不要求填写姓名、电话或联系方式。
""")

show_ids = False

sections = []
for q in QUESTIONS:
    if q["module"] not in sections:
        sections.append(q["module"])

questions_by_section = {}
for section in sections:
    section_items = [q for q in QUESTIONS if q["module"] == section]
    rng = random.Random(f"shenxing-v06-axis-{st.session_state['shuffle_seed']}-{section}")
    rng.shuffle(section_items)
    questions_by_section[section] = section_items

st.divider()
st.subheader("开始作答")
st.caption("题目已自动打乱。所有题目均需作答。为避免默认值造成误判，本测评不会预先选择“3”。")

answers = {}
tabs = st.tabs(sections)
for tab, section in zip(tabs, sections):
    with tab:
        if section.startswith("第一部分"):
            st.info("这一部分同时包含两类题：你自然喜欢/认可什么，以及你最不喜欢被迫面对什么。")
        if section.startswith("第三部分"):
            st.info("这一部分关注你在压力下如何让自己稳定下来，或如何把外界压力处理成自己能承受的形式。")
        if section.startswith("第五部分"):
            st.info("这一部分关注人在极度受压时可能出现的强烈反应，包括对外决裂、强烈否定、自责或自我攻击。它不代表你一定会这样做，也不代表道德评价。")
        for q in questions_by_section[section]:
            label = q["front_text"] if not show_ids else f"【{q['qid']}】{q['front_text']}"
            answers[q["qid"]] = st.radio(
                label,
                options=[1, 2, 3, 4, 5],
                index=None,
                horizontal=True,
                key=q["qid"],
                format_func=lambda x: {
                    1: "1 完全不符合",
                    2: "2 不太符合",
                    3: "3 说不清",
                    4: "4 比较符合",
                    5: "5 非常符合",
                }[x],
            )

answered_count = sum(1 for value in answers.values() if value is not None)
total_count = len(QUESTIONS)
st.progress(answered_count / total_count, text=f"已作答 {answered_count}/{total_count} 题")

st.divider()
st.subheader("非计分对照题")
col1, col2 = st.columns(2)
with col1:
    mbti_past = st.text_input("你过往最常测出的 MBTI 类型是？", placeholder="例如 INTP")
with col2:
    mbti_self = st.text_input("你自认为最接近的 MBTI 类型是？", placeholder="例如 INTP")

if st.button("生成测评结果", type="primary"):
    missing = [q["qid"] for q in QUESTIONS if answers.get(q["qid"]) is None]
    if missing:
        st.error(f"还有 {len(missing)} 题未作答。请完成全部题目后再生成结果。")
        with st.expander("查看未作答题号"):
            st.write("、".join(missing))
        st.stop()

    result = compute_scores(answers)
    report = build_report(result)

    submission_row = build_submission_row(
        answers=answers,
        result=result,
        mbti_past=mbti_past,
        mbti_self=mbti_self,
        submission_id=st.session_state["submission_id"],
    )
    save_status = save_submission(submission_row)

    st.divider()
    st.header(f"{result['level']} {result['top_type']}")
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
        st.subheader("结构摘要")
        m = result["map"]
        role_rows = [
            ("核心判断", m["monarch"], PRINCIPLES[m["monarch"]]),
            ("做事方式", m["chancellor"], PRINCIPLES[m["chancellor"]]),
            ("稳定方式", m["guard"], PRINCIPLES[m["guard"]]),
            ("反面压力", m["civilian"], PRINCIPLES[m["civilian"]]),
            ("解释方式", m["emperor"], PRINCIPLES[m["emperor"]]),
            ("极端反应", m["marshal"], PRINCIPLES[m["marshal"]]),
        ]
        st.table(pd.DataFrame(role_rows, columns=["面向", "功能", "关键词"]))

        st.subheader("候选类型")
        candidate_rows = []
        for candidate_type, display_score in result["ordered_types"]:
            cd = result["detail"][candidate_type]
            candidate_rows.append({
                "类型": candidate_type,
                "核心轴": round(cd.get("monarch_axis", 0), 3),
                "核心轴差": round(cd.get("monarch_axis_centered", 0), 3),
                "分支支持": round(cd.get("branch_score", 0), 3),
                "分支差": round(cd.get("branch_score_centered", 0), 3),
                "综合接近度": round(display_score, 3),
            })
        st.dataframe(pd.DataFrame(candidate_rows), use_container_width=True)

        st.subheader("当前主类型分数")
        t = result["top_type"]
        d = result["detail"][t]
        detail_df = pd.DataFrame([{
            "核心正向": round(d["monarch_raw"], 3),
            "核心轴": round(d.get("monarch_axis", d["monarch_raw"]), 3),
            "做事方式": round(d["chancellor"], 3),
            "稳定方式": round(d["guard"], 3),
            "反面压力": round(d["civilian"], 3),
            "反面正向拥抱": round(d.get("civilian_positive", 0), 3),
            "反面排斥": round(d.get("civilian_aversion", 0), 3),
            "隐藏压力指标": round(d.get("latent_civilian", d["civilian"]), 3),
            "解释方式": round(d["emperor"], 3),
            "极端反应": round(d["marshal"], 3),
            "分支支持度": round(d.get("branch_score", 0), 3),
            "总体接近度": round(d["score"], 3),
            "置信度": result["confidence"],
        }])
        st.dataframe(detail_df, use_container_width=True)

        st.subheader("判型间距")
        gap_df = pd.DataFrame([{
            "核心轴差距": round(result.get("monarch_gap", 0), 3),
            "底盘分支差距": round(result.get("branch_gap", 0), 3),
        }])
        st.dataframe(gap_df, use_container_width=True)
