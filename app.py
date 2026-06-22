# -*- coding: utf-8 -*-
import random
import uuid

import streamlit as st
import pandas as pd

from data import QUESTIONS, TYPE_MAP, PRINCIPLES
from scoring import compute_scores, build_report
from backend import build_submission_row, save_submission

st.set_page_config(page_title="神性论人格王国底盘测评 v0.3", page_icon="👑", layout="wide")

if "submission_id" not in st.session_state:
    st.session_state["submission_id"] = str(uuid.uuid4())

st.title("神性论人格王国底盘测评 v0.3")
st.caption("人格结构研究与自我理解工具｜非医学、非心理诊断")

with st.expander("测评说明", expanded=True):
    st.markdown("""
本测评只判定人格王国底盘、低位/高位、帝师气质、元帅反相与护卫风险提示。  
不判登山、幸福、英雄、圣徒、超人、神魔或人生终局。

量表说明：

- 1 = 完全不符合
- 2 = 不太符合
- 3 = 说不清 / 一半一半
- 4 = 比较符合
- 5 = 非常符合

低位不是能力低，而是君主秩序正在建立，类似秦。  
高位不是更激烈，而是君主已经坐稳，王国开始解释自身秩序，类似汉。

生成结果时，系统会默认记录本次答卷与计算结果，用于后续题库校准和模型改进。后台记录包含题目答案、各位次分数、最终结果、风险提示和可选 MBTI 对照；本页面不要求填写姓名、电话或联系方式。
""")

randomize = st.toggle("随机打乱每部分内部题目顺序", value=False)
show_ids = st.toggle("显示题号", value=False)

# 固定分段顺序。若随机，只随机每个分段内部题目，避免标签页顺序被打乱。
sections = []
for q in QUESTIONS:
    if q["module"] not in sections:
        sections.append(q["module"])

questions_by_section = {}
for section in sections:
    section_items = [q for q in QUESTIONS if q["module"] == section]
    if randomize:
        rng = random.Random(f"shenxing-v03-{section}")
        rng.shuffle(section_items)
    questions_by_section[section] = section_items

st.divider()
st.subheader("开始作答")
st.caption("所有题目均需作答。为避免默认值造成误判，本测评不会预先选择“3”。")

answers = {}
tabs = st.tabs(sections)
for tab, section in zip(tabs, sections):
    with tab:
        if section.startswith("第六部分"):
            st.info("以下题目询问的是极端失望、愤怒、受压或被逼到尽头时的反应倾向，不代表你平时会这样，也不是道德评价。")
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

    if save_status["ok"]:
        if save_status["backend"] == "google_sheets":
            st.caption("后台记录完成。")
        else:
            st.caption("后台记录已写入本地临时文件。正式收集样本时，请在 Streamlit Secrets 中配置 Google Sheets 持久化后台。")
    else:
        st.warning(f"结果已生成，但后台记录失败：{save_status['message']}")

    if result["risks"]:
        st.subheader("附加提示")
        for risk in result["risks"]:
            st.warning(f"**{risk['title']}**\n\n{risk['body']}")

    st.subheader("王国位次")
    m = result["map"]
    role_rows = [
        ("君主", m["monarch"], PRINCIPLES[m["monarch"]]),
        ("宰相", m["chancellor"], PRINCIPLES[m["chancellor"]]),
        ("护卫", m["guard"], PRINCIPLES[m["guard"]]),
        ("子民", m["civilian"], PRINCIPLES[m["civilian"]]),
        ("帝师", m["emperor"], PRINCIPLES[m["emperor"]]),
        ("元帅", m["marshal"], PRINCIPLES[m["marshal"]]),
    ]
    st.table(pd.DataFrame(role_rows, columns=["位次", "功能", "原则"]))

    st.subheader("16型底盘分")
    score_df = pd.DataFrame(
        [{"类型": t, "底盘分": round(s, 3)} for t, s in result["ordered_types"]]
    )
    st.dataframe(score_df, use_container_width=True)

    st.subheader("当前主类型各位次分")
    t = result["top_type"]
    d = result["detail"][t]
    detail_df = pd.DataFrame([{
        "君主原始分": round(d["monarch_raw"], 3),
        "宰相分": round(d["chancellor"], 3),
        "护卫分": round(d["guard"], 3),
        "子民分": round(d["civilian"], 3),
        "帝师分": round(d["emperor"], 3),
        "元帅分": round(d["marshal"], 3),
        "底盘分": round(d["score"], 3),
        "置信度": result["confidence"],
    }])
    st.dataframe(detail_df, use_container_width=True)

    if mbti_past or mbti_self:
        st.info(f"对照信息：过往常测 MBTI：{mbti_past or '未填写'}；自认为接近：{mbti_self or '未填写'}。")
