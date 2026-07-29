import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Reset & Core Theme ── */
:root {
    --bg-dark: #090d16;
    --card-bg: rgba(18, 26, 43, 0.65);
    --card-border: rgba(255, 255, 255, 0.08);
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-dark);
    background-image: 
        radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(15, 23, 42, 0.5) 0px, transparent 100%);
    background-attachment: fixed;
}

/* ── Hide Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding: 3rem 4rem 5rem; 
    max-width: 1320px; 
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    border-radius: 9999px;
    background: rgba(6, 182, 212, 0.08);
    border: 1px solid rgba(6, 182, 212, 0.25);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--accent-cyan);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: clamp(2.5rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #38bdf8 0%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.1rem;
    font-weight: 400;
    color: var(--text-secondary);
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Visual Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    margin: 2.5rem 0;
}

/* ── Control Card ── */
.input-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(16px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
}

/* ── Streamlit Form Input Customization ── */
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}
.stTextInput > div > div > input {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 4px rgba(6, 182, 212, 0.15) !important;
    background: rgba(15, 23, 42, 0.9) !important;
}

/* ── Primary Action Button ── */
.stButton > button {
    background: linear-gradient(135deg, #06b6d4 0%, #10b981 100%) !important;
    color: #04121e !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 10px 25px -5px rgba(6, 182, 212, 0.4) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 30px -5px rgba(6, 182, 212, 0.6) !important;
    filter: brightness(1.08);
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Example Chips ── */
.chip-container {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
    align-items: center;
}
.chip-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
}
.chip {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 0.35rem 0.75rem;
    font-size: 0.78rem;
    color: var(--text-secondary);
    transition: all 0.2s ease;
}
.chip:hover {
    border-color: rgba(6, 182, 212, 0.3);
    color: var(--text-primary);
}

/* ── Pipeline Cards ── */
.step-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.85rem;
    position: relative;
    backdrop-filter: blur(12px);
    transition: all 0.25s ease;
}
.step-card.active {
    border-color: rgba(6, 182, 212, 0.5);
    background: rgba(6, 182, 212, 0.05);
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.1);
}
.step-card.done {
    border-color: rgba(16, 185, 129, 0.3);
    background: rgba(16, 185, 129, 0.03);
}

.step-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.step-title-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-cyan);
}
.step-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-primary);
}
.step-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    letter-spacing: 0.05em;
}
.status-waiting { color: var(--text-muted); background: rgba(255, 255, 255, 0.03); }
.status-running { 
    color: var(--accent-cyan); 
    background: rgba(6, 182, 212, 0.1);
    animation: pulse 1.8s infinite;
}
.status-done { color: var(--accent-emerald); background: rgba(16, 185, 129, 0.1); }

@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

/* ── Result & Feedback Panels ── */
.panel {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 18px;
    padding: 2rem;
    margin-top: 1.2rem;
    backdrop-filter: blur(16px);
}
.panel-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding-bottom: 0.8rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-header.cyan {
    color: var(--accent-cyan);
    border-bottom: 1px solid rgba(6, 182, 212, 0.2);
}
.panel-header.emerald {
    color: var(--accent-emerald);
    border-bottom: 1px solid rgba(16, 185, 129, 0.2);
}

/* ── Streamlit Expanders Overrides ── */
div[data-testid="stExpander"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    color: var(--text-secondary) !important;
}

/* ── Download Button Styling ── */
.stDownloadButton > button {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    box-shadow: none !important;
    margin-top: 1rem !important;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--accent-cyan) !important;
    color: #ffffff !important;
}

/* ── Section Headings ── */
.section-heading {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 1.2rem 0;
    letter-spacing: -0.01em;
}

/* ── Footer Notice ── */
.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("RUNNING", "status-running"),
        "done":    ("COMPLETED", "status-done"),
    }

    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <div class="step-title-group">
                <span class="step-num">{num}</span>
                <span class="step-title">{title}</span>
            </div>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.8rem; color:var(--text-secondary); margin-top:0.4rem; padding-left:1.8rem;'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ Autonomous Intelligence</div>
    <h1>Research<span>Agent</span></h1>
    <p class="hero-sub">
        A multi-agent system executing search, extraction, drafting, and critical scoring in an automated pipeline.
    </p>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: Input Left, Pipeline Right ────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Objective",
        placeholder="e.g. Roadmap for AGI development in next 5 years",
        key="topic_input",
        label_visibility="visible",
    )

    run_btn = st.button(
        "Run Pipeline",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Example Chips
    st.markdown("""
    <div class="chip-container">
        <span class="chip-label">EXAMPLES:</span>
    """, unsafe_allow_html=True)

    examples = [
        "Future of LLM in Tech Industry",
        "All Latest AI Agents in 2026",
        "Roadmap for AGI development",
    ]

    for ex in examples:
        st.markdown(f'<span class="chip">{ex}</span>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:

    st.markdown('<div class="section-heading">Execution Status</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"

        steps = ["search", "reader", "writer", "critic"]

        if step in r:
            return "done"

        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"

        return "waiting"

    step_card(
        "01",
        "Search Agent",
        s("search"),
        "Queries live web resources and indexes insights"
    )

    step_card(
        "02",
        "Reader Agent",
        s("reader"),
        "Scrapes, parses, and extracts deep contents"
    )

    step_card(
        "03",
        "Writer Chain",
        s("writer"),
        "Synthesizes data into a structured research report"
    )

    step_card(
        "04",
        "Critic Chain",
        s("critic"),
        "Evaluates technical depth and validates findings"
    )


# ── Run Pipeline ──────────────────────────────────────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please specify a target topic to execute the pipeline.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("Search Agent gathering context..."):

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("Reader Agent extracting top documents..."):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("Writer Chain synthesizing draft..."):

        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })

        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("Critic Chain analyzing report accuracy..."):

        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Generated Output</div>', unsafe_allow_html=True)

    # Raw outputs expandable
    if "search" in r:
        with st.expander("🔍 Search Results (Raw Metadata)", expanded=False):
            st.markdown(r["search"])

    if "reader" in r:
        with st.expander("📄 Scraped Content (Raw Text)", expanded=False):
            st.markdown(r["reader"])

    # Final report panel
    if "writer" in r:
        st.markdown("""
        <div class="panel">
            <div class="panel-header cyan">
                <span>📝</span> Primary Research Report
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["writer"])

        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback panel
    if "critic" in r:
        st.markdown("""
        <div class="panel">
            <div class="panel-header emerald">
                <span>🧐</span> Critic Evaluation & Feedback
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["critic"])

        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    RESEARCH AGENT SYSTEM · LANGCHAIN & STREAMLIT FRAMEWORK
</div>
""", unsafe_allow_html=True)