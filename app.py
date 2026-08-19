import html
import textwrap

import streamlit as st
from src.faq_retriever import FAQRetriever

st.set_page_config(
    page_title="SafeX University Assistant",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
)

WELCOME_MESSAGE = (
    "Hello! I can help you find information about university admissions, "
    "programs, fees, scholarships, deadlines, and the SafeX internship program."
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

if "theme" not in st.session_state:
    st.session_state.theme = "light"


@st.cache_resource
def load_retriever():
    return FAQRetriever("data/faqs.csv")


retriever = load_retriever()

FAQ_QUESTIONS = [
    "What are the admission requirements?",
    "What undergraduate programs are offered?",
    "How do I apply for admission?",
    "What is the tuition fee structure?",
    "What scholarships are available?",
    "What is the application deadline?",
    "Who is eligible for the SafeX internship?",
    "How long does the SafeX internship last?",
    "Do interns receive a certificate?",
    "What GPA do I need to maintain my scholarship?",
]

theme = st.session_state.theme

if theme == "light":
    BG         = "#F4F6FA"
    SIDEBAR_BG = "#FFFFFF"
    CARD_BG    = "#FFFFFF"
    TEXT       = "#111827"
    MUTED      = "#6B7280"
    BORDER     = "#E2E8F0"
    BLUE       = "#2563EB"
    BLUE_DARK  = "#1D4ED8"
    BLUE_SOFT  = "#EFF6FF"
    USER_BG    = "#EEF4FF"
    BOT_BG     = "#FFFFFF"
    INPUT_BG   = "#FFFFFF"
    INPUT_TEXT = "#111827"
    INPUT_PH   = "#9CA3AF"
    SHADOW     = "rgba(0,0,0,0.06)"
    # icon: dark on light bg, always #111827
    ICON_FG    = "#111827"
    ICON_BG    = "#FFFFFF"
    ICON_BD    = "#E2E8F0"
else:
    BG         = "#0D1117"
    SIDEBAR_BG = "#161B22"
    CARD_BG    = "#1C2333"
    TEXT       = "#E6EDF3"
    MUTED      = "#8B949E"
    BORDER     = "#30363D"
    BLUE       = "#3B82F6"
    BLUE_DARK  = "#2563EB"
    BLUE_SOFT  = "#1D2D50"
    USER_BG    = "#1A2744"
    BOT_BG     = "#1C2333"
    INPUT_BG   = "#1C2333"
    INPUT_TEXT = "#E6EDF3"
    INPUT_PH   = "#6B7280"
    SHADOW     = "rgba(0,0,0,0.3)"
    # icon: light on dark bg, always #E6EDF3
    ICON_FG    = "#E6EDF3"
    ICON_BG    = "#1C2333"
    ICON_BD    = "#30363D"

css = textwrap.dedent(f"""
<style>

/* global */
.stApp, [data-testid="stAppViewContainer"] {{
    background: {BG};
    color: {TEXT};
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}}
[data-testid="stHeader"] {{
    background: transparent !important;
    border-bottom: none !important;
}}
[data-testid="stDecoration"] {{ display: none !important; }}
.main .block-container {{
    max-width: 860px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
}}

/* drawer toggle buttons — both collapsed and collapse-inside */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 9999 !important;
}}

[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {{
    width: 38px !important;
    height: 38px !important;
    min-width: 38px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: {ICON_BG} !important;
    border: 1.5px solid {ICON_BD} !important;
    border-radius: 9px !important;
    box-shadow: 0 2px 8px {SHADOW} !important;
}}

/* icon SVG — hardcoded to theme foreground, not inherited */
[data-testid="stSidebarCollapsedControl"] button svg,
[data-testid="stSidebarCollapsedControl"] button svg path,
[data-testid="stSidebarCollapsedControl"] button svg line,
[data-testid="stSidebarCollapsedControl"] button svg rect,
[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="stSidebarCollapseButton"] button svg path,
[data-testid="stSidebarCollapseButton"] button svg line,
[data-testid="stSidebarCollapseButton"] button svg rect {{
    fill: {ICON_FG} !important;
    stroke: {ICON_FG} !important;
    color: {ICON_FG} !important;
}}

[data-testid="stSidebarCollapsedControl"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover {{
    border-color: {BLUE} !important;
    background: {BLUE_SOFT} !important;
}}
[data-testid="stSidebarCollapsedControl"] button:hover svg path,
[data-testid="stSidebarCollapsedControl"] button:hover svg line,
[data-testid="stSidebarCollapseButton"] button:hover svg path,
[data-testid="stSidebarCollapseButton"] button:hover svg line {{
    fill: {BLUE} !important;
    stroke: {BLUE} !important;
}}

@media (max-width: 768px) {{
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"] {{
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
    }}
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button {{
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
    }}
}}

/* sidebar */
[data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {BORDER} !important;
}}
[data-testid="stSidebar"] * {{ color: {TEXT}; }}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 1.25rem; }}

.sidebar-brand {{
    padding: 4px 6px 18px 6px;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 16px;
}}
.sidebar-brand-name {{
    font-size: 17px;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: -0.3px;
}}
.sidebar-brand-sub {{
    font-size: 12px;
    color: {MUTED};
    margin-top: 3px;
}}
.sidebar-section {{
    font-size: 10px;
    font-weight: 700;
    color: {MUTED};
    letter-spacing: 1.1px;
    text-transform: uppercase;
    margin: 18px 0 8px 2px;
}}

/* sidebar buttons */
.stButton > button {{
    width: 100%;
    min-height: 40px;
    border-radius: 8px;
    border: 1px solid {BORDER};
    background: {CARD_BG};
    color: {TEXT};
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    padding: 8px 12px;
    transition: border-color 0.15s, color 0.15s, background 0.15s;
}}
.stButton > button:hover {{
    border-color: {BLUE};
    color: {BLUE};
    background: {BLUE_SOFT};
}}

/* header card */
.top-header {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 26px 28px 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px {SHADOW};
}}
.top-title {{
    font-size: 22px;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: -0.4px;
    margin: 0 0 6px;
    line-height: 1.2;
}}
.top-subtitle {{
    font-size: 13.5px;
    color: {MUTED};
    line-height: 1.6;
    margin: 0;
}}
.blue-bar {{
    width: 36px;
    height: 3px;
    background: {BLUE};
    border-radius: 4px;
    margin-top: 16px;
}}

/* chat bubbles */
.chat-user {{
    background: {USER_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px 15px;
    margin: 8px 0 8px auto;
    max-width: 78%;
}}
.chat-bot {{
    background: {BOT_BG};
    border: 1px solid {BORDER};
    border-left: 3px solid {BLUE};
    border-radius: 12px;
    padding: 12px 15px;
    margin: 8px auto 14px 0;
    max-width: 84%;
    box-shadow: 0 1px 3px {SHADOW};
}}
.chat-label {{
    font-size: 10px;
    font-weight: 700;
    color: {BLUE};
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 5px;
}}
.chat-text {{
    font-size: 14px;
    color: {TEXT};
    line-height: 1.65;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}}
/* Bottom chat-input area */
[data-testid="stBottom"] {{
    background: {BG} !important;
    background-color: {BG} !important;
    border-top: none !important;
}}

[data-testid="stBottom"] > div {{
    background: {BG} !important;
    background-color: {BG} !important;
}}

[data-testid="stBottom"] [data-testid="stChatInput"] {{
    background: {INPUT_BG} !important;
}}

/* Streamlit bottom container */
.stBottom {{
    background: {BG} !important;
}}

.stBottom > div {{
    background: {BG} !important;
}}

/* chat input */
[data-testid="stChatInput"] {{
    background: {INPUT_BG} !important;
    border: 1.5px solid {BLUE} !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px {SHADOW} !important;
    padding: 4px 6px !important;
}}

[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] > div > div,
[data-testid="stChatInput"] form,
[data-testid="stChatInput"] form > div,
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea + div {{
    background: {INPUT_BG} !important;
}}

/* Text area */
[data-testid="stChatInput"] textarea {{
    color: {INPUT_TEXT} !important;
    -webkit-text-fill-color: {INPUT_TEXT} !important;
    caret-color: {BLUE} !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    padding: 10px 10px !important;
    resize: none !important;
}}

/* Placeholder */
[data-testid="stChatInput"] textarea::placeholder {{
    color: {INPUT_PH} !important;
    -webkit-text-fill-color: {INPUT_PH} !important;
    opacity: 1 !important;
    font-size: 13px !important;
}}

/* Focus */
[data-testid="stChatInput"]:focus-within {{
    border-color: {BLUE} !important;
    box-shadow:
        0 2px 12px {SHADOW},
        0 0 0 3px rgba(59,130,246,0.12) !important;
}}

/* Send button */
[data-testid="stChatInput"] button {{
    background: {BLUE} !important;
    border: none !important;
    border-radius: 10px !important;
    width: 36px !important;
    height: 36px !important;
    flex-shrink: 0 !important;
}}

[data-testid="stChatInput"] button:hover {{
    background: {BLUE_DARK} !important;
}}

[data-testid="stChatInput"] button svg {{
    fill: #ffffff !important;
    color: #ffffff !important;
}}
/* toggle */
[data-testid="stToggle"] label {{
    color: {TEXT} !important;
    font-size: 13px !important;
}}

/* footer */
.footer {{
    text-align: center;
    font-size: 11px;
    color: {MUTED};
    padding: 20px 0 6px;
}}

/* mobile */
@media (max-width: 768px) {{
    .main .block-container {{
        padding-top: 3.5rem;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }}
    .top-header {{ padding: 18px 16px 16px; }}
    .top-title {{ font-size: 18px; }}
    .chat-user, .chat-bot {{ max-width: 94%; }}
    [data-testid="stChatInput"] textarea {{
        font-size: 14px !important;
        padding: 9px 8px !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        font-size: 12px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }}
}}

</style>
""")

st.markdown(css, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(textwrap.dedent("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-name">SafeX University</div>
            <div class="sidebar-brand-sub">Student Support Assistant</div>
        </div>
    """), unsafe_allow_html=True)

    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
        st.rerun()

    st.markdown('<div class="sidebar-section">Frequently Asked</div>', unsafe_allow_html=True)

    for question in FAQ_QUESTIONS:
        if st.button(question, key=f"faq_{question}", use_container_width=True):
            result = retriever.retrieve(question)
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
            st.rerun()

    st.markdown('<div class="sidebar-section">Chat</div>', unsafe_allow_html=True)

    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
        st.rerun()

    st.markdown('<div class="sidebar-section">Appearance</div>', unsafe_allow_html=True)

    dark_mode = st.toggle("Dark theme", value=(theme == "dark"))
    if ("dark" if dark_mode else "light") != st.session_state.theme:
        st.session_state.theme = "dark" if dark_mode else "light"
        st.rerun()

st.markdown(textwrap.dedent(f"""
    <div class="top-header">
        <div class="top-title">SafeX University Assistant</div>
        <div class="top-subtitle">
            Get quick answers about admissions, undergraduate programs,
            tuition fees, scholarships, application deadlines, and
            SafeX internship opportunities.
        </div>
        <div class="blue-bar"></div>
    </div>
"""), unsafe_allow_html=True)

for message in st.session_state.messages:
    safe = html.escape(str(message["content"]))
    if message["role"] == "user":
        st.markdown(textwrap.dedent(f"""
            <div class="chat-user">
                <div class="chat-label">You</div>
                <div class="chat-text">{safe}</div>
            </div>
        """), unsafe_allow_html=True)
    else:
        st.markdown(textwrap.dedent(f"""
            <div class="chat-bot">
                <div class="chat-label">Assistant</div>
                <div class="chat-text">{safe}</div>
            </div>
        """), unsafe_allow_html=True)

prompt = st.chat_input("Ask a question...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    result = retriever.retrieve(prompt)
    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
    st.rerun()

st.markdown('<div class="footer">SafeX University Student Support Assistant</div>', unsafe_allow_html=True)