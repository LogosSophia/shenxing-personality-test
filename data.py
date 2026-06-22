# -*- coding: utf-8 -*-
"""神性论人格王国底盘测评 v0.3 数据表。
本文件由 ChatGPT 根据当前题库草案生成。
"""

PRINCIPLES = {
    "Ti": "自洽性与逻辑性（可理解性）",
    "Te": "建构性与目的性",
    "Ni": "涌现性与压缩性",
    "Ne": "创生性与可能性",
    "Si": "守恒性与不变性",
    "Se": "在场性与现实性",
    "Fi": "本真性与统一性",
    "Fe": "关联性与互系性"
}

TYPE_MAP = {
    "INTP": {
        "monarch": "Ti",
        "chancellor": "Ne",
        "guard": "Si",
        "civilian": "Fe",
        "emperor": "Ni",
        "marshal": "Fi"
    },
    "ENTP": {
        "monarch": "Ne",
        "chancellor": "Ti",
        "guard": "Fe",
        "civilian": "Si",
        "emperor": "Te",
        "marshal": "Se"
    },
    "ISTP": {
        "monarch": "Ti",
        "chancellor": "Se",
        "guard": "Ni",
        "civilian": "Fe",
        "emperor": "Si",
        "marshal": "Fi"
    },
    "ESTP": {
        "monarch": "Se",
        "chancellor": "Ti",
        "guard": "Fe",
        "civilian": "Ni",
        "emperor": "Te",
        "marshal": "Ne"
    },
    "INFP": {
        "monarch": "Fi",
        "chancellor": "Ne",
        "guard": "Si",
        "civilian": "Te",
        "emperor": "Ni",
        "marshal": "Ti"
    },
    "ENFP": {
        "monarch": "Ne",
        "chancellor": "Fi",
        "guard": "Te",
        "civilian": "Si",
        "emperor": "Fe",
        "marshal": "Se"
    },
    "ISFP": {
        "monarch": "Fi",
        "chancellor": "Se",
        "guard": "Ni",
        "civilian": "Te",
        "emperor": "Si",
        "marshal": "Ti"
    },
    "ESFP": {
        "monarch": "Se",
        "chancellor": "Fi",
        "guard": "Te",
        "civilian": "Ni",
        "emperor": "Fe",
        "marshal": "Ne"
    },
    "INTJ": {
        "monarch": "Ni",
        "chancellor": "Te",
        "guard": "Fi",
        "civilian": "Se",
        "emperor": "Ti",
        "marshal": "Si"
    },
    "ENTJ": {
        "monarch": "Te",
        "chancellor": "Ni",
        "guard": "Se",
        "civilian": "Fi",
        "emperor": "Ne",
        "marshal": "Fe"
    },
    "INFJ": {
        "monarch": "Ni",
        "chancellor": "Fe",
        "guard": "Ti",
        "civilian": "Se",
        "emperor": "Fi",
        "marshal": "Si"
    },
    "ENFJ": {
        "monarch": "Fe",
        "chancellor": "Ni",
        "guard": "Se",
        "civilian": "Ti",
        "emperor": "Ne",
        "marshal": "Te"
    },
    "ISTJ": {
        "monarch": "Si",
        "chancellor": "Te",
        "guard": "Fi",
        "civilian": "Ne",
        "emperor": "Ti",
        "marshal": "Ni"
    },
    "ESTJ": {
        "monarch": "Te",
        "chancellor": "Si",
        "guard": "Ne",
        "civilian": "Fi",
        "emperor": "Se",
        "marshal": "Fe"
    },
    "ISFJ": {
        "monarch": "Si",
        "chancellor": "Fe",
        "guard": "Ti",
        "civilian": "Ne",
        "emperor": "Fi",
        "marshal": "Ni"
    },
    "ESFJ": {
        "monarch": "Fe",
        "chancellor": "Si",
        "guard": "Ne",
        "civilian": "Ti",
        "emperor": "Se",
        "marshal": "Te"
    }
}

