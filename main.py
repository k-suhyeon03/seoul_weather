import streamlit as st
import pandas as pd

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    # 연도별 평균기온 계산
    yearly = (
        df.dropna(subset=["평균기온"])
        .groupby("연도")["평균기온"]
        .mean()
        .reset_index()
    )

    yearly["평균기온"] = yearly["평균기온"].round(2)

    return yearly


# --------------------------------------------------
# 제목
# --------------------------------------------------

st.title("🌡️ 서울의 100년 기온 변화")
st.subheader("연평균 기온은 지난 100여 년 동안 어떻게 변해 왔을까요?")

st.write(
    "서울의 일별 평균기온 자료를 연도별로 평균 내어 "
    "장기간의 기온 변화를 한눈에 확인할 수 있습니다."
)


# --------------------------------------------------
# 데이터 처리
# --------------------------------------------------

try:
    yearly_data = load_data()

    # 분석 가능한 기간
    min_year = int(yearly_data["연도"].min())
    max_year = int(yearly_data["연도"].max())

    st.caption(
        f"분석 기간: {min_year}년 ~ {max_year}년"
    )

    # --------------------------------------------------
    # 그래프
    # --------------------------------------------------

    st.markdown("### 📈 연평균 기온 변화")

    chart_data = yearly_data.set_index("연도")

    st.line_chart(
        chart_data["평균기온"],
        y_label="평균기온 (℃)",
        x_label="연도",
        height=500
    )

    # --------------------------------------------------
    # 간단한 수치 정보
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    first_year = yearly_data.iloc[0]
    last_year = yearly_data.iloc[-1]

    temperature_change = (
        last_year["평균기온"] - first_year["평균기온"]
    )

    with col1:
        st.metric(
            "가장 오래된 연도",
            f"{int(first_year['연도'])}년",
            f"{first_year['평균기온']:.2f} ℃"
        )

    with col2:
        st.metric(
            "가장 최근 연도",
            f"{int(last_year['연도'])}년",
            f"{last_year['평균기온']:.2f} ℃"
        )

    with col3:
        st.metric(
            "두 시점의 평균기온 차이",
            f"{temperature_change:+.2f} ℃"
        )

    # --------------------------------------------------
    # 데이터 표
    # --------------------------------------------------

    with st.expander("📋 연도별 평균기온 데이터 보기"):
        st.dataframe(
            yearly_data,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
