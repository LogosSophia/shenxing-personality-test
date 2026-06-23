# -*- coding: utf-8 -*-
"""Streamlit entrypoint for 神性论人格王国测评 v0.7 beta."""
import sys
import backend_v07

sys.modules["backend"] = backend_v07
import app_v07