QUESTIONS_TSV = r"""qid	module	position	dimension	principle	front_text	scoring_key
M_Ti_01	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	我判断一件事时，首先在意它是否自洽、清楚、讲得通。	Ti_MonarchRaw
M_Ti_02	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	如果一个说法前后矛盾，即使它很有用或很动人，我也很难真正接受。	Ti_MonarchRaw
M_Ti_03	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	我习惯先弄清概念、边界和前提，再决定是否继续讨论。	Ti_MonarchRaw
M_Ti_04	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	我最无法忍受别人说不清楚却还强行要求我相信。	Ti_MonarchRaw
M_Te_01	第一部分：君主统治强度	君主	Te	建构性与目的性	我判断一个想法时，很重视它能否建成、推进并产生实际结果。	Te_MonarchRaw
M_Te_02	第一部分：君主统治强度	君主	Te	建构性与目的性	当局面混乱时，我会本能地想把它整理成目标、步骤和责任。	Te_MonarchRaw
M_Te_03	第一部分：君主统治强度	君主	Te	建构性与目的性	如果一件事长期停在空谈里，我会明显失去耐心。	Te_MonarchRaw
M_Te_04	第一部分：君主统治强度	君主	Te	建构性与目的性	我更容易相信能够组织资源、完成任务、达成目的的判断方式。	Te_MonarchRaw
M_Ni_01	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	我经常能从复杂材料中看出一个正在涌现的深层方向。	Ni_MonarchRaw
M_Ni_02	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	我会把大量分散现象压缩成一个核心判断或最终走向。	Ni_MonarchRaw
M_Ni_03	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	比起表面的热闹，我更在意事情背后真正压向哪里。	Ni_MonarchRaw
M_Ni_04	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	我常常觉得某些局面有一个尚未说出的终局正在形成。	Ni_MonarchRaw
M_Ne_01	第一部分：君主统治强度	君主	Ne	创生性与可能性	我面对问题时，会自然想到它还能怎样展开、变形或连接。	Ne_MonarchRaw
M_Ne_02	第一部分：君主统治强度	君主	Ne	创生性与可能性	我很难接受人生被固定成单一路径，没有新出口和新可能。	Ne_MonarchRaw
M_Ne_03	第一部分：君主统治强度	君主	Ne	创生性与可能性	一个词、画面或想法常常会让我立刻联想到许多分支。	Ne_MonarchRaw
M_Ne_04	第一部分：君主统治强度	君主	Ne	创生性与可能性	我更愿意保留可能性，而不是过早把事情完全定死。	Ne_MonarchRaw
M_Si_01	第一部分：君主统治强度	君主	Si	守恒性与不变性	我很重视某些稳定的习惯、旧物、旧经验或不变的节奏。	Si_MonarchRaw
M_Si_02	第一部分：君主统治强度	君主	Si	守恒性与不变性	当外部变化过快时，我会本能地寻找可以守住的东西。	Si_MonarchRaw
M_Si_03	第一部分：君主统治强度	君主	Si	守恒性与不变性	某些旧地方、旧资料、旧记忆会让我感到一种连续而真实的存在。	Si_MonarchRaw
M_Si_04	第一部分：君主统治强度	君主	Si	守恒性与不变性	我不喜欢别人轻易否定过去，好像曾经发生的东西都不重要。	Si_MonarchRaw
M_Se_01	第一部分：君主统治强度	君主	Se	在场性与现实性	我更相信当下看到的、发生的、能直接接触和处理的现实。	Se_MonarchRaw
M_Se_02	第一部分：君主统治强度	君主	Se	在场性与现实性	比起一直分析，我有时更想直接进入现场，把局面打开。	Se_MonarchRaw
M_Se_03	第一部分：君主统治强度	君主	Se	在场性与现实性	我对身体状态、现场气氛和现实变化比较敏感。	Se_MonarchRaw
M_Se_04	第一部分：君主统治强度	君主	Se	在场性与现实性	如果一件事迟迟不落到现实行动上，我会感到烦躁。	Se_MonarchRaw
M_Fi_01	第一部分：君主统治强度	君主	Fi	本真性与统一性	我判断一件事时，很在意它是否符合我的真心、信念和底线。	Fi_MonarchRaw
M_Fi_02	第一部分：君主统治强度	君主	Fi	本真性与统一性	如果一件事违背内在真实，即使有好处，我也很难接受。	Fi_MonarchRaw
M_Fi_03	第一部分：君主统治强度	君主	Fi	本真性与统一性	我很难长期扮演一个与自己内在不统一的人。	Fi_MonarchRaw
M_Fi_04	第一部分：君主统治强度	君主	Fi	本真性与统一性	别人说我没有真心、没有底线、只是装出来的，会明显刺痛我。	Fi_MonarchRaw
M_Fe_01	第一部分：君主统治强度	君主	Fe	关联性与互系性	我很在意人与人之间是否形成真实的关联和互相回应。	Fe_MonarchRaw
M_Fe_02	第一部分：君主统治强度	君主	Fe	关联性与互系性	在一个场合里，我会注意谁被冷落、谁没有被接住、谁被排除在外。	Fe_MonarchRaw
M_Fe_03	第一部分：君主统治强度	君主	Fe	关联性与互系性	比起一个人单独正确，我更在意这件事能否让关系和共同处境成立。	Fe_MonarchRaw
M_Fe_04	第一部分：君主统治强度	君主	Fe	关联性与互系性	当关系气氛变坏时，我很难完全无所谓。	Fe_MonarchRaw
C_Ti_01	第二部分：子民/刺痛入口	子民	Ti	自洽性与逻辑性（可理解性）	如果别人不断要求我证明自己的前提和逻辑，我会感到被逼迫。	Ti_Civilian
C_Ti_02	第二部分：子民/刺痛入口	子民	Ti	自洽性与逻辑性（可理解性）	如果所有人都说我根本没想清楚，我会被明显刺痛。	Ti_Civilian
C_Te_01	第二部分：子民/刺痛入口	子民	Te	建构性与目的性	当别人追问我到底做成了什么、承担了什么结果时，我会感到压力。	Te_Civilian
C_Te_02	第二部分：子民/刺痛入口	子民	Te	建构性与目的性	如果别人说我只会想或只会说，无法进入现实建构，我会被刺痛。	Te_Civilian
C_Ni_01	第二部分：子民/刺痛入口	子民	Ni	涌现性与压缩性	当别人要求我说清楚自己到底要走向哪里时，我会感到压力。	Ni_Civilian
C_Ni_02	第二部分：子民/刺痛入口	子民	Ni	涌现性与压缩性	如果别人说我没有深层判断，只是在表面忙乱，我会被刺痛。	Ni_Civilian
C_Ne_01	第二部分：子民/刺痛入口	子民	Ne	创生性与可能性	当别人不断打开新可能、新角度、新玩法时，我会感到烦躁或失控。	Ne_Civilian
C_Ne_02	第二部分：子民/刺痛入口	子民	Ne	创生性与可能性	如果别人说我封闭、僵硬、没有想象力，我会被刺痛。	Ne_Civilian
C_Si_01	第二部分：子民/刺痛入口	子民	Si	守恒性与不变性	我最不愿面对旧伤、旧事、旧记忆突然回来。	Si_Civilian
C_Si_02	第二部分：子民/刺痛入口	子民	Si	守恒性与不变性	如果别人轻易翻出我的旧账、旧伤或旧我，我会强烈抗拒。	Si_Civilian
C_Se_01	第二部分：子民/刺痛入口	子民	Se	在场性与现实性	当事情逼到现场，要求我立刻进入现实，我会明显紧张。	Se_Civilian
C_Se_02	第二部分：子民/刺痛入口	子民	Se	在场性与现实性	如果别人说我只会躲在脑子里，不敢接触现实，我会被刺痛。	Se_Civilian
C_Fi_01	第二部分：子民/刺痛入口	子民	Fi	本真性与统一性	我害怕有一天发现自己已经变成一个不像自己的人。	Fi_Civilian
C_Fi_02	第二部分：子民/刺痛入口	子民	Fi	本真性与统一性	如果别人说我没有真心、没有底线，只是顺着现实走，我会被刺痛。	Fi_Civilian
C_Fe_01	第二部分：子民/刺痛入口	子民	Fe	关联性与互系性	当别人期待我回应关系、照顾气氛、表达在乎时，我会感到压力。	Fe_Civilian
C_Fe_02	第二部分：子民/刺痛入口	子民	Fe	关联性与互系性	如果别人说我冷、隔离、不回应、不在共同世界里，我会被刺痛。	Fe_Civilian
Z_Ti_01	第三部分：宰相施政方式	宰相	Ti	自洽性与逻辑性（可理解性）	我让事情运转起来的方式，常常是先把结构、概念和前提理清。	Ti_Chancellor
Z_Ti_02	第三部分：宰相施政方式	宰相	Ti	自洽性与逻辑性（可理解性）	我擅长通过澄清规则、定义和内在关系来推进讨论。	Ti_Chancellor
Z_Te_01	第三部分：宰相施政方式	宰相	Te	建构性与目的性	我让事情运转起来的方式，是把它变成可执行、可检查、可完成的任务。	Te_Chancellor
Z_Te_02	第三部分：宰相施政方式	宰相	Te	建构性与目的性	我擅长把混乱局面组织成目标、资源、流程和结果。	Te_Chancellor
Z_Ni_01	第三部分：宰相施政方式	宰相	Ni	涌现性与压缩性	我会用一个长程判断或深层方向来统摄眼前很多小选择。	Ni_Chancellor
Z_Ni_02	第三部分：宰相施政方式	宰相	Ni	涌现性与压缩性	我擅长把分散线索压缩成一个能够指导行动的核心判断。	Ni_Chancellor
Z_Ne_01	第三部分：宰相施政方式	宰相	Ne	创生性与可能性	我遇到障碍时，第一反应常常是换一个角度、入口或玩法。	Ne_Chancellor
Z_Ne_02	第三部分：宰相施政方式	宰相	Ne	创生性与可能性	我擅长打开分支、连接资源、创造新的可能路径。	Ne_Chancellor
Z_Si_01	第三部分：宰相施政方式	宰相	Si	守恒性与不变性	我做事时，会自然依赖过去经验、熟悉流程和稳定节奏。	Si_Chancellor
Z_Si_02	第三部分：宰相施政方式	宰相	Si	守恒性与不变性	我擅长通过保留、复用、沉淀既有经验来让事情继续运转。	Si_Chancellor
Z_Se_01	第三部分：宰相施政方式	宰相	Se	在场性与现实性	比起一直讨论，我更擅长在现实切点中边做边调整。	Se_Chancellor
Z_Se_02	第三部分：宰相施政方式	宰相	Se	在场性与现实性	我擅长通过现场行动、实际接触和即时反馈推动局面。	Se_Chancellor
Z_Fi_01	第三部分：宰相施政方式	宰相	Fi	本真性与统一性	我让自己坚持下去的力量，常常来自内在信念，而不是外部要求。	Fi_Chancellor
Z_Fi_02	第三部分：宰相施政方式	宰相	Fi	本真性与统一性	我擅长用真心、底线和内在统一来决定事情该不该继续。	Fi_Chancellor
Z_Fe_01	第三部分：宰相施政方式	宰相	Fe	关联性与互系性	我解决问题时，常常会先处理人与人之间能不能互相关联、共同成立。	Fe_Chancellor
Z_Fe_02	第三部分：宰相施政方式	宰相	Fe	关联性与互系性	我擅长通过回应、协调和重新连接来让共同处境运转起来。	Fe_Chancellor
G_Ti_01	第四部分：护卫守门方式	护卫	Ti	自洽性与逻辑性（可理解性）	只要我能把问题讲清楚，它对我的威胁就会下降。	Ti_Guard
G_Ti_02	第四部分：护卫守门方式	护卫	Ti	自洽性与逻辑性（可理解性）	压力进入时，我会用分析、定义和解释来保护自己。	Ti_Guard
G_Te_01	第四部分：护卫守门方式	护卫	Te	建构性与目的性	当我痛苦或慌乱时，我会把事情变成待办事项、流程和现实安排。	Te_Guard
G_Te_02	第四部分：护卫守门方式	护卫	Te	建构性与目的性	压力进入时，我会通过做计划、推进结果和控制资源来恢复稳定。	Te_Guard
G_Ni_01	第四部分：护卫守门方式	护卫	Ni	涌现性与压缩性	我保护自己的方式，是把偶然事件压缩成一种深层解释或方向判断。	Ni_Guard
G_Ni_02	第四部分：护卫守门方式	护卫	Ni	涌现性与压缩性	压力进入时，我会寻找它背后的命运线索或最终意义。	Ni_Guard
G_Ne_01	第四部分：护卫守门方式	护卫	Ne	创生性与可能性	只要还有新可能，我就不容易被彻底困死。	Ne_Guard
G_Ne_02	第四部分：护卫守门方式	护卫	Ne	创生性与可能性	压力进入时，我会通过打开新解释、新玩法或新出口来缓冲。	Ne_Guard
G_Si_01	第四部分：护卫守门方式	护卫	Si	守恒性与不变性	压力大时，我会退回熟悉的环境、旧习惯、旧物或旧资料里。	Si_Guard
G_Si_02	第四部分：护卫守门方式	护卫	Si	守恒性与不变性	我会通过守住稳定节奏、过去经验和不变部分来保护自己。	Si_Guard
G_Se_01	第四部分：护卫守门方式	护卫	Se	在场性与现实性	压力进入时，我会通过出门、运动、处理现场、做点实际动作来缓冲。	Se_Guard
G_Se_02	第四部分：护卫守门方式	护卫	Se	在场性与现实性	我会通过身体、行动和现实在场来让自己重新稳定。	Se_Guard
G_Fi_01	第四部分：护卫守门方式	护卫	Fi	本真性与统一性	当我被外界冲击时，我会退回自己的良知、信念和底线。	Fi_Guard
G_Fi_02	第四部分：护卫守门方式	护卫	Fi	本真性与统一性	我会通过确认自己仍然真实、完整、不背叛自己来保护自己。	Fi_Guard
G_Fe_01	第四部分：护卫守门方式	护卫	Fe	关联性与互系性	当我被击中时，被理解、被回应、被接住，对我很重要。	Fe_Guard
G_Fe_02	第四部分：护卫守门方式	护卫	Fe	关联性与互系性	我会通过关系回应、共同感和互相连接来恢复稳定。	Fe_Guard
E_Ti_01	第五部分：帝师合法性解释	帝师	Ti	自洽性与逻辑性（可理解性）	我能把复杂局面重新组织成一套可理解、可审查、可解释的结构。	Ti_EmperorTeacher
E_Ti_02	第五部分：帝师合法性解释	帝师	Ti	自洽性与逻辑性（可理解性）	我能说明一种判断为什么在逻辑上成立，而不只是说自己觉得对。	Ti_EmperorTeacher
E_Ti_03	第五部分：帝师合法性解释	帝师	Ti	自洽性与逻辑性（可理解性）	面对质疑时，我更倾向于让结构自己站住，而不是急着用情绪证明。	Ti_EmperorTeacher
E_Te_01	第五部分：帝师合法性解释	帝师	Te	建构性与目的性	我能把分散资源和现实压力组织成一个明确目的和可执行秩序。	Te_EmperorTeacher
E_Te_02	第五部分：帝师合法性解释	帝师	Te	建构性与目的性	我能解释一套安排为什么能承担结果，而不只是看起来有效。	Te_EmperorTeacher
E_Te_03	第五部分：帝师合法性解释	帝师	Te	建构性与目的性	面对质疑时，我不太需要硬压别人服从，而更希望让结果秩序证明自身。	Te_EmperorTeacher
E_Ni_01	第五部分：帝师合法性解释	帝师	Ni	涌现性与压缩性	我能从复杂材料中看出涌现出的整体方向，并把它压缩成高阶判断。	Ni_EmperorTeacher
E_Ni_02	第五部分：帝师合法性解释	帝师	Ni	涌现性与压缩性	我能解释一个判断为什么代表深层走向，而不只是个人预感。	Ni_EmperorTeacher
E_Ni_03	第五部分：帝师合法性解释	帝师	Ni	涌现性与压缩性	面对混乱时，我更像是在等待整体方向显形，而不是急着证明某个局部。	Ni_EmperorTeacher
E_Ne_01	第五部分：帝师合法性解释	帝师	Ne	创生性与可能性	我能为一个已经僵住的系统打开新的创生入口和可能空间。	Ne_EmperorTeacher
E_Ne_02	第五部分：帝师合法性解释	帝师	Ne	创生性与可能性	我能解释为什么一个新分支不是胡思乱想，而是秩序继续生成的入口。	Ne_EmperorTeacher
E_Ne_03	第五部分：帝师合法性解释	帝师	Ne	创生性与可能性	面对封闭局面时，我更倾向于让新的可能自己打开秩序，而不是强行破坏。	Ne_EmperorTeacher
E_Si_01	第五部分：帝师合法性解释	帝师	Si	守恒性与不变性	我能从变化中提取出需要守住的不变部分，并把它变成稳定秩序。	Si_EmperorTeacher
E_Si_02	第五部分：帝师合法性解释	帝师	Si	守恒性与不变性	我能解释为什么某些东西必须保留，而不是出于单纯习惯或怀旧。	Si_EmperorTeacher
E_Si_03	第五部分：帝师合法性解释	帝师	Si	守恒性与不变性	面对变化时，我不只是抗拒变化，而是试图说明什么不能被轻易破坏。	Si_EmperorTeacher
E_Se_01	第五部分：帝师合法性解释	帝师	Se	在场性与现实性	我能在混乱现场中直接抓住现实切点，让局面重新进入可处理状态。	Se_EmperorTeacher
E_Se_02	第五部分：帝师合法性解释	帝师	Se	在场性与现实性	我能解释为什么必须回到现场与现实，而不是停留在远处判断。	Se_EmperorTeacher
E_Se_03	第五部分：帝师合法性解释	帝师	Se	在场性与现实性	面对僵局时，我更倾向于让现实接触本身打开秩序，而不是只靠解释。	Se_EmperorTeacher
E_Fi_01	第五部分：帝师合法性解释	帝师	Fi	本真性与统一性	我能把分裂、妥协和外部压力重新统一到真实的内在原则中。	Fi_EmperorTeacher
E_Fi_02	第五部分：帝师合法性解释	帝师	Fi	本真性与统一性	我能解释为什么某条底线不是任性，而是人格统一性的要求。	Fi_EmperorTeacher
E_Fi_03	第五部分：帝师合法性解释	帝师	Fi	本真性与统一性	面对质疑时，我更倾向于让真实本身获得说明，而不是用过激方式证明自己。	Fi_EmperorTeacher
E_Fe_01	第五部分：帝师合法性解释	帝师	Fe	关联性与互系性	我能让断裂的关系、分散的个体和互相隔离的处境重新形成关联。	Fe_EmperorTeacher
E_Fe_02	第五部分：帝师合法性解释	帝师	Fe	关联性与互系性	我能解释为什么关系与互系不是表面和气，而是秩序成立的条件。	Fe_EmperorTeacher
E_Fe_03	第五部分：帝师合法性解释	帝师	Fe	关联性与互系性	面对关系冲突时，我更倾向于让共同处境获得解释，而不是只靠情绪维持。	Fe_EmperorTeacher
X_Ti_01	第六部分：元帅极限反相	元帅	Ti	自洽性与逻辑性（可理解性）	当我的底线或真诚感被侵犯时，我曾经会或强烈想要冷酷地判定对方不配为人、不值得体谅。	Ti_Marshal
X_Ti_02	第六部分：元帅极限反相	元帅	Ti	自洽性与逻辑性（可理解性）	当我觉得一个人已经污染我的内在秩序时，我曾经会或强烈想要给对方下定义、定性，然后彻底断绝往来。	Ti_Marshal
X_Te_01	第六部分：元帅极限反相	元帅	Te	建构性与目的性	当某人破坏我所在的关系场或共同体秩序时，我曾经会或强烈想要用规则、责任、证据和后果把对方孤立出去。	Te_Marshal
X_Te_02	第六部分：元帅极限反相	元帅	Te	建构性与目的性	当我认定某人伤害了共同世界时，我曾经会或强烈想要发动清算、公开定责，甚至用舆论压力围剿对方。	Te_Marshal
X_Ni_01	第六部分：元帅极限反相	元帅	Ni	涌现性与压缩性	当稳定和信任被破坏时，我曾经会或强烈想要直接宣告对方没救了、这件事完了、未来不会好了。	Ni_Marshal
X_Ni_02	第六部分：元帅极限反相	元帅	Ni	涌现性与压缩性	当我被逼急时，我曾经会或强烈想要给一个人或一段关系下最终判词：不用再看了，结局已经死了。	Ni_Marshal
X_Ne_01	第六部分：元帅极限反相	元帅	Ne	创生性与可能性	当我无法掌控现实局面时，我曾经会或强烈想要搅乱变量、制造分叉，让大家都别想稳定收场。	Ne_Marshal
X_Ne_02	第六部分：元帅极限反相	元帅	Ne	创生性与可能性	当我不好过时，我曾经会或强烈想要让局面变复杂、变混乱，哪怕损人不利己，也让别人别想好过。	Ne_Marshal
X_Si_01	第六部分：元帅极限反相	元帅	Si	守恒性与不变性	当我的判断被挑战时，我曾经会或强烈想要翻旧账、抓旧证据，把对方过去的错误重新钉出来。	Si_Marshal
X_Si_02	第六部分：元帅极限反相	元帅	Si	守恒性与不变性	当我认定对方犯过不可原谅的错时，我曾经会或强烈想要把它变成耻辱柱：一刻是罪犯，一辈子都是罪犯。	Si_Marshal
X_Se_01	第六部分：元帅极限反相	元帅	Se	在场性与现实性	当所有出口都被堵死时，我曾经会或强烈想要大闹一场、撕开现场，让原来的局面无法继续维持。	Se_Marshal
X_Se_02	第六部分：元帅极限反相	元帅	Se	在场性与现实性	当我被逼到极限时，我曾经会或强烈想要直接掀桌、摔门、闹大，甚至产生毁掉一切的冲动。	Se_Marshal
X_Fi_01	第六部分：元帅极限反相	元帅	Fi	本真性与统一性	当我已经讲不通、又被对方彻底激怒时，我曾经会或强烈想要情绪爆发、羞辱对方，让对方别再侮辱我的智商。	Fi_Marshal
X_Fi_02	第六部分：元帅极限反相	元帅	Fi	本真性与统一性	当我觉得对方根本不配和我交流时，我曾经会或强烈想要翻脸、拉黑、断绝，用很不讲理的方式把对方踢出去。	Fi_Marshal
X_Fe_01	第六部分：元帅极限反相	元帅	Fe	关联性与互系性	当我的目标、秩序或执行被人阻碍时，我曾经会或强烈想要用关系压力、道德绑架或情感绑架逼对方让步。	Fe_Marshal
X_Fe_02	第六部分：元帅极限反相	元帅	Fe	关联性与互系性	当我被逼急时，我曾经会或强烈想要把自己的痛苦、崩溃或关系后果压到对方身上，让对方觉得不能拒绝我。	Fe_Marshal
"""

def load_questions():
    rows = []
    lines = [line for line in QUESTIONS_TSV.strip().splitlines() if line.strip()]
    header = lines[0].split("\t")
    for line in lines[1:]:
        parts = line.split("\t")
        if len(parts) != len(header):
            raise ValueError(f"题目行字段数量不正确: {line}")
        item = dict(zip(header, parts))
        rows.append(item)
    return rows

QUESTIONS = load_questions()
