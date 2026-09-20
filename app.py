
import streamlit as st
from PIL import Image
from predictor import predict_disease


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriGuard AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "scan_result" not in st.session_state:
    st.session_state.scan_result = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f8f6;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #10271d;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Brand */

.brand {
    padding: 10px 5px 25px 5px;
}

.brand-icon {
    font-size: 42px;
}

.brand-title {
    font-size: 27px;
    font-weight: 800;
    margin-top: 5px;
}

.brand-subtitle {
    font-size: 12px;
    color: #b9cfc3;
}

/* Hero */

.hero {
    background: linear-gradient(135deg, #123c28, #1f7048);
    padding: 38px 42px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px rgba(16, 70, 42, 0.18);
}

.hero-small {
    color: #ccebd9;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.15;
    margin: 8px 0;
}

.hero-description {
    font-size: 16px;
    color: #e1f2e8;
    max-width: 750px;
    line-height: 1.7;
}

/* Cards */

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e4ebe7;
    box-shadow: 0 5px 18px rgba(0,0,0,0.04);
    height: 100%;
}

.card-title {
    font-size: 14px;
    color: #64736b;
    font-weight: 600;
    margin-bottom: 8px;
}

.card-value {
    font-size: 29px;
    color: #163b29;
    font-weight: 800;
}

.card-icon {
    font-size: 30px;
    margin-bottom: 12px;
}

/* Section headings */

