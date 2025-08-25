# -*- coding: utf-8 -*-
"""
수원시 패널조사 Q10, Q17-1 원형 그래프 (한글 폰트 자동 설정)
- 방법 A: CSV로 바로 시각화
- 방법 B: 원본 엑셀(데이터 + 코드북)에서 집계 후 시각화
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# -------------------------------
# 0) 한글 폰트 자동 설정 (Windows / macOS / Linux 대응)
# -------------------------------
CANDIDATE_FONTS = [
    "Malgun Gothic",      # Windows
    "AppleGothic",        # macOS
    "NanumGothic",        # Linux/개발환경
    "Noto Sans CJK KR",   # Google Noto
    "Noto Sans KR",       # Google Noto (대체)
    "NanumSquare",        # 추가 후보
]

def set_korean_font():
    available = set(f.name for f in fm.fontManager.ttflist)
    chosen = None
    for name in CANDIDATE_FONTS:
        if name in available:
            chosen = name
            break
    if chosen:
        plt.rcParams["font.family"] = chosen
        plt.rcParams["axes.unicode_minus"] = False
        print(f"[INFO] 한글 폰트 적용: {chosen}")
    else:
        print("[WARN] 시스템에 한글 폰트가 감지되지 않았습니다.")
        print("       Windows: '맑은 고딕' / macOS: 'AppleGothic' / Linux: 'NanumGothic' 권장")
        plt.rcParams["axes.unicode_minus"] = False

set_korean_font()

# -------------------------------
# 공통 유틸
# -------------------------------
def group_minor(series_perc: pd.Series, threshold=5.0) -> pd.Series:
    """5% 미만 항목을 '기타'로 합산."""
    series_perc = pd.to_numeric(series_perc, errors="coerce").dropna()
    major = series_perc[series_perc >= threshold].copy()
    minor_sum = series_perc[series_perc < threshold].sum()
    if minor_sum > 0:
        major.loc["기타"] = round(minor_sum, 1)
    return major

def plot_pie_from_series(percents: pd.Series, title: str, save_path: str = None):
    """
    percents: index=항목(한글), values=비율(%)
    - 바깥: 항목 라벨
    - 안쪽: 퍼센트
    - 여백/잘림 보강
    """
    import numpy as np
    s = pd.to_numeric(percents, errors="coerce").dropna()
    if s.empty or s.sum() == 0:
        print(f"[WARN] '{title}' 시각화할 데이터가 없습니다.")
        return

    s = s.sort_values(ascending=False)
    labels = list(s.index)
    sizes  = s.values

    # 라벨 글자 수가 길면 폰트 자동으로 조금 줄이기
    max_len = max(len(str(x)) for x in labels)
    label_fs = 13 if max_len <= 10 else (12 if max_len <= 16 else 11)

    # 여백 문제 최소화: constrained_layout + 넉넉한 figsize
    fig = plt.figure(figsize=(9, 9), constrained_layout=True)
    ax = fig.add_subplot(111)

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        startangle=90,
        autopct="%1.1f%%",
        pctdistance=0.70,     # 퍼센트 위치(조금 안쪽)
        labeldistance=1.12,   # 라벨 위치(조금 바깥)
        wedgeprops=dict(width=0.96)
    )

    # 폰트/색상 정리
    for t in texts:
        t.set_fontsize(label_fs)
    for at in autotexts:
        at.set_fontsize(12)
        at.set_color("#333")

    ax.set_title(title, fontsize=18, pad=22)
    ax.axis("equal")

    # 추가 여백 확보
    # (tight_layout보다 더 강하게 자르지 않고 여백 포함)
    if save_path:
        # 캔버스 여백 + 라벨 잘림 방지
        plt.savefig(save_path, dpi=300, bbox_inches="tight", pad_inches=0.8)
        print(f"[SAVE] {save_path}")
        plt.close(fig)
    else:
        # 화면 표시 시에도 테두리 여유
        plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.02)
        plt.show()


# ===============================================================
# 방법 A) CSV로 바로 시각화
# ===============================================================
def visualize_from_csv(csv_path: str):
    """
    CSV 형식:
    문항, 항목, 비율(%)
    Q10, ..., ...
    Q17-1, ..., ...
    """
    df = pd.read_csv(csv_path)  # 필요 시 encoding="utf-8-sig"
    for q in df["문항"].unique():
        sub_df = df[df["문항"] == q][["항목", "비율(%)"]].copy()
        sub_df["비율(%)"] = pd.to_numeric(sub_df["비율(%)"], errors="coerce")
        sub = sub_df.set_index("항목")["비율(%)"].dropna()
        title = "Q10. 현재 귀하가 느끼는 수원시의 이미지는 어떤가요?" if q == "Q10" \
                else "Q17-1. 수원시민으로서 자부심을 느끼는 이유"
        plot_pie_from_series(sub, title, save_path=f"{q}_pie.png")

# ===============================================================
# 방법 B) 원본 엑셀에서 집계 → 5% 미만 '기타' → 시각화
# ===============================================================
def parse_choices(text: str):
    """
    코드북 '변수값/단위'에서
    '① 항목명\\n② 항목명 ...' → {1:'항목명', 2:'항목명', ...}
    """
    lines = [ln.strip() for ln in str(text).split("\n") if ln.strip()]
    mapping = {}
    for i, line in enumerate(lines, start=1):
        mapping[i] = line[2:].strip() if len(line) >= 2 else line
    return mapping

def visualize_from_excel(data_path: str, codebook_path: str):
    data = pd.read_excel(data_path)
    codebook = pd.read_excel(codebook_path, sheet_name=None)["code"]

    q10_row = codebook[codebook["변수명"] == "q10"].iloc[0]
    q17_1_row = codebook[codebook["변수명"] == "q17_1"].iloc[0]
    q10_map   = parse_choices(q10_row["변수값/단위"])
    q17_1_map = parse_choices(q17_1_row["변수값/단위"])

    # Q10
    q10 = data[["q10", "WT"]].dropna()
    q10_counts = q10.groupby("q10")["WT"].sum().rename(index=q10_map)
    q10_perc = (q10_counts / q10_counts.sum() * 100).round(1)
    q10_final = group_minor(q10_perc, threshold=5.0)
    plot_pie_from_series(q10_final, "Q10. 현재 귀하가 느끼는 수원시의 이미지는 어떤가요?", "Q10_pie.png")

    # Q17-1
    q17_1 = data[["q17_1", "WT"]].dropna()
    q17_1_counts = q17_1.groupby("q17_1")["WT"].sum().rename(index=q17_1_map)
    q17_1_perc = (q17_1_counts / q17_1_counts.sum() * 100).round(1)
    q17_1_final = group_minor(q17_1_perc, threshold=5.0)
    plot_pie_from_series(q17_1_final, "Q17-1. 수원시민으로서 자부심을 느끼는 이유", "Q17-1_pie.png")

# ======================
# 실행부
# ======================
if __name__ == "__main__":
    # --- 방법 A: CSV로 바로 ---
    csv_file = "Q10_Q17-1_results.csv"   # <== CSV 경로로 수정 가능
    if os.path.exists(csv_file):
        visualize_from_csv(csv_file)
    else:
        print(f"[INFO] CSV가 없으면 방법 B(엑셀에서 집계)로 진행합니다: {csv_file}")

    # --- 방법 B: 엑셀에서 집계 ---
    # 원본에서부터 다시 집계하고 싶으면 아래 두 경로를 맞춰서 사용 (주석 해제)
    # data_xlsx = "(공개용)2025년 2분기 패널조사_데이터(가중치).xlsx"
    # codebook_xlsx = "2025년 2분기 패널조사_코드북.xlsx"
    # if os.path.exists(data_xlsx) and os.path.exists(codebook_xlsx):
    #     visualize_from_excel(data_xlsx, codebook_xlsx)
    # else:
    #     print("[HINT] 원본 엑셀에서 집계하려면 data_xlsx / codebook_xlsx 경로를 맞춰주세요.")
