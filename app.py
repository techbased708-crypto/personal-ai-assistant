import streamlit as st
from agent import get_agent
from dotenv import load_dotenv

load_dotenv()

# ─── Page Setup ─────────────────────────────────
st.set_page_config(
    page_title="🤖 Personal AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ─── Header ─────────────────────────────────────
st.title("🤖 Personal AI Assistant Agent")
st.caption("Search • Weather • News • Calculator • Time — Sab ek jagah")

# ─── Tool badges dikhao ─────────────────────────
cols = st.columns(5)
badges = ["🔍 Search", "☀️ Weather", "📰 News", "🧮 Math", "🕐 Time"]
for col, badge in zip(cols, badges):
    col.markdown(
        f"<div style='text-align:center; background:#1e1e2e; "
        f"padding:6px; border-radius:8px; font-size:12px'>{badge}</div>",
        unsafe_allow_html=True
    )

st.divider()

# ─── Example prompts ────────────────────────────
st.markdown("**💡 Try these:**")
examples = [
    "What's the weather in Lahore?",
    "Latest news about Pakistan cricket",
    "Convert 1 USD to PKR",
    "What time is it in London right now?",
    "Calculate 15% of 25000"
]

# Button click se input fill ho jaye
example_cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    if example_cols[i % len(example_cols)].button(
        ex[:25] + "...", key=f"ex_{i}", use_container_width=True
    ):
        st.session_state["prefill"] = ex

# ─── Chat History ───────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    with st.spinner("Agent load ho raha hai..."):
        st.session_state.agent = get_agent()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─── Input ──────────────────────────────────────
prefill = st.session_state.pop("prefill", "")
user_input = st.chat_input("Kuch bhi poocho...", key="chat_input")
query = user_input or prefill

if query:
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Soch raha hoon..."):
            try:
                response = st.session_state.agent.invoke({
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                })

                answer = response["messages"][-1].content

            except Exception as e:
                answer = f"❌ Error: {str(e)}"

        st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
