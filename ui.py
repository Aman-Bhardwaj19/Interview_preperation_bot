import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-base: #0b0b0f;
        --text-primary: #f5f5f7;
        --text-secondary: #a3a3af;
        --text-muted: #74747f;

        --accent: #e8384f;
        --accent-hover: #ff4d63;
        --accent-soft: rgba(232, 56, 79, 0.14);
        --accent-soft-hover: rgba(232, 56, 79, 0.22);
        --accent-gradient: linear-gradient(135deg, #e8384f 0%, #7a1220 100%);

        --surface: rgba(255, 255, 255, 0.05);
        --surface-strong: rgba(255, 255, 255, 0.09);
        --border: rgba(255, 255, 255, 0.10);
        --border-strong: rgba(255, 255, 255, 0.18);
        --card-shadow: 0 8px 30px rgba(0, 0, 0, 0.45);

        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 20px;
    }

    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(232, 56, 79, 0.14), transparent 40%),
            radial-gradient(circle at 85% 90%, rgba(122, 18, 32, 0.18), transparent 45%),
            var(--bg-base);
        color: var(--text-primary);
    }

    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        margin-top: 4px;
        margin-bottom: 4px;
        letter-spacing: -0.8px;
        color: var(--text-primary);
    }

    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 15px;
        font-weight: 500;
        margin-bottom: 30px;
    }

    .section-label {
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.7px;
        color: var(--text-muted);
        margin-bottom: 8px;
    }

    /* ============ Glass cards ============ */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--card-shadow) !important;
        backdrop-filter: blur(20px) saturate(140%);
        -webkit-backdrop-filter: blur(20px) saturate(140%);
    }

    .question-card {
        padding: 22px 26px;
        margin: 14px 0;
        border-radius: var(--radius-md);
        background: var(--surface);
        border: 1px solid var(--border-strong);
        box-shadow: var(--card-shadow);
        backdrop-filter: blur(18px) saturate(140%);
        -webkit-backdrop-filter: blur(18px) saturate(140%);
        color: var(--text-primary);
        word-wrap: break-word;
        overflow-wrap: anywhere;
    }

    .question-card h3 { color: var(--text-primary); font-weight: 600; font-size: 16px; margin: 0 0 6px 0; }
    .question-card p { color: var(--text-secondary); }

    .score-tier-good { border-left: 3px solid #22c55e; }
    .score-tier-mid  { border-left: 3px solid #eab308; }
    .score-tier-low  { border-left: 3px solid var(--accent); }

    .glass-hero {
        background: var(--surface-strong);
        border: 1px solid var(--border-strong);
        border-radius: var(--radius-lg);
        box-shadow: var(--card-shadow);
        backdrop-filter: blur(22px) saturate(150%);
        -webkit-backdrop-filter: blur(22px) saturate(150%);
        padding: 30px 34px;
        margin: 4px 0 20px 0;
        word-wrap: break-word;
        overflow-wrap: anywhere;
    }

    .glass-hero h3 {
        font-size: 21px;
        font-weight: 700;
        line-height: 1.5;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.2px;
    }

    .q-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 34px;
        height: 26px;
        padding: 0 10px;
        background: var(--accent-soft);
        color: var(--accent-hover);
        font-size: 12px;
        font-weight: 700;
        border-radius: 999px;
        margin-bottom: 14px;
    }

    .pill-badge {
        display: inline-block;
        background: var(--accent-soft);
        color: var(--accent-hover);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 999px;
        margin-bottom: 12px;
    }

    /* ============ Progress bar ============ */
    .progress-wrap { margin-bottom: 22px; }
    .progress-label { font-size: 13px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; }
    .progress-track { width: 100%; height: 6px; background: var(--border); border-radius: 999px; overflow: hidden; }
    .progress-fill { height: 100%; background: var(--accent-gradient); border-radius: 999px; transition: width 0.3s ease; }
    .stProgress { display: none; }

    /* ============ Score gauge ============ */
    .gauge-card { text-align: center; padding: 20px 10px 24px 10px; }
    .gauge-wrap { position: relative; width: 160px; height: 160px; margin: 0 auto; }
    .gauge-ring {
        position: absolute; inset: 0; border-radius: 50%;
        background: conic-gradient(
            from -135deg,
            var(--accent) calc(var(--pct, 0) * 2.7deg),
            rgba(255,255,255,0.08) calc(var(--pct, 0) * 2.7deg) 270deg,
            transparent 270deg 360deg
        );
    }
    .gauge-inner {
        position: absolute; top: 20px; left: 20px; right: 20px; bottom: 20px;
        border-radius: 50%; background: #131318;
        box-shadow: inset 0 0 0 1px var(--border-strong);
    }
    .gauge-label { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
    .gauge-number { font-size: 34px; font-weight: 800; color: var(--text-primary); line-height: 1; }
    .gauge-out { font-size: 13px; color: var(--text-secondary); margin-top: 2px; }
    .gauge-caption { margin-top: 10px; font-size: 13px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.4px; }

    /* ============ Segmented toggle (replaces the interview-mode radio) ============ */
    .segmented-wrap { display: flex; gap: 6px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 4px; margin-bottom: 4px; }
    .segmented-wrap .stButton > button {
        background: transparent;
        border: none;
        box-shadow: none;
        color: var(--text-secondary);
        font-weight: 600;
    }
    .segmented-wrap .stButton > button[kind="primary"] {
        background: var(--accent);
        color: #fff;
        box-shadow: 0 4px 14px rgba(232, 56, 79, 0.35);
    }

    /* ============ Inputs ============ */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--surface-strong) !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-primary) !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder { color: var(--text-muted) !important; }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }

    /* Selectbox dropdown popover */
    div[data-baseweb="popover"] ul[role="listbox"] {
        background: #17171d !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: var(--radius-sm) !important;
    }
    div[data-baseweb="popover"] li[role="option"] {
        background: transparent !important;
        color: var(--text-primary) !important;
    }
    div[data-baseweb="popover"] li[role="option"]:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background: var(--accent-soft) !important;
        color: var(--accent-hover) !important;
    }
    .stSelectbox svg { fill: var(--text-secondary) !important; }

    /* Radio buttons */
    .stRadio label { color: var(--text-primary) !important; }
    .stRadio div[role="radiogroup"] label span:first-child { border-color: var(--border-strong) !important; }
    input[type="radio"], input[type="checkbox"] { accent-color: var(--accent); }

    /* ============ Slider — thin track, red thumb, always-visible labels ============ */
    div[data-baseweb="slider"] { padding-top: 22px !important; }

    div[data-baseweb="slider"] > div:first-child {
        background: rgba(255, 255, 255, 0.10) !important;
        height: 4px !important;
    }
    div[data-baseweb="slider"] > div:first-child > div {
        background: var(--accent) !important;
        height: 4px !important;
    }

    div[data-baseweb="slider"] [role="slider"] {
        background-color: var(--accent) !important;
        box-shadow: 0 0 0 4px rgba(232, 56, 79, 0.15) !important;
    }

    div[data-testid="stThumbValue"] {
        opacity: 1 !important;
        visibility: visible !important;
        color: var(--accent-hover) !important;
        font-weight: 700 !important;
    }

    div[data-testid="stTickBar"],
    div[data-testid="stTickBarMin"],
    div[data-testid="stTickBarMax"] {
        opacity: 1 !important;
        visibility: visible !important;
        color: var(--text-secondary) !important;
    }

    /* ============ Buttons ============ */
    .stButton > button {
        border-radius: var(--radius-sm);
        min-height: 44px;
        font-weight: 600;
        font-size: 14px;
        background: var(--surface-strong);
        border: 1px solid var(--border-strong);
        color: var(--text-primary);
        transition: all 0.15s ease;
    }
    .stButton > button:hover { background: var(--accent-soft); border-color: var(--accent); }
    .stButton > button[kind="primary"] {
        background: var(--accent);
        border: 1px solid var(--accent);
        color: #ffffff;
        box-shadow: 0 8px 20px rgba(232, 56, 79, 0.30);
    }
    .stButton > button[kind="primary"]:hover { background: var(--accent-hover); border-color: var(--accent-hover); }

    /* ============ Sidebar ============ */
    section[data-testid="stSidebar"] {
        background: #101014;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div:first-child { display: flex; flex-direction: column; height: 100%; padding-bottom: 12px; }

    .sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 6px 0 20px 0; }
    .app-logo {
        width: 38px; height: 38px; border-radius: 10px;
        background: var(--accent-gradient); color: #fff;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 14px; flex-shrink: 0;
    }
    .sidebar-title { font-size: 14.5px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
    .sidebar-subtitle { font-size: 12px; color: var(--text-secondary); }
    .sidebar-divider { border-top: 1px solid var(--border); margin: 2px 0 16px 0; }
    .sidebar-spacer { flex-grow: 1; }
    .sidebar-user { border-top: 1px solid var(--border); padding: 14px 0 10px 0; margin-top: 8px; }
    .sidebar-user-email { font-size: 12px; color: var(--text-secondary); margin-bottom: 10px; word-break: break-all; }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        color: var(--text-secondary);
        text-align: left;
        justify-content: flex-start;
        padding-left: 14px;
        border-radius: 10px;
        font-weight: 500;
        box-shadow: none;
        border: none;
        border-left: 3px solid transparent;
    }
    section[data-testid="stSidebar"] .stButton > button:hover { background: var(--accent-soft); color: var(--accent-hover); }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: var(--accent-soft);
        color: var(--accent-hover);
        border-left: 3px solid var(--accent);
        box-shadow: none;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover { background: var(--accent-soft-hover); }

    /* ============ Auth page ============ */
    .auth-banner {
        height: 96px; border-radius: var(--radius-lg);
        background: var(--accent-gradient);
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 18px;
    }
    .auth-avatar {
        width: 64px; height: 64px; border-radius: 50%;
        background: #101014; color: var(--accent-hover);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 20px;
        border: 3px solid #101014;
        box-shadow: 0 6px 16px rgba(232, 56, 79, 0.35);
    }
    .auth-heading { text-align: center; margin-bottom: 20px; }
    .auth-title { font-size: 23px; font-weight: 800; margin: 0 0 4px 0; color: var(--text-primary); letter-spacing: -0.4px; }
    .auth-tagline { font-size: 14px; color: var(--text-secondary); margin: 0; }

    /* ============ Metrics ============ */
    [data-testid="stMetric"] {
        background: var(--surface); border: 1px solid var(--border-strong);
        border-radius: var(--radius-md); box-shadow: var(--card-shadow);
        backdrop-filter: blur(16px);
        padding: 16px;
    }
    [data-testid="stMetricLabel"] { color: var(--text-secondary); }
    [data-testid="stMetricValue"] { color: var(--text-primary); font-weight: 700; }

    /* ============ Expander ============ */
    div[data-testid="stExpander"] {
        background: var(--surface); border: 1px solid var(--border-strong);
        border-radius: var(--radius-md); box-shadow: var(--card-shadow);
        backdrop-filter: blur(16px);
        margin-bottom: 12px; overflow: hidden;
    }
    .streamlit-expanderHeader { font-weight: 600; color: var(--text-primary) !important; }

    /* ============ Alerts ============ */
    div[data-testid="stAlert"] {
        border-radius: var(--radius-sm); border: 1px solid var(--border-strong);
        background: var(--surface); backdrop-filter: blur(12px);
    }

    /* Line chart text */
    [data-testid="stVegaLiteChart"] text { fill: var(--text-secondary) !important; }

    @media (max-width: 640px) {
        .main-title { font-size: 25px; }
        .glass-hero { padding: 20px 18px; }
        .gauge-wrap { width: 130px; height: 130px; }
        .gauge-number { font-size: 28px; }
    }

    </style>
    """, unsafe_allow_html=True)


def render_progress_bar(current, total):
    pct = (current / total) * 100 if total else 0
    st.markdown(
        f"""
        <div class="progress-wrap">
            <div class="progress-label">Question {current} of {total}</div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{pct}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_score_gauge(score, max_score=10, label="Overall Score"):
    pct = max(0, min(100, (score / max_score) * 100)) if max_score else 0
    st.markdown(
        f"""
        <div class="gauge-card">
            <div class="gauge-wrap">
                <div class="gauge-ring" style="--pct:{pct};"></div>
                <div class="gauge-inner"></div>
                <div class="gauge-label">
                    <span class="gauge-number">{score:.1f}</span>
                    <span class="gauge-out">/{max_score}</span>
                </div>
            </div>
            <div class="gauge-caption">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_segmented_toggle(options, state_key, default_index=0):
    """A two-option segmented control to replace st.radio where visibility matters."""
    if state_key not in st.session_state:
        st.session_state[state_key] = options[default_index]

    st.markdown('<div class="segmented-wrap">', unsafe_allow_html=True)
    cols = st.columns(len(options))
    for col, opt in zip(cols, options):
        with col:
            is_active = st.session_state[state_key] == opt
            if st.button(opt, key=f"{state_key}_{opt}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state[state_key] = opt
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    return st.session_state[state_key]