import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="COLDGUARD AI",
    page_icon="❄️",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }

    .header {
        background: linear-gradient(135deg, #0b1f3a, #164a7b);
        padding: 28px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
    }

    .header h1 {
        margin: 0;
        font-size: 34px;
    }

    .header p {
        margin-top: 8px;
        font-size: 16px;
        opacity: 0.9;
    }

    .kpi {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .kpi-title {
        color: #666;
        font-size: 14px;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: bold;
        color: #0b1f3a;
    }

    .risk-high {
        color: #d62728;
        font-weight: bold;
    }

    .risk-warning {
        color: #e6a700;
        font-weight: bold;
    }

    .risk-normal {
        color: #198754;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="header">
    <h1>❄️ COLDGUARD AI</h1>
    <p>AI-POWERED COLD CHAIN RISK MANAGEMENT</p>
    <p>Giám sát và dự báo rủi ro chuỗi lạnh hàng hóa xuất khẩu</p>
</div>
""", unsafe_allow_html=True)

# =========================
# HÀM TÍNH RISK SCORE
# =========================
def calculate_risk(temp, humidity, waiting, refrigeration):

    score = 0
    reasons = []

    # Nhiệt độ
    if temp > 8:
        score += 35
        reasons.append("Nhiệt độ vượt ngưỡng an toàn")
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

    # Hệ thống làm lạnh
    if refrigeration == "Bất thường":
        score += 20
        reasons.append("Hệ thống làm lạnh bất thường")

    score = min(score, 100)

    if score >= 70:
        status = "High Risk"
    elif score >= 40:
        status = "Warning"
    else:
        status = "Normal"

    return score, status, reasons


# =========================
# DỮ LIỆU MẪU
# =========================
sample_data = pd.DataFrame({
    "Container": ["MG001", "MG002", "MG003", "MG004", "MG005"],
    "Nhiệt độ (°C)": [4.2, 5.1, 6.3, 4.8, 8.9],
    "Độ ẩm (%)": [82, 85, 88, 80, 94],
    "Thời gian chờ (giờ)": [18, 24, 31, 20, 52],
    "Làm lạnh": [
        "Bình thường",
        "Bình thường",
        "Bình thường",
        "Bình thường",
        "Bất thường"
    ]
})


# =========================
# SIDEBAR - DỮ LIỆU
# =========================
st.sidebar.header("📂 DỮ LIỆU")

uploaded_file = st.sidebar.file_uploader(
    "Tải dữ liệu Excel hoặc CSV",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    try:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.sidebar.success("Đã tải dữ liệu thành công!")

    except Exception as e:
        st.sidebar.error("Không thể đọc file dữ liệu.")
        data = sample_data.copy()

else:

    data = sample_data.copy()

    st.sidebar.info(
        "Đang sử dụng dữ liệu mô phỏng COLDGUARD AI."
    )


# =========================
# KIỂM TRA / TÍNH TOÁN
# =========================
required_columns = [
    "Container",
    "Nhiệt độ (°C)",
    "Độ ẩm (%)",
    "Thời gian chờ (giờ)",
    "Làm lạnh"
]

missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:

    st.error(
        "File dữ liệu thiếu các cột: "
        + ", ".join(missing_columns)
    )

    st.stop()


risk_scores = []
statuses = []

for _, row in data.iterrows():

    score, status, reasons = calculate_risk(
        row["Nhiệt độ (°C)"],
        row["Độ ẩm (%)"],
        row["Thời gian chờ (giờ)"],
        row["Làm lạnh"]
    )

    risk_scores.append(score)
    statuses.append(status)

data["Risk Score"] = risk_scores
data["Phân loại"] = statuses


# =========================
# TABS
# =========================
tab1, tab2 = st.tabs([
    "📊 DASHBOARD",
    "🥭 CASE STUDY"
])


# =====================================================
# DASHBOARD
# =====================================================
with tab1:

    st.subheader("📊 Tổng quan rủi ro chuỗi lạnh")

    total = len(data)

    normal = len(
        data[data["Phân loại"] == "Normal"]
    )

    warning = len(
        data[data["Phân loại"] == "Warning"]
    )

    high = len(
        data[data["Phân loại"] == "High Risk"]
    )

    avg_risk = data["Risk Score"].mean()

    # KPI
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric("📦 Tổng Container", total)

    with c2:
        st.metric("🟢 Normal", normal)

    with c3:
        st.metric("🟡 Warning", warning)

    with c4:
        st.metric("🔴 High Risk", high)

    with c5:
        st.metric(
            "⚠️ Risk Score TB",
            f"{avg_risk:.1f}"
        )

    st.divider()

    # =========================
    # BIỂU ĐỒ
    # =========================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Risk Score theo Container")

        chart = px.bar(
            data,
            x="Container",
            y="Risk Score",
            text="Risk Score",
            title="Mức độ rủi ro"
        )

        chart.update_traces(
            textposition="outside"
        )

        chart.update_layout(
            yaxis_range=[0, 100]
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    with col2:

        st.subheader("📊 Phân loại rủi ro")

        status_count = (
            data["Phân loại"]
            .value_counts()
            .reset_index()
        )

        status_count.columns = [
            "Phân loại",
            "Số lượng"
        ]

        pie = px.pie(
            status_count,
            names="Phân loại",
            values="Số lượng",
            hole=0.45
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

    # =========================
    # BẢNG XẾP HẠNG
    # =========================

    st.subheader("🏆 Xếp hạng Container theo mức độ rủi ro")

    ranking = data.sort_values(
        "Risk Score",
        ascending=False
    ).reset_index(drop=True)

    ranking.index = ranking.index + 1

    st.dataframe(
        ranking,
        use_container_width=True
    )

    # Container nguy hiểm nhất
    highest = ranking.iloc[0]

    st.warning(
        f"⚠️ Container cần ưu tiên xử lý: "
        f"**{highest['Container']}** "
        f"— Risk Score **{highest['Risk Score']}** "
        f"— {highest['Phân loại']}"
    )


# =====================================================
# CASE STUDY
# =====================================================
with tab2:

    st.subheader(
        "🥭 Case Study – Xuất khẩu xoài tại cửa khẩu Lào Cai"
    )

    st.write(
        "Nhập thông số container để COLDGUARD AI "
        "mô phỏng đánh giá rủi ro."
    )

    col1, col2 = st.columns(2)

    with col1:

        container_id = st.text_input(
            "Mã Container",
            "MG006"
        )

        temperature = st.number_input(
            "🌡️ Nhiệt độ (°C)",
            min_value=0.0,
            max_value=20.0,
            value=8.0,
            step=0.1
        )

        humidity = st.number_input(
            "💧 Độ ẩm (%)",
            min_value=0.0,
            max_value=100.0,
            value=90.0,
            step=1.0
        )

    with col2:

        waiting = st.number_input(
            "⏱️ Thời gian chờ (giờ)",
            min_value=0.0,
            max_value=200.0,
            value=48.0,
            step=1.0
        )

        refrigeration = st.selectbox(
            "❄️ Trạng thái làm lạnh",
            [
                "Bình thường",
                "Bất thường"
            ]
        )

    if st.button(
        "🔍 PHÂN TÍCH RỦI RO",
        use_container_width=True
    ):

        score, status, reasons = calculate_risk(
            temperature,
            humidity,
            waiting,
            refrigeration
        )

        st.divider()

        st.subheader(
            f"Container {container_id}"
        )

        if status == "High Risk":
            st.error(
                f"🔴 HIGH RISK — Risk Score: {score}/100"
            )

        elif status == "Warning":
            st.warning(
                f"🟡 WARNING — Risk Score: {score}/100"
            )

        else:
            st.success(
                f"🟢 NORMAL — Risk Score: {score}/100"
            )

        st.write("### 🔎 Nguyên nhân được phát hiện")

        if reasons:
            for reason in reasons:
                st.write("• " + reason)
        else:
            st.write(
                "Chưa phát hiện yếu tố rủi ro đáng kể."
            )

        st.write("### 💡 Khuyến nghị xử lý")

        if status == "High Risk":

            st.write(
                "• Kiểm tra ngay nguồn điện và hệ thống làm lạnh."
            )

            st.write(
                "• Ưu tiên container trong quá trình thông quan."
            )

            st.write(
                "• Cân nhắc chuyển hàng vào khu vực bảo quản lạnh phù hợp."
            )

            st.write(
                "• Tăng tần suất giám sát nhiệt độ và độ ẩm."
            )

        elif status == "Warning":

            st.write(
                "• Tiếp tục theo dõi nhiệt độ và độ ẩm."
            )

            st.write(
                "• Kiểm tra thời gian chờ và tình trạng làm lạnh."
            )

        else:

            st.write(
                "• Tiếp tục duy trì điều kiện bảo quản hiện tại."
            )

# =========================
# FOOTER
# =========================
st.divider()

st.caption(
    "COLDGUARD AI | Prototype mô phỏng quản trị rủi ro chuỗi lạnh | "
    "Dữ liệu phục vụ mục đích nghiên cứu và trình diễn."
)
