# -*- coding: utf-8 -*-
"""Streamlit entrypoint for 神性论人格王国测评 v0.7 beta."""
import importlib
import sys

import backend_v07

sys.modules["backend"] = backend_v07

if "app_v07" in sys.modules:
    importlib.reload(sys.modules["app_v07"])
else:
    import app_v07
