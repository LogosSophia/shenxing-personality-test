# -*- coding: utf-8 -*-
import csv
from data import QUESTIONS

fields = [
    "module",
    "qid",
    "position",
    "dimension",
    "principle",
    "front_text",
    "scoring_key",
]

with open("questions_export.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for q in QUESTIONS:
        writer.writerow({field: q.get(field, "") for field in fields})

print(f"已导出 {len(QUESTIONS)} 题到 questions_export.csv")
