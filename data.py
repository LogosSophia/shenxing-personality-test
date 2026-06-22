# -*- coding: utf-8 -*-
"""神性论人格王国底盘测评 v0.4 数据表。"""

PRINCIPLES = {
    "Ti": "自洽性与逻辑性（可理解性）",
    "Te": "建构性与目的性",
    "Ni": "涌现性与压缩性",
    "Ne": "创生性与可能性",
    "Si": "守恒性与不变性",
    "Se": "在场性与现实性",
    "Fi": "本真性与统一性",
    "Fe": "关联性与互系性",
}

TYPE_MAP = {
    "INTP": {"monarch": "Ti", "chancellor": "Ne", "guard": "Si", "civilian": "Fe", "emperor": "Ni", "marshal": "Fi"},
    "ENTP": {"monarch": "Ne", "chancellor": "Ti", "guard": "Fe", "civilian": "Si", "emperor": "Te", "marshal": "Se"},
    "ISTP": {"monarch": "Ti", "chancellor": "Se", "guard": "Ni", "civilian": "Fe", "emperor": "Si", "marshal": "Fi"},
    "ESTP": {"monarch": "Se", "chancellor": "Ti", "guard": "Fe", "civilian": "Ni", "emperor": "Te", "marshal": "Ne"},
    "INFP": {"monarch": "Fi", "chancellor": "Ne", "guard": "Si", "civilian": "Te", "emperor": "Ni", "marshal": "Ti"},
    "ENFP": {"monarch": "Ne", "chancellor": "Fi", "guard": "Te", "civilian": "Si", "emperor": "Fe", "marshal": "Se"},
    "ISFP": {"monarch": "Fi", "chancellor": "Se", "guard": "Ni", "civilian": "Te", "emperor": "Si", "marshal": "Ti"},
    "ESFP": {"monarch": "Se", "chancellor": "Fi", "guard": "Te", "civilian": "Ni", "emperor": "Fe", "marshal": "Ne"},
    "INTJ": {"monarch": "Ni", "chancellor": "Te", "guard": "Fi", "civilian": "Se", "emperor": "Ti", "marshal": "Si"},
    "ENTJ": {"monarch": "Te", "chancellor": "Ni", "guard": "Se", "civilian": "Fi", "emperor": "Ne", "marshal": "Fe"},
    "INFJ": {"monarch": "Ni", "chancellor": "Fe", "guard": "Ti", "civilian": "Se", "emperor": "Fi", "marshal": "Si"},
    "ENFJ": {"monarch": "Fe", "chancellor": "Ni", "guard": "Se", "civilian": "Ti", "emperor": "Ne", "marshal": "Te"},
    "ISTJ": {"monarch": "Si", "chancellor": "Te", "guard": "Fi", "civilian": "Ne", "emperor": "Ti", "marshal": "Ni"},
    "ESTJ": {"monarch": "Te", "chancellor": "Si", "guard": "Ne", "civilian": "Fi", "emperor": "Se", "marshal": "Fe"},
    "ISFJ": {"monarch": "Si", "chancellor": "Fe", "guard": "Ti", "civilian": "Ne", "emperor": "Fi", "marshal": "Ni"},
    "ESFJ": {"monarch": "Fe", "chancellor": "Si", "guard": "Ne", "civilian": "Ti", "emperor": "Se", "marshal": "Te"},
}