.section-title {
    color: #163b29;
    font-size: 24px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* Scanner */

.scanner-box {
    background: white;
    border: 2px dashed #b9d8c5;
    border-radius: 22px;
    padding: 35px;
    text-align: center;
    margin-bottom: 20px;
}

.scanner-icon {
    font-size: 55px;
    margin-bottom: 10px;
}

.scanner-title {
    font-size: 24px;
    font-weight: 800;
    color: #173d2a;
}

.scanner-description {
    color: #6c7b73;
    margin-bottom: 10px;
}

/* Result */

.result-header {
    background: #eaf6ee;
    border: 1px solid #cde7d5;
    padding: 18px 22px;
    border-radius: 17px;
    margin-top: 20px;
    margin-bottom: 18px;
}

.result-header-title {
    color: #17643a;
    font-size: 18px;
    font-weight: 800;
}

.result-header-subtitle {
    color: #5c7064;
    font-size: 13px;
}

/* Detection */

.detection-card {
    background: white;
    border-radius: 18px;
    padding: 25px;
    border-left: 6px solid #26834f;
    box-shadow: 0 5px 18px rgba(0,0,0,0.04);
    min-height: 190px;
}

.action-card {
    background: #fffaf0;
    border-radius: 18px;
    padding: 25px;
    border-left: 6px solid #e6a12c;
    box-shadow: 0 5px 18px rgba(0,0,0,0.04);
    min-height: 190px;
}

.result-card-title {
    font-size: 17px;
    font-weight: 800;
    color: #173d2a;
    margin-bottom: 12px;
}

.result-text {
    color: #56665d;
    line-height: 1.7;
    font-size: 14px;
}

/* Metrics */

.metric-box {
    background: white;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #e4ebe7;
    text-align: center;
}

.metric-label {
    color: #708078;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #173d2a;
    font-size: 21px;
    font-weight: 800;
    margin-top: 5px;
}

/* Tips */

.tip-card {
    background: white;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #e4ebe7;
    min-height: 150px;
}

.tip-title {
    font-weight: 800;
    color: #173d2a;
    margin-bottom: 8px;
}

.tip-text {
    color: #65746c;
    font-size: 13px;
    line-height: 1.6;
}

/* Buttons */

.stButton > button {
    background: #17643a;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 20px;
    font-weight: 700;
    min-height: 48px;
}

.stButton > button:hover {
    background: #0f4d2c;
    color: white;
    border: none;
}

/* File uploader */

[data-testid="stFileUploader"] {
    background: transparent;
}

/* Hide Streamlit footer */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🌱</div>
        <div class="brand-title">AgriGuard</div>
        <div class="brand-subtitle">
            AI CROP INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📷 AI Crop Scanner",
            "📋 Scan History",
            "🗺️ Field Health",
            "💡 Recommendations"
        ]
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
        background:#173b2b;
        padding:15px;
        border-radius:14px;
        ">
        <div style="
        font-size:12px;
        color:#a9c9b7;
        ">
        AI SYSTEM STATUS
        </div>

        <div style="
        font-size:15px;
        font-weight:700;
        margin-top:5px;
        color:#8ce0aa;
        ">
        ● System Online
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">
            SMART AGRICULTURE • AI POWERED
        </div>

        <div class="hero-title">
            Protect Crops.<br>
            Detect Diseases Earlier.
        </div>

        <div class="hero-description">
            AgriGuard uses artificial intelligence to analyze crop leaf
            images and provide rapid disease detection with actionable
            guidance for farmers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Platform Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown("""
        <div class="card">
            <div class="card-icon">🧠</div>
            <div class="card-title">AI MODEL</div>
            <div class="card-value">MobileNetV2</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="card">
            <div class="card-icon">🌿</div>
            <div class="card-title">SUPPORTED CLASSES</div>
            <div class="card-value">20</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="card">
            <div class="card-icon">🌱</div>
            <div class="card-title">CROP TYPES</div>
            <div class="card-value">11+</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown("""
        <div class="card">
            <div class="card-icon">⚡</div>
            <div class="card-title">ANALYSIS</div>
            <div class="card-value">AI Powered</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">What AgriGuard Does</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:

        st.markdown("""
        <div class="tip-card">
            <div class="card-icon">📷</div>
            <div class="tip-title">1. Scan</div>
            <div class="tip-text">
            Take a photo using your phone camera or upload
            a clear crop leaf image.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with b:

        st.markdown("""
        <div class="tip-card">
            <div class="card-icon">🧠</div>
            <div class="tip-title">2. Detect</div>
            <div class="tip-text">
            The trained AI model analyzes the image and identifies
            the crop condition.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c:

        st.markdown("""
        <div class="tip-card">
            <div class="card-icon">⚡</div>
            <div class="tip-title">3. Act</div>
            <div class="tip-text">
            Get immediate management guidance and recommended
            next steps.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Start Diagnosis</div>',
        unsafe_allow_html=True
    )

    st.info(
        "📷 Go to **AI Crop Scanner** from the sidebar to analyze a crop leaf."
    )


# =========================================================
# AI CROP SCANNER
# =========================================================

elif page == "📷 AI Crop Scanner":

    st.markdown("""
    <div class="hero">
        <div class="hero-small">
            AGRIGUARD AI • COMPUTER VISION
        </div>

        <div class="hero-title">
            AI Crop Scanner
        </div>

        <div class="hero-description">
            Take a photo using your device camera or upload a crop leaf
            image. AgriGuard will analyze the image and identify the
            most likely crop condition.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scanner-box">
        <div class="scanner-icon">📷</div>

        <div class="scanner-title">
            Scan Your Crop
        </div>

        <div class="scanner-description">
            Take a live photo or upload JPG, JPEG or PNG.
            Use a clear image with the leaf visible.
        </div>
    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # IMAGE SOURCE
    # =====================================================

    source = st.radio(
        "Choose image source",
        ["📷 Camera", "📁 Upload Image"],
        horizontal=True
    )

    uploaded_file = None

    if source == "📷 Camera":

        uploaded_file = st.camera_input(
            "Take a photo of the crop leaf"
        )

    else:

        uploaded_file = st.file_uploader(
            "Choose a crop leaf image",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed"
        )


    # =====================================================
    # IMAGE PREVIEW + ANALYSIS
    # =====================================================

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        left, right = st.columns([1, 1])

        with left:

            st.image(
                image,
                caption="Crop Leaf Image",
                use_container_width=True
            )

        with right:

            st.markdown("""
            <div class="card">

                <div class="card-icon">
                    🔬
                </div>

                <div class="result-card-title">
                    Ready for AI Analysis
                </div>

                <div class="result-text">
                    Your crop image has been successfully captured.
                    Click the button below to start the AgriGuard
                    disease detection model.
                </div>

            </div>
            """, unsafe_allow_html=True)

            st.write("")

            if st.button(
                "🔍 Analyze Crop",
                use_container_width=True
            ):

                with st.spinner(
                    "AgriGuard AI is analyzing the leaf..."
                ):

                    result = predict_disease(image)

                    st.session_state.scan_result = result


    # =====================================================
    # RESULTS
    # =====================================================

    if st.session_state.scan_result is not None:

        result = st.session_state.scan_result

        disease = result.get(
            "disease",
            "Unknown"
        )

        crop = result.get(
            "crop",
            "Unknown"
        )

        confidence = float(
            result.get(
                "confidence",
                0
            )
        )

        healthy = "healthy" in disease.lower()


        # =================================================
        # RESULT HEADER
        # =================================================

        st.markdown("""
        <div class="result-header">

            <div class="result-header-title">
                ✅ AI Analysis Complete
            </div>

            <div class="result-header-subtitle">
                AgriGuard has processed your crop image.
            </div>

        </div>
        """, unsafe_allow_html=True)


        # =================================================
        # TOP RESULT METRICS
        # =================================================

        m1, m2, m3 = st.columns(3)

        with m1:

            st.markdown(f"""
            <div class="metric-box">

                <div class="metric-label">
                    DETECTED CROP
                </div>

                <div class="metric-value">
                    🌱 {crop}
                </div>

            </div>
            """, unsafe_allow_html=True)

        with m2:

            st.markdown(f"""
            <div class="metric-box">

                <div class="metric-label">
                    DETECTED CONDITION
                </div>

                <div class="metric-value">
                    🦠 {disease}
                </div>

            </div>
            """, unsafe_allow_html=True)

        with m3:

            st.markdown(f"""
            <div class="metric-box">

                <div class="metric-label">
                    AI CONFIDENCE
                </div>

                <div class="metric-value">
                    🎯 {confidence:.2f}%
                </div>

            </div>
            """, unsafe_allow_html=True)


        # =================================================
        # CONFIDENCE
        # =================================================

        st.markdown(
            '<div class="section-title">AI Confidence</div>',
            unsafe_allow_html=True
        )

        st.progress(
            min(confidence / 100, 1.0)
        )

        if confidence >= 90:

            st.success(
                f"High confidence prediction: {confidence:.2f}%"
            )

        elif confidence >= 70:

            st.info(
                f"Moderate confidence prediction: {confidence:.2f}%"
            )

        else:

            st.warning(
                f"Low confidence prediction: {confidence:.2f}%. "
                "Consider uploading a clearer image."
            )


        # =================================================
        # DETECTION TEXT
        # =================================================

        if healthy:

            detection_text = (
                f"AgriGuard AI detected a healthy {crop} leaf. "
                "No major disease symptoms were detected in the "
                "uploaded image."
            )

        else:

            detection_text = (
                f"AgriGuard AI detected {disease} in the "
                f"{crop} leaf with {confidence:.2f}% confidence."
            )


        # =================================================
        # IMMEDIATE ACTION
        # =================================================

        if healthy:

            action_text = (
                "No immediate treatment is required. Continue regular "
                "monitoring, proper irrigation, adequate nutrition, "
                "and good field hygiene."
            )

        elif "early blight" in disease.lower():

            action_text = (
                "Remove severely affected leaves and dispose of them "
                "safely. Avoid overhead irrigation, keep foliage dry, "
                "improve air circulation, and monitor nearby plants."
            )

        elif "late blight" in disease.lower():

            action_text = (
                "Isolate affected plants if possible. Remove severely "
                "infected leaves and avoid overhead watering. Inspect "
                "nearby plants because the disease can spread rapidly."
            )

        elif "powdery mildew" in disease.lower():

            action_text = (
                "Remove heavily infected leaves and improve air "
                "circulation. Avoid excessive humidity and overcrowding. "
                "Monitor surrounding plants for new symptoms."
            )

        elif "rust" in disease.lower():

            action_text = (
                "Remove infected leaves and dispose of them away from "
                "the field. Improve air circulation and monitor nearby "
                "plants for further infection."
            )

        elif "mosaic virus" in disease.lower():

            action_text = (
                "Remove and safely dispose of infected plants. "
                "Disinfect tools after handling infected plants and "
                "control possible insect vectors."
            )

        elif "black rot" in disease.lower():

            action_text = (
                "Remove infected leaves and fruit. Maintain good field "
                "sanitation, avoid unnecessary leaf wetness, and inspect "
                "nearby plants."
            )

        elif "esca" in disease.lower():

            action_text = (
                "Remove severely affected plant material and maintain "
                "good field sanitation. Avoid spreading infected material "
                "through contaminated tools."
            )

        elif "leaf scorch" in disease.lower():

            action_text = (
                "Remove severely affected leaves and maintain proper "
                "irrigation. Avoid plant stress and monitor surrounding "
                "plants regularly."
            )

        elif "target spot" in disease.lower():

            action_text = (
                "Remove affected leaves, improve air circulation, and "
                "avoid overhead irrigation. Monitor nearby plants."
            )

        elif "cercospora" in disease.lower():

            action_text = (
                "Remove infected leaves and maintain good field sanitation. "
                "Avoid prolonged leaf wetness and improve air circulation."
            )

        elif "northern leaf blight" in disease.lower():

            action_text = (
                "Remove severely infected plant material where practical. "
                "Improve field sanitation and monitor nearby corn plants."
            )

        elif "haunglongbing" in disease.lower():

            action_text = (
                "Inspect the plant and surrounding citrus plants carefully. "
                "Follow local agricultural guidance and control possible "
                "insect vectors."
            )

        else:

            action_text = (
                "Isolate the affected plant if possible and inspect nearby "
                "plants. Remove severely affected material and avoid "
                "spreading infected plant material."
            )


        # =================================================
        # DETECTION + ACTION CARDS
        # =================================================

        st.markdown(
            '<div class="section-title">'
            'Diagnosis & Immediate Response'
            '</div>',
            unsafe_allow_html=True
        )

        d1, d2 = st.columns(2)

        with d1:

            st.markdown(f"""
            <div class="detection-card">

                <div class="result-card-title">
                    🔍 Detection
                </div>

                <div class="result-text">
                    {detection_text}
                </div>

            </div>
            """, unsafe_allow_html=True)

        with d2:

            st.markdown(f"""
            <div class="action-card">

                <div class="result-card-title">
                    ⚡ Immediate Action
                </div>

                <div class="result-text">
                    {action_text}
                </div>

            </div>
            """, unsafe_allow_html=True)


        # =================================================
        # TREATMENT & PREVENTION
        # =================================================

        st.markdown(
            '<div class="section-title">'
            '🌿 Treatment & Prevention'
            '</div>',
            unsafe_allow_html=True
        )

        if healthy:

            treatment = (
                "Maintain balanced irrigation and nutrition. "
                "Continue routine crop inspection."
            )

            prevention = (
                "Use healthy planting material, maintain field hygiene, "
                "and regularly inspect leaves for early symptoms."
            )

        else:

            treatment = (
                "Management depends on the confirmed disease, crop stage, "
                "and local conditions. Follow recommendations from a "
                "qualified agricultural expert before using pesticides "
                "or fungicides."
            )

            prevention = (
                "Maintain field sanitation, avoid unnecessary leaf wetness, "
                "provide adequate plant spacing, remove infected material, "
                "and monitor nearby plants regularly."
            )


        t1, t2 = st.columns(2)

        with t1:

            st.markdown(f"""
            <div class="tip-card">

                <div class="card-icon">
                    🧪
                </div>

                <div class="tip-title">
                    Treatment Guidance
                </div>

                <div class="tip-text">
                    {treatment}
                </div>

            </div>
            """, unsafe_allow_html=True)

        with t2:

            st.markdown(f"""
            <div class="tip-card">

                <div class="card-icon">
                    🛡️
                </div>

                <div class="tip-title">
                    Prevention
                </div>

                <div class="tip-text">
                    {prevention}
                </div>

            </div>
            """, unsafe_allow_html=True)


        # =================================================
        # DISCLAIMER
        # =================================================

        st.markdown("---")

        st.caption(
            "⚠️ AgriGuard AI provides an AI-based preliminary assessment. "
            "For serious crop damage or chemical treatment decisions, "
            "consult a qualified agricultural professional."
        )


# =========================================================
# SCAN HISTORY
# =========================================================

elif page == "📋 Scan History":

    st.markdown("""
    <div class="hero">

        <div class="hero-small">
            AGRIGUARD RECORDS
        </div>

        <div class="hero-title">
            Scan History
        </div>

        <div class="hero-description">
            Review your recent AI crop analysis results.
        </div>

    </div>
    """, unsafe_allow_html=True)

    if st.session_state.scan_result is None:

        st.info(
            "📋 No scan has been performed yet. "
            "Run an analysis from AI Crop Scanner."
        )

    else:

        result = st.session_state.scan_result

        st.markdown(f"""
        <div class="card">

            <div class="card-title">
                LATEST AI SCAN
            </div>

            <div class="card-value">
                🌱 {result.get("crop", "Unknown")}
            </div>

            <p>
                Disease:
                <b>{result.get("disease", "Unknown")}</b>
                <br>

                Confidence:
                <b>
                {float(result.get("confidence", 0)):.2f}%
                </b>
            </p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FIELD HEALTH
# =========================================================

elif page == "🗺️ Field Health":

    st.markdown("""
    <div class="hero">

        <div class="hero-small">
            SMART FIELD MONITORING
        </div>

        <div class="hero-title">
            Field Health
        </div>

        <div class="hero-description">
            A future-ready dashboard for monitoring crop health
            across agricultural fields.
        </div>

    </div>
    """, unsafe_allow_html=True)


    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="card">

            <div class="card-icon">
                🌱
            </div>

            <div class="card-title">
                FIELD MONITORING
            </div>

            <div class="card-value">
                Ready
            </div>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="card">

            <div class="card-icon">
                📡
            </div>

            <div class="card-title">
                SENSOR INTEGRATION
            </div>

            <div class="card-value">
                Planned
            </div>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="card">

            <div class="card-icon">
                🤖
            </div>

            <div class="card-title">
                ROBOT INTEGRATION
            </div>

            <div class="card-value">
                Planned
            </div>

        </div>
        """, unsafe_allow_html=True)


    st.markdown(
        '<div class="section-title">'
        'Future AgriGuard Architecture'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "🛰️ Future versions can integrate GPS, IoT sensors, "
        "soil monitoring, weather data and agricultural robots "
        "for complete field-level monitoring."
    )


# =========================================================
# RECOMMENDATIONS
# =========================================================

elif page == "💡 Recommendations":

    st.markdown("""
    <div class="hero">

        <div class="hero-small">
            SMART AGRICULTURE GUIDANCE
        </div>

        <div class="hero-title">
            Recommendations
        </div>

        <div class="hero-description">
            General practices that help maintain healthier crops
            and reduce disease risk.
        </div>

    </div>
    """, unsafe_allow_html=True)


    r1, r2 = st.columns(2)

    with r1:

        st.markdown("""
        <div class="tip-card">

            <div class="card-icon">
                💧
            </div>

            <div class="tip-title">
                Smart Irrigation
            </div>

            <div class="tip-text">
                Avoid unnecessary overhead watering and maintain
                appropriate soil moisture for the crop.
            </div>

        </div>
        """, unsafe_allow_html=True)

    with r2:

        st.markdown("""
        <div class="tip-card">

            <div class="card-icon">
                🌬️
            </div>

            <div class="tip-title">
                Air Circulation
            </div>

            <div class="tip-text">
                Maintain adequate spacing between plants to reduce
                humidity and improve air movement.
            </div>

        </div>
        """, unsafe_allow_html=True)


    st.write("")


    r3, r4 = st.columns(2)

    with r3:

        st.markdown("""
        <div class="tip-card">

            <div class="card-icon">
                🧹
            </div>

            <div class="tip-title">
                Field Hygiene
            </div>

            <div class="tip-text">
                Remove infected plant material and keep tools and
                growing areas clean.
            </div>

        </div>
        """, unsafe_allow_html=True)

    with r4:

        st.markdown("""
        <div class="tip-card">

            <div class="card-icon">
                🔎
            </div>

            <div class="tip-title">
                Early Monitoring
            </div>

            <div class="tip-text">
                Regularly inspect crop leaves so potential problems
                can be identified at an early stage.
            </div>

        </div>
        """, unsafe_allow_html=True)
