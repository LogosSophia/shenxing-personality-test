# -*- coding: utf-8 -*-
"""Streamlit entrypoint for 神性论人格王国测评 v0.7 beta."""
import importlib
import sys

import backend_v07

sys.modules["backend"] = backend_v07

# Streamlit reruns keep imported modules in memory. Reload the data/scoring
# modules first so page reruns always use the newest GitHub-deployed question set.
for module_name in ["data_v07", "scoring_v07", "app_v07"]:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])

if "app_v07" not in sys.modules:
    import app_v07
