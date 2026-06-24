# -*- coding: utf-8 -*-
"""v0.8 后台兼容层。"""
from backend import build_submission_row as _build_submission_row
from backend import save_submission


def build_submission_row(*args, **kwargs):
    row = _build_submission_row(*args, **kwargs)
    row["schema_version"] = "v0.8.1-pressure-collab"
    return row
