# -*- coding: utf-8 -*-
"""Streamlit entrypoint for 神性论人格王国测评 v0.8 structure."""
import importlib
import sys

# 旧版曾把 backend_v07 注入为 sys.modules['backend']，Streamlit rerun/reload 时会让
# backend_v07 误从自己导入 build_submission_row，造成递归。这里清掉该别名，
# app_v07 直接从 backend_v07 导入兼容层。
backend_module = sys.modules.get("backend")
if getattr(backend_module, "__name__", "") == "backend_v07":
    del sys.modules["backend"]

# Streamlit reruns keep imported modules in memory. Reload the data/scoring/backend
# modules first so page reruns always use the newest GitHub-deployed question set.
for module_name in ["backend", "backend_v07", "data_v07", "scoring_v07", "app_v07"]:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])

if "app_v07" not in sys.modules:
    import app_v07
