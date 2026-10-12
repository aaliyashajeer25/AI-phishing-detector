import joblib
from pathlib import Path

import streamlit as st
from detector import analyze_email

#PAGE CONFIGURATION

st.set_page_config(
    page_title="PhishGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL_PATH = Path(__file__).resolve().parent / "phishing_model.pkl"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

#CUSTOM DASHBOARD STYLING

st.markdown("""
<style>
    .stApp {
         background:#0B1120;
         color:#E2E8F0;
    }

    .block-container {
         max-width: 1200px;
         padding-top: 2rem;
         padding-bottom: 3rem;
    }

    h1,h2,h3 {
         color: #F8FAFC !important;
         letter-spacing: -0.5px;
    }

    [data-testid = "stSidebar"]{
         background: #111827;
         border-right: 1px solid #243247;
    }

    [data-testid="stMetricLabel"] {
         color: #94A3B8;
    }

    .stTextArea textarea {
         background: #172235;
         color: #F8FAFC;
         border: 1px solid #334155;
         border-radius: 12px;
    }

    .stButton > button[kind="primary"]{
         background: #2563EB;
         color: white;
         border: none;
         border-radius: 10px;
         font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover{
         background: #1D4ED8;
         color: white;
    }

    .hero {
         background: linear-gradient(
         120deg, #172554, #0F172A 65%, #123047
        );
    
         padding: 30px;
         border: 1px solid #334155;
         border-radius: 18px;
         margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 8px;
    }

    .hero p {
        color: #CBD5E1;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .finding {
        background: #172235;
        border-left: 4px solid #F59E0B;
        padding: 13px 16px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #E2E8F0;
    }

    .footer {
        text-align: center;
        color: #94A3B8;
        padding: 25px 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


#SAMPLE EMAILS

SAMPLE_EMAILS = {
    "Custom Email": "",
    "Phishing Example": (
        "Subject: URGENT ACTION REQUIRED!\n\n"
        "Your account has been suspended. "
        "Verify your account immediately to avoid losing access.\n\n"
        "Visit http://192.168.1.10/login "
        "to confirm your password!!!"
    ),
    "Legitimate Example": (
        "Subject: Meeting Reminder\n\n"
        "Hello,\n\n"
        "This is a reminder that our project meeting "
        "is scheduled for tomorrow at 10 AM.\n\n"
        "Please review the agenda before attending.\n\n"
        "Best regards,\nProject Coordinator"
    ),
    "Suspicious Bank Email": (
        "Subject: Account Security Alert\n\n"
        "We detected unusual login activity. "
        "Verify your account immediately.\n\n"
        "Your account will be closed unless you "
        "confirm your password at "
        "http://192.168.1.20/verify"
    )
}

#SIDEBAR

with st.sidebar:
    st.title("🛡️ PhishGuard AI")
    st.caption("Cybersecurity Analysis Platform")

    st.divider()

    st.subheader("Navigation")
    st.markdown("🔍 Email Threat Analysis")
    st.markdown("🧠 Machine Learning")
    st.markdown("🛡️ Security Findings")

    st.divider()

    st.subheader("System Status")

    if MODEL_PATH.exists():
        st.success("ML Model Available")
    else:
        st.warning("ML Model Not Found")

    st.info("Rule-Based Detection Active")

    st.divider()

    st.subheader("About")
    st.write(
        "PhishGuard AI combines heuristic security "
        "analysis with machine-learning email "
        "classification."
    )

    st.caption(
        "Educational cybersecurity project built "
        "with Python, Streamlit, and scikit-learn."
    )

#HEADER

st.markdown("""
<div class="hero">
    <h1>🛡️ PhishGuard AI</h1>
    <p>
        Intelligent Email Threat Analysis Dashboard
        — Detect suspicious language, unsafe links,
        and potential social-engineering attempts.
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("🔍 Analyze an Email")
st.write(
    "Paste an email or select a sample to evaluate "
    "potential security threats."
)

#EMAIL INPUT

selected_sample = st.selectbox(
    "Choose an email example",
    list(SAMPLE_EMAILS.keys())
)

#update the input only when the sample selection changes.
if "previous_sample" not in st.session_state:
    st.session_state.previous_sample = selected_sample
    st.session_state.email_input = SAMPLE_EMAILS[selected_sample]

if selected_sample != st.session_state.previous_sample:
    st.session_state.email_input = SAMPLE_EMAILS[selected_sample]
    st.session_state.previous_sample = selected_sample

email_text = st.text_area(
    "Email Content",
    key="email_input",
    height=220,
    placeholder="Paste the email subject and body here..."
)

analyze_clicked = st.button(
    "🔍 Analyze Email",
    type="primary",
    use_container_width=True
)

#EMAIL ANALYSIS

if analyze_clicked:

    if not email_text.strip():
        st.warning("Please enter an email before analyzing.")

    else:
        result = analyze_email(email_text)

        st.divider()
        st.header("📊 Analysis Overview")

        col1, col2 = st.columns(2, gap="large")

        # HEURISTIC RESULTS

        with col1:
            st.subheader("🛡️ Rule-Based Detection")

            st.metric(
                "Heuristic Risk Score",
                f"{result['score']}/100"
            )

            st.progress(result["score"] / 100)

            if result["risk"] == "High Risk":
                st.error("🔴 High Phishing Risk")

            elif result["risk"] == "Medium Risk":
                st.warning("🟡 Medium Phishing Risk")

            else:
                st.success("🟢 Low Heuristic Risk")

            st.caption(
                "Score based on suspicious phrases, "
                "URLs, and other predefined indicators."
            )

        # MACHINE LEARNING RESULTS

        with col2:
            st.subheader("🧠 Machine Learning")

            if MODEL_PATH.exists():

                try:
                    model = load_model()

                    prediction = model.predict(
                        [email_text]
                    )[0]

                    probabilities = model.predict_proba(
                        [email_text]
                    )[0]

                    classes = list(model.classes_)
                    spam_index = classes.index(1)
                    spam_score = probabilities[spam_index]

                    st.metric(
                        "Model Spam Score",
                        f"{spam_score:.1%}"
                    )

                    st.progress(float(spam_score))

                    if prediction == 1:
                        st.warning("ML Classification: Spam")
                    else:
                        st.info("ML Classification: Legitimate")

                    st.caption(
                        "Trained on CEAS_08 spam data. "
                        "This score is not a calibrated "
                        "probability of phishing."
                    )

                    if (
                        result["risk"] == "High Risk"
                        and prediction == 0
                    ):
                        st.warning(
                            "The heuristic detector identified "
                            "high-risk indicators, although the "
                            "ML model classified this email as "
                            "legitimate. Review manually."
                        )

                except (
                    OSError, ValueError, KeyError,
                    AttributeError, IndexError
                ) as error:
                    st.error(
                        "The ML model could not be loaded "
                        "or used for prediction."
                    )
                    st.caption(str(error))

            else:
                st.info(
                    "Train your model to enable "
                    "machine-learning analysis."
                )


        #SECURITY FINDINGS

        st.divider()
        st.header("🚨 Security Findings")

        if result["warnings"]:

            st.write(
                f"**{len(result['warnings'])} "
                "security indicators detected**"
            )

            for warning in result["warnings"]:
                st.warning(f"⚠️ {warning}")

        else:
            st.success(
                "No suspicious indicators were detected "
                "by the rule-based checks."
            )

        #SECURITY RECOMMENDATIONS

        st.divider()
        st.header("🔐 Security Recommendations")

        if result["risk"] == "High Risk":
            st.error(
                "Do not click links, download attachments, "
                "or share credentials. Verify the sender "
                "through an independent trusted channel."
            )

        elif result["risk"] == "Medium Risk":
            st.warning(
                "Review the sender and any links carefully "
                "before interacting with this email."
            )

        else:
            st.info(
                "No major rule-based indicators were found. "
                "This does not guarantee the email is safe."
            )


#FOOTER

st.markdown("""
<div class="footer">
    PhishGuard AI | Educational Cybersecurity Project
    <br>
    Built with Python, Streamlit & Machine Learning
</div>
""", unsafe_allow_html=True)