QUESTIONS_TSV = r"""qid	module	position	dimension	principle	front_text	scoring_key
M_Ti_01	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	如果一个方案很有效，但概念和前提很混乱，我还是很难真正接受。	Ti_MonarchRaw
M_Ti_02	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	比起尽快推进，我更需要先弄清楚这件事到底讲不讲得通。	Ti_MonarchRaw
M_Ti_03	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	如果一件事前后说不通，我很难只因为大家都接受就跟着接受。	Ti_MonarchRaw
M_Ti_04	第一部分：君主统治强度	君主	Ti	自洽性与逻辑性（可理解性）	做判断前，我通常会先确认边界、定义和条件有没有说清楚。	Ti_MonarchRaw
M_Te_01	第一部分：君主统治强度	君主	Te	建构性与目的性	如果一个想法很漂亮，但无法落地执行，我会很快失去耐心。	Te_MonarchRaw
M_Te_02	第一部分：君主统治强度	君主	Te	建构性与目的性	比起把话说得完全严密，我更在意事情能不能被组织起来并产生结果。	Te_MonarchRaw
M_Te_03	第一部分：君主统治强度	君主	Te	建构性与目的性	当局面混乱时，我会本能地想先分清目标、责任和可执行步骤。	Te_MonarchRaw
M_Te_04	第一部分：君主统治强度	君主	Te	建构性与目的性	如果一件事没有结果、没有承担、没有推进，我很难相信它真的成立。	Te_MonarchRaw
M_Ni_01	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	比起眼前的热闹，我更在意这件事最后会走向哪里。	Ni_MonarchRaw
M_Ni_02	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	我常常会从很多杂乱信息里抓出一个真正压向未来的方向。	Ni_MonarchRaw
M_Ni_03	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	如果一件事没有深层方向，只是在表面忙乱，我会很难投入。	Ni_MonarchRaw
M_Ni_04	第一部分：君主统治强度	君主	Ni	涌现性与压缩性	我做判断时，很容易把分散现象压缩成一个核心走向。	Ni_MonarchRaw
M_Ne_01	第一部分：君主统治强度	君主	Ne	创生性与可能性	面对问题时，我会自然想到它还能怎样展开、变形或连接。	Ne_MonarchRaw
M_Ne_02	第一部分：君主统治强度	君主	Ne	创生性与可能性	我很难接受一件事被固定成唯一道路，没有新的出口和玩法。	Ne_MonarchRaw
M_Ne_03	第一部分：君主统治强度	君主	Ne	创生性与可能性	比起把事情过早定死，我更愿意先保留可能性。	Ne_MonarchRaw
M_Ne_04	第一部分：君主统治强度	君主	Ne	创生性与可能性	一个词、画面或想法，常常会让我立刻想到许多分支。	Ne_MonarchRaw
M_Si_01	第一部分：君主统治强度	君主	Si	守恒性与不变性	我很重视那些已经沉淀下来的习惯、经验、节奏或旧东西。	Si_MonarchRaw
M_Si_02	第一部分：君主统治强度	君主	Si	守恒性与不变性	外部变化太快时，我会本能地想先守住一些不能乱的东西。	Si_MonarchRaw
M_Si_03	第一部分：君主统治强度	君主	Si	守恒性与不变性	我不喜欢别人轻易否定过去，好像曾经发生的东西都不重要。	Si_MonarchRaw
M_Si_04	第一部分：君主统治强度	君主	Si	守恒性与不变性	比起不断换新，我更相信经过时间验证、能够延续下来的东西。	Si_MonarchRaw
M_Se_01	第一部分：君主统治强度	君主	Se	在场性与现实性	比起一直分析，我更相信当下正在发生、能直接处理的现实。	Se_MonarchRaw
M_Se_02	第一部分：君主统治强度	君主	Se	在场性与现实性	如果一件事迟迟不落到现实行动上，我会感到烦躁。	Se_MonarchRaw
M_Se_03	第一部分：君主统治强度	君主	Se	在场性与现实性	我更愿意直接进入现场，先把局面打开，再边做边调整。	Se_MonarchRaw
M_Se_04	第一部分：君主统治强度	君主	Se	在场性与现实性	身体状态、现场气氛和现实变化，会很快影响我的判断。	Se_MonarchRaw
M_Fi_01	第一部分：君主统治强度	君主	Fi	本真性与统一性	如果一件事让我越来越不像自己，即使它有好处，我也很难继续。	Fi_MonarchRaw
M_Fi_02	第一部分：君主统治强度	君主	Fi	本真性与统一性	比起得到外部认可，我更不能接受自己内心过不去。	Fi_MonarchRaw
M_Fi_03	第一部分：君主统治强度	君主	Fi	本真性与统一性	如果一种选择会让我违背良知或底线，我很难因为它有用就接受。	Fi_MonarchRaw
M_Fi_04	第一部分：君主统治强度	君主	Fi	本真性与统一性	我很难长期扮演一个和自己内在不一致的人。	Fi_MonarchRaw
M_Fe_01	第一部分：君主统治强度	君主	Fe	关联性与互系性	如果一个判断让大家无法继续共同相处，我会怀疑它是不是真的合适。	Fe_MonarchRaw
M_Fe_02	第一部分：君主统治强度	君主	Fe	关联性与互系性	比起一个人单独正确，我更在意这件事能不能让共同处境成立。	Fe_MonarchRaw
M_Fe_03	第一部分：君主统治强度	君主	Fe	关联性与互系性	在一个场合里，我会很快注意到谁被冷落、谁被排除在外。	Fe_MonarchRaw
M_Fe_04	第一部分：君主统治强度	君主	Fe	关联性与互系性	当关系气氛变坏、大家无法互相接住时，我很难完全无所谓。	Fe_MonarchRaw
C_Ti_01	第二部分：子民/刺痛入口	子民	Ti	自洽性与逻辑性（可理解性）	我很排斥那种为了证明自己清楚、正确，就让别人下不来台的人。	Ti_Civilian
C_Ti_02	第二部分：子民/刺痛入口	子民	Ti	自洽性与逻辑性（可理解性）	当大家本来可以求同存异时，如果有人反复指出差异和矛盾，我会很烦。	Ti_Civilian
C_Te_01	第二部分：子民/刺痛入口	子民	Te	建构性与目的性	如果别人问我“你说得这么真诚，那你到底做成了什么”，我会很焦虑。	Te_Civilian
C_Te_02	第二部分：子民/刺痛入口	子民	Te	建构性与目的性	我很讨厌别人用结果和现实压力来压我，好像没做成就什么都不算。	Te_Civilian
C_Ni_01	第二部分：子民/刺痛入口	子民	Ni	涌现性与压缩性	如果别人说我只是活在当下、其实是在虚耗光阴，我会很不舒服。	Ni_Civilian
C_Ni_02	第二部分：子民/刺痛入口	子民	Ni	涌现性与压缩性	我很讨厌别人问我：“你这样下去，最后到底要走向哪里？”	Ni_Civilian
C_Ne_01	第二部分：子民/刺痛入口	子民	Ne	创生性与可能性	我很讨厌别人说我封闭、僵硬、没想象力，看不到新的可能。	Ne_Civilian
C_Ne_02	第二部分：子民/刺痛入口	子民	Ne	创生性与可能性	当别人不断提出新可能，好像我守住的东西只是固执时，我会很烦。	Ne_Civilian
C_Si_01	第二部分：子民/刺痛入口	子民	Si	守恒性与不变性	如果别人问我“你到底有没有自己真正想要的东西”，我会很不舒服。	Si_Civilian
C_Si_02	第二部分：子民/刺痛入口	子民	Si	守恒性与不变性	我很讨厌别人说我只是不断换方向，却没有任何东西真正留得住。	Si_Civilian
C_Se_01	第二部分：子民/刺痛入口	子民	Se	在场性与现实性	当事情突然逼到现场，要求我马上面对现实后果时，我会很焦虑。	Se_Civilian
C_Se_02	第二部分：子民/刺痛入口	子民	Se	在场性与现实性	如果别人说我只会想、只会判断，却不敢真的下场，我会很受不了。	Se_Civilian
C_Fi_01	第二部分：子民/刺痛入口	子民	Fi	本真性与统一性	如果别人说我太冷血，为了结果什么都能做，我会很受不了。	Fi_Civilian
C_Fi_02	第二部分：子民/刺痛入口	子民	Fi	本真性与统一性	如果别人说我已经不像自己了，只剩任务、效率和成功，我会很烦。	Fi_Civilian
C_Fe_01	第二部分：子民/刺痛入口	子民	Fe	关联性与互系性	如果别人说我只顾自己想清楚，根本不顾大家，我会很不爽。	Fe_Civilian
C_Fe_02	第二部分：子民/刺痛入口	子民	Fe	关联性与互系性	如果别人说我为了讲道理，把人逼得下不来台，还觉得自己没错，我会很受不了。	Fe_Civilian
Z_Ti_01	第三部分：宰相施政方式	宰相	Ti	自洽性与逻辑性（可理解性）	我推进事情时，常常会先把结构、概念和前提理清。	Ti_Chancellor
Z_Ti_02	第三部分：宰相施政方式	宰相	Ti	自洽性与逻辑性（可理解性）	遇到混乱讨论时，我通常会通过澄清定义和边界来让事情继续。	Ti_Chancellor
Z_Te_01	第三部分：宰相施政方式	宰相	Te	建构性与目的性	一旦方向确定，我会自然地把它拆成目标、步骤和责任。	Te_Chancellor
Z_Te_02	第三部分：宰相施政方式	宰相	Te	建构性与目的性	我推进事情时，会很在意每一步是否可检查、可完成。	Te_Chancellor
Z_Ni_01	第三部分：宰相施政方式	宰相	Ni	涌现性与压缩性	我会用一个长程方向或深层判断，统摄眼前很多小选择。	Ni_Chancellor
Z_Ni_02	第三部分：宰相施政方式	宰相	Ni	涌现性与压缩性	我擅长把分散线索压缩成一个能指导行动的核心判断。	Ni_Chancellor
Z_Ne_01	第三部分：宰相施政方式	宰相	Ne	创生性与可能性	遇到障碍时，我通常会先换个入口、换个角度，而不是直接硬推。	Ne_Chancellor
Z_Ne_02	第三部分：宰相施政方式	宰相	Ne	创生性与可能性	我常常通过联想、替代方案和新连接，让事情重新动起来。	Ne_Chancellor
Z_Si_01	第三部分：宰相施政方式	宰相	Si	守恒性与不变性	我做事时会自然依赖过去验证过的流程、节奏和经验。	Si_Chancellor
Z_Si_02	第三部分：宰相施政方式	宰相	Si	守恒性与不变性	面对新局面，我会先找有没有可以复用的旧经验。	Si_Chancellor
Z_Se_01	第三部分：宰相施政方式	宰相	Se	在场性与现实性	我推进事情时，更愿意直接接触现场，在现实反馈中调整。	Se_Chancellor
Z_Se_02	第三部分：宰相施政方式	宰相	Se	在场性与现实性	比起把方案反复想完，我更常通过实际动作先把局面打开。	Se_Chancellor
Z_Fi_01	第三部分：宰相施政方式	宰相	Fi	本真性与统一性	我让事情继续下去的力量，常常来自内心过不过得去。	Fi_Chancellor
Z_Fi_02	第三部分：宰相施政方式	宰相	Fi	本真性与统一性	我会用真心、底线和自我统一来决定一件事还该不该继续。	Fi_Chancellor
Z_Fe_01	第三部分：宰相施政方式	宰相	Fe	关联性与互系性	我解决问题时，常常会先看人与人之间能不能重新接上。	Fe_Chancellor
Z_Fe_02	第三部分：宰相施政方式	宰相	Fe	关联性与互系性	我擅长通过回应、协调和照顾共同处境，让局面重新运转。	Fe_Chancellor
G_Ti_01	第四部分：护卫守门方式	护卫	Ti	自洽性与逻辑性（可理解性）	压力很大时，只要能把问题讲清楚，我就会稳定很多。	Ti_Guard
G_Ti_02	第四部分：护卫守门方式	护卫	Ti	自洽性与逻辑性（可理解性）	我常常靠分析、定义和解释，把混乱挡在外面。	Ti_Guard
G_Te_01	第四部分：护卫守门方式	护卫	Te	建构性与目的性	慌乱时，我会把事情变成待办事项、流程和现实安排。	Te_Guard
G_Te_02	第四部分：护卫守门方式	护卫	Te	建构性与目的性	只要还能推进一点结果、控制一点资源，我就不容易彻底失控。	Te_Guard
G_Ni_01	第四部分：护卫守门方式	护卫	Ni	涌现性与压缩性	遇到冲击时，我会试着给它找一个更深的方向或意义。	Ni_Guard
G_Ni_02	第四部分：护卫守门方式	护卫	Ni	涌现性与压缩性	只要能看出这件事最终指向哪里，我就会安定很多。	Ni_Guard
G_Ne_01	第四部分：护卫守门方式	护卫	Ne	创生性与可能性	只要还能找到新解释、新玩法或新出口，我就不容易被困死。	Ne_Guard
G_Ne_02	第四部分：护卫守门方式	护卫	Ne	创生性与可能性	压力来时，我会本能地打开更多可能，让自己有回旋空间。	Ne_Guard
G_Si_01	第四部分：护卫守门方式	护卫	Si	守恒性与不变性	压力大时，熟悉的环境、旧习惯或稳定节奏能让我恢复很多。	Si_Guard
G_Si_02	第四部分：护卫守门方式	护卫	Si	守恒性与不变性	只要能回到某种已知秩序里，我就不容易被外界冲散。	Si_Guard
G_Se_01	第四部分：护卫守门方式	护卫	Se	在场性与现实性	压力来时，出门、运动、处理现场或做点实际动作能让我缓过来。	Se_Guard
G_Se_02	第四部分：护卫守门方式	护卫	Se	在场性与现实性	只要身体和现实动起来，我就不容易一直困在脑子里。	Se_Guard
G_Fi_01	第四部分：护卫守门方式	护卫	Fi	本真性与统一性	外界冲击很强时，只要确认自己没有背叛内心，我就能稳住。	Fi_Guard
G_Fi_02	第四部分：护卫守门方式	护卫	Fi	本真性与统一性	我会通过守住真心、底线和自我一致来保护自己。	Fi_Guard
G_Fe_01	第四部分：护卫守门方式	护卫	Fe	关联性与互系性	被击中时，如果有人回应、理解、接住我，我会恢复很多。	Fe_Guard
G_Fe_02	第四部分：护卫守门方式	护卫	Fe	关联性与互系性	只要关系还在、大家还能互相回应，我就不容易崩掉。	Fe_Guard
E_Ti_01	第五部分：帝师合法性解释	帝师	Ti	自洽性与逻辑性（可理解性）	我能把混乱争论整理成一套清楚、可审查、能自己站住的结构。	Ti_EmperorTeacher
E_Ti_02	第五部分：帝师合法性解释	帝师	Ti	自洽性与逻辑性（可理解性）	我能说明一个判断为什么在逻辑上成立，而不只是说“我觉得有道理”。	Ti_EmperorTeacher
E_Te_01	第五部分：帝师合法性解释	帝师	Te	建构性与目的性	我能把资源、责任和压力组织成一个能承担结果的秩序。	Te_EmperorTeacher
E_Te_02	第五部分：帝师合法性解释	帝师	Te	建构性与目的性	我能说明一套安排为什么值得执行，而不只是因为它暂时有效。	Te_EmperorTeacher
E_Ni_01	第五部分：帝师合法性解释	帝师	Ni	涌现性与压缩性	我能从复杂局面中看出一个正在形成的深层方向。	Ni_EmperorTeacher
E_Ni_02	第五部分：帝师合法性解释	帝师	Ni	涌现性与压缩性	我能说明一个判断为什么代表事情的走向，而不只是我的预感。	Ni_EmperorTeacher
E_Ne_01	第五部分：帝师合法性解释	帝师	Ne	创生性与可能性	我能在已经僵住的局面里打开新的入口，让事情重新有可能。	Ne_EmperorTeacher
E_Ne_02	第五部分：帝师合法性解释	帝师	Ne	创生性与可能性	我能说明一个新分支为什么不是胡思乱想，而是秩序继续生成的机会。	Ne_EmperorTeacher
E_Si_01	第五部分：帝师合法性解释	帝师	Si	守恒性与不变性	我能指出变化中哪些东西必须被保留，不能被轻易抹掉。	Si_EmperorTeacher
E_Si_02	第五部分：帝师合法性解释	帝师	Si	守恒性与不变性	我能说明某些经验、记忆或传统为什么值得守住，而不只是因为习惯。	Si_EmperorTeacher
E_Se_01	第五部分：帝师合法性解释	帝师	Se	在场性与现实性	我能在混乱现场抓住现实切点，让局面重新进入可处理状态。	Se_EmperorTeacher
E_Se_02	第五部分：帝师合法性解释	帝师	Se	在场性与现实性	我能说明为什么必须回到现场和现实接触，而不是一直停在远处判断。	Se_EmperorTeacher
E_Fi_01	第五部分：帝师合法性解释	帝师	Fi	本真性与统一性	我能在外部压力和妥协中，重新找到人格统一的位置。	Fi_EmperorTeacher
E_Fi_02	第五部分：帝师合法性解释	帝师	Fi	本真性与统一性	我能说明一条底线为什么不是任性，而是良知和自我统一的要求。	Fi_EmperorTeacher
E_Fe_01	第五部分：帝师合法性解释	帝师	Fe	关联性与互系性	我能让断裂的人、关系和处境重新进入可以共同承载的世界。	Fe_EmperorTeacher
E_Fe_02	第五部分：帝师合法性解释	帝师	Fe	关联性与互系性	我能说明仁爱、关系和共同处境为什么不是表面和气，而是秩序成立的条件。	Fe_EmperorTeacher
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
