import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="COLDGUARD AI",
    page_icon="🥭",
    layout="wide"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0b1f3a, #123d6a);
    padding: 28px 32px;
    border-radius: 14px;
    margin-bottom: 25px;
    color: white;
}

.main-header h1 {
    margin: 0;
    font-size: 34px;
    font-weight: 700;
}

.main-header p {
    margin-top: 8px;
    font-size: 16px;
    color: #dce8f5;
}

/* KPI cards */
.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e1e7ef;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    text-align: center;
}

.kpi-title {
    color: #667085;
    font-size: 14px;
    margin-bottom: 8px;
}

.kpi-value {
    color: #0b1f3a;
    font-size: 30px;
    font-weight: 700;
}

/* Section title */
.section-title {
    color: #0b1f3a;
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 12px;
}

/* Risk boxes */
.risk-high {
    background-color: #fff1f0;
    border-left: 6px solid #d92d20;
    padding: 18px;
    border-radius: 8px;
}

.risk-warning {
    background-color: #fffaeb;
    border-left: 6px solid #f79009;
    padding: 18px;
    border-radius: 8px;
}

.risk-normal {
    background-color: #ecfdf3;
    border-left: 6px solid #12b76a;
    padding: 18px;
    border-radius: 8px;
}

.footer {
    text-align: center;
    color: #667085;
    font-size: 13px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# DỮ LIỆU MÔ PHỎNG
# =========================
data = pd.DataFrame({
    "Container": ["MG001", "MG002", "MG003", "MG004", "MG005"],
    "Nhiệt độ (°C)": [4.2, 5.1, 6.3, 4.8, 8.9],
    "Độ ẩm (%)": [82, 85, 88, 80, 94],
    "Thời gian chờ (giờ)": [18, 24, 31, 20, 52],
    "Risk Score": [18, 35, 58, 27, 87],
    "Phân loại": [
        "Normal",
        "Normal",
        "Warning",
        "Normal",
        "High Risk"
    ]
})


# =========================
# HÀM TÍNH RISK SCORE
# =========================
def calculate_risk(temp, humidity, waiting, refrigeration):

    score = 0
    reasons = []

    # Nhiệt độ
    if temp > 8:
        score += 35
        reasons.append("Nhiệt độ vượt ngưỡng bảo quản an toàn")
    elif temp > 6:
        score += 20
        reasons.append("Nhiệt độ có xu hướng tăng")

    # Độ ẩm
    if humidity > 90:
        score += 25
        reasons.append("Độ ẩm rất cao")
    elif humidity > 85:
        score += 15
        reasons.append("Độ ẩm tăng")

    # Thời gian chờ
    if waiting > 48:
        score += 30
        reasons.append("Thời gian chờ kéo dài")
    elif waiting > 30:
        score += 15
        reasons.append("Thời gian chờ tương đối dài")

    # Thiết bị lạnh
    if refrigeration == "Bất thường":
        score += 20
        reasons.append("Thiết bị làm lạnh có dấu hiệu bất thường")

    score = min(score, 100)

    if score >= 70:
        classification = "HIGH RISK"
    elif score >= 40:
        classification = "WARNING"
    else:
        classification = "NORMAL"

    return score, classification, reasons


# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-header">
    <h1>🥭 COLDGUARD AI</h1>
    <p>AI-POWERED COLD CHAIN RISK MANAGEMENT</p>
    <p>Lào Cai International Border Gate • Prototype</p>
</div>
""", unsafe_allow_html=True)


# =========================
# TABS
# =========================
tab1, tab2 = st.tabs([
    "📊 Dashboard",
    "🥭 Case Study – Xuất khẩu xoài"
])


# ==========================================================
# TAB 1 — DASHBOARD
# ==========================================================
with tab1:

    st.markdown(
        '<div class="section-title">Tổng quan rủi ro chuỗi lạnh</div>',
        unsafe_allow_html=True
    )

    total = len(data)
    normal = len(data[data["Phân loại"] == "Normal"])
    warning = len(data[data["Phân loại"] == "Warning"])
    high = len(data[data["Phân loại"] == "High Risk"])
    average = round(data["Risk Score"].mean(), 1)

    # KPI
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Tổng container</div>
            <div class="kpi-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Normal</div>
            <div class="kpi-value">{normal}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Warning</div>
            <div class="kpi-value">{warning}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">High Risk</div>
            <div class="kpi-value">{high}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Risk Score TB</div>
            <div class="kpi-value">{average}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # BIỂU ĐỒ
    # =========================
    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="section-title">Risk Score theo container</div>',
            unsafe_allow_html=True
        )

        fig_bar = px.bar(
            data,
            x="Container",
            y="Risk Score",
            text="Risk Score",
            labels={
                "Container": "Container",
                "Risk Score": "Risk Score"
            }
        )

        fig_bar.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(range=[0, 100])
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:

        st.markdown(
            '<div class="section-title">Phân loại rủi ro</div>',
            unsafe_allow_html=True
        )

        risk_count = data["Phân loại"].value_counts().reset_index()
        risk_count.columns = ["Phân loại", "Số lượng"]

        fig_pie = px.pie(
            risk_count,
            names="Phân loại",
            values="Số lượng",
            hole=0.45
        )

        fig_pie.update_layout(
            paper_bgcolor="white"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    # =========================
    # BẢNG GIÁM SÁT
    # =========================
    st.markdown(
        '<div class="section-title">Danh sách container đang giám sát</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# TAB 2 — CASE STUDY
# ==========================================================
with tab2:

    st.markdown(
        '<div class="section-title">Mô phỏng: 01 container xoài xuất khẩu</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Nhập các thông số thực tế của container để mô phỏng "
        "cơ chế đánh giá rủi ro chuỗi lạnh."
    )

    col1, col2 = st.columns(2)

    with col1:

        temperature = st.number_input(
            "🌡️ Nhiệt độ (°C)",
            min_value=0.0,
            max_value=20.0,
            value=8.9,
            step=0.1
        )

        humidity = st.number_input(
            "💧 Độ ẩm (%)",
            min_value=0,
            max_value=100,
            value=94,
            step=1
        )

    with col2:

        waiting = st.number_input(
            "⏱️ Thời gian chờ (giờ)",
            min_value=0,
            max_value=200,
            value=52,
            step=1
        )

        refrigeration = st.selectbox(
            "❄️ Tình trạng thiết bị lạnh",
            ["Bình thường", "Bất thường"]
        )

    st.write("")

    analyze = st.button(
        "🔍 PHÂN TÍCH RỦI RO",
        use_container_width=True
    )

    if analyze:

        score, classification, reasons = calculate_risk(
            temperature,
            humidity,
            waiting,
            refrigeration
        )

        st.markdown("---")

        # =========================
        # KẾT QUẢ
        # =========================
        if classification == "HIGH RISK":

            st.markdown(f"""
            <div class="risk-high">
                <h2>🔴 HIGH RISK</h2>
                <h3>Risk Score: {score}/100</h3>
                <p>Container có nguy cơ cao đối với chất lượng hàng hóa.</p>
            </div>
            """, unsafe_allow_html=True)

        elif classification == "WARNING":

            st.markdown(f"""
            <div class="risk-warning">
                <h2>🟠 WARNING</h2>
                <h3>Risk Score: {score}/100</h3>
                <p>Container cần được theo dõi và kiểm tra.</p>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="risk-normal">
                <h2>🟢 NORMAL</h2>
                <h3>Risk Score: {score}/100</h3>
                <p>Container đang trong trạng thái tương đối ổn định.</p>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # =========================
        # NGUYÊN NHÂN
        # =========================
        st.markdown(
            '<div class="section-title">⚠️ Các yếu tố rủi ro phát hiện</div>',
            unsafe_allow_html=True
        )

        if reasons:

            for reason in reasons:
                st.write("• " + reason)

        else:

            st.write("Chưa phát hiện yếu tố rủi ro đáng kể.")

        # =========================
        # KHUYẾN NGHỊ
        # =========================
        st.markdown(
            '<div class="section-title">💡 Khuyến nghị xử lý</div>',
            unsafe_allow_html=True
        )

        if classification == "HIGH RISK":

            st.error(
                "Ưu tiên kiểm tra nguồn điện và thiết bị làm lạnh; "
                "ưu tiên xử lý container; cân nhắc chuyển hàng vào "
                "khu vực bảo quản phù hợp; tăng tần suất theo dõi nhiệt độ."
            )

        elif classification == "WARNING":

            st.warning(
                "Theo dõi sát nhiệt độ và độ ẩm; kiểm tra tình trạng "
                "thiết bị lạnh; ưu tiên xử lý nếu thời gian chờ tiếp tục tăng."
            )

        else:

            st.success(
                "Tiếp tục theo dõi các chỉ số nhiệt độ, độ ẩm và thời gian chờ."
            )


# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    COLDGUARD AI • Cold Chain Risk Management Prototype<br>
    Phục vụ mục đích mô phỏng và minh họa mô hình
</div>
""", unsafe_allow_html=True)
