import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')  # 또는 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# 데이터 (5% 미만은 기타로 합친 버전)
data = {
    "미래 도시 희망상 (1순위)": {
        "경제도시": 26.8, "교육도시": 17.1, "문화도시": 22.3,
        "복지도시": 9.5, "건강도시": 5.0, "안전도시": 5.6, "환경도시": 5.9, "기타": 7.8
    },
    "운동경기장 관람 응답자 나이대별 비율": {
        "20대": 25.7, "30대": 28.0, "40대": 22.0, "50대": 12.4,
        "60대": 6.8, "기타": 4.9
    },
    "문화활동 응답 비율": {
        "극장에서 영화 관람": 25.3, "활동 없음": 16.9, "야외문화행사": 15.6,
        "박물관 관람": 8.6, "운동경기장 관람": 7.7, "연극공연": 7.5,
        "대중공연": 7.2, "기타": 8.2
    },
    "현재 귀하가 느끼는 수원시의 이미지": {
        "역사와 전통이 살아 있는 도시": 34.9, "주거와 교통이 편리한 도시": 18.1,
        "교육문화 인프라가 좋은 도시": 14.5, "첨단 산업이 발달한 도시": 13.5,
        "행정 중심 도시": 8.2, "활기찬 상업과 소비 도시": 6.4, "기타": 4.5
    },
    "수원시민으로서 자부심을 느끼는 이유": {
        "수원화성 등 역사문화유산": 33.5, "삼성전자 등 글로벌 기업 본사": 24.7,
        "주거환경과 교통 인프라": 20.5, "문화예술·스포츠 인프라": 13.0, "기타": 8.3
    }
}

# 차트 저장
colors = [
    '#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0',
    '#ffb3e6','#c2f0c2','#f0c2c2','#b3e6ff','#e6b3b3'
]

for i, (title, values) in enumerate(data.items(), start=1):
    # 4번 차트만 라벨 폰트 크기와 도넛 두께 조정
    if i == 4:
        # 긴 라벨 자동 줄바꿈 함수
        def wrap_label(label, width=10):
            import textwrap
            return '\n'.join(textwrap.wrap(label, width))

        wrapped_labels = [wrap_label(lbl, 10) for lbl in values.keys()]
        fig, ax = plt.subplots(figsize=(8,8))  # 원형 더 크게
        wedges, texts, autotexts = ax.pie(
            values.values(),
            labels=wrapped_labels,
            autopct="%.1f%%",
            startangle=90,
            colors=colors[:len(values)],
            wedgeprops={"edgecolor": "white", "linewidth": 2, "alpha": 0.9},
            textprops={"fontsize": 12, "weight": "bold"},  # 볼드체
            pctdistance=0.85  # %를 도넛 중심에서 더 멀리
        )
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_weight('normal')
        centre_circle = plt.Circle((0,0),0.70,fc='white')  # 도넛 두께 얇게
        fig.gca().add_artist(centre_circle)
        ax.set_title(title, fontsize=18, fontweight='bold', color='#333333', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(f"분석결과_{i}.png", bbox_inches="tight", dpi=150)
        plt.close(fig)
    else:
        fig, ax = plt.subplots(figsize=(7,7))
        wedges, texts, autotexts = ax.pie(
            values.values(),
            labels=values.keys(),
            autopct="%.1f%%",
            startangle=90,
            colors=colors[:len(values)],
            wedgeprops={"edgecolor": "white", "linewidth": 2, "alpha": 0.9},
            textprops={"fontsize": 14, "weight": "bold"},
            pctdistance=0.75
        )
        for autotext in autotexts:
            autotext.set_fontsize(11)
            autotext.set_weight('normal')
        centre_circle = plt.Circle((0,0),0.60,fc='white')
        fig.gca().add_artist(centre_circle)
        ax.set_title(title, fontsize=18, fontweight='bold', color='#333333', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(f"분석결과_{i}.png", bbox_inches="tight", dpi=150)
        plt.close(fig)