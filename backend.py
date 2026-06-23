# -*- coding: utf-8 -*-
"""后台记录模块。"""
from __future__ import annotations

import csv
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

import streamlit as st

HEADERS = [
    "submitted_at_utc", "submission_id", "schema_version", "top_type", "level",
    "confidence", "gap", "second_type", "monarch", "chancellor", "guard",
    "civilian", "emperor", "marshal", "monarch_raw", "chancellor_score",
    "guard_score", "civilian_score", "emperor_score", "marshal_score", "type_score",
    "risk_titles", "mbti_past", "mbti_self", "answers_json", "type_scores_json", "risks_json",
]


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def build_submission_row(
    answers: Dict[str, int],
    result: Dict[str, Any],
    mbti_past: str = "",
    mbti_self: str = "",
    submission_id: str | None = None,
) -> Dict[str, Any]:
    top_type = result["top_type"]
    detail = result["detail"][top_type]
    type_map = result["map"]
    risks = result.get("risks", [])
    return {
        "submitted_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "submission_id": submission_id or str(uuid.uuid4()),
        "schema_version": "v0.6",
        "top_type": top_type,
        "level": result["level"],
        "confidence": result["confidence"],
        "gap": round(float(result["gap"]), 6),
        "second_type": result.get("second_type", ""),
        "monarch": type_map["monarch"],
        "chancellor": type_map["chancellor"],
        "guard": type_map["guard"],
        "civilian": type_map["civilian"],
        "emperor": type_map["emperor"],
        "marshal": type_map["marshal"],
        "monarch_raw": round(float(detail["monarch_raw"]), 6),
        "chancellor_score": round(float(detail["chancellor"]), 6),
        "guard_score": round(float(detail["guard"]), 6),
        "civilian_score": round(float(detail["civilian"]), 6),
        "emperor_score": round(float(detail["emperor"]), 6),
        "marshal_score": round(float(detail["marshal"]), 6),
        "type_score": round(float(detail["score"]), 6),
        "risk_titles": "；".join(risk.get("title", "") for risk in risks),
        "mbti_past": mbti_past.strip(),
        "mbti_self": mbti_self.strip(),
        "answers_json": _json_dumps(answers),
        "type_scores_json": _json_dumps(result["type_scores"]),
        "risks_json": _json_dumps(risks),
    }


def _get_secret_section(name: str):
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def _to_plain_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return {k: _to_plain_dict(v) if isinstance(v, dict) else v for k, v in value.items()}
    try:
        return dict(value)
    except Exception:
        return {}


def _save_to_google_sheets(row: Dict[str, Any]) -> Tuple[bool, str]:
    gsheets_cfg = _get_secret_section("gsheets")
    service_account_cfg = _get_secret_section("gcp_service_account")
    if not gsheets_cfg or not service_account_cfg:
        return False, "Google Sheets secrets not configured."
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as exc:
        return False, f"Google Sheets dependency missing: {exc}"

    gsheets_cfg = _to_plain_dict(gsheets_cfg)
    service_account_info = _to_plain_dict(service_account_cfg)
    spreadsheet_id = gsheets_cfg.get("spreadsheet_id")
    worksheet_name = gsheets_cfg.get("worksheet_name", "Submissions")
    if not spreadsheet_id:
        return False, "gsheets.spreadsheet_id is missing."

    key_name = "private" + "_key"
    if key_name in service_account_info:
        service_account_info[key_name] = service_account_info[key_name].replace("\\n", "\n")

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    try:
        credentials = Credentials.from_service_account_info(service_account_info, scopes=scopes)
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(spreadsheet_id)
        try:
            worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=len(HEADERS))
            worksheet.append_row(HEADERS, value_input_option="RAW")
        first_row = worksheet.row_values(1)
        if not first_row:
            worksheet.append_row(HEADERS, value_input_option="RAW")
        worksheet.append_row([row.get(header, "") for header in HEADERS], value_input_option="USER_ENTERED")
        return True, "saved_to_google_sheets"
    except Exception as exc:
        return False, f"Google Sheets save failed: {exc}"


def _save_to_local_csv(row: Dict[str, Any]) -> Tuple[bool, str]:
    try:
        output_dir = Path("submissions")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "submissions.csv"
        exists = output_path.exists()
        with output_path.open("a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            if not exists:
                writer.writeheader()
            writer.writerow({header: row.get(header, "") for header in HEADERS})
        return True, "saved_to_local_csv"
    except Exception as exc:
        return False, f"Local CSV save failed: {exc}"


def save_submission(row: Dict[str, Any]) -> Dict[str, Any]:
    ok, message = _save_to_google_sheets(row)
    if ok:
        return {"ok": True, "backend": "google_sheets", "message": message}
    fallback_ok, fallback_message = _save_to_local_csv(row)
    if fallback_ok:
        return {"ok": True, "backend": "local_csv", "message": f"{fallback_message}; persistent backend unavailable: {message}"}
    return {"ok": False, "backend": "none", "message": f"{message}; {fallback_message}"}
