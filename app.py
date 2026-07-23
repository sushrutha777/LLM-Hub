import streamlit as st
import asyncio
import pandas as pd
from gateway import process_request, REQUEST_LOGS

st.set_page_config(
    page_title="LLMHub - AI Gateway",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🚀 LLMHub Gateway")
page = st.sidebar.radio("Navigation", ["📊 Dashboard & Analytics", "🧪 AI Playground", "🔑 API Keys", "🔌 Integration Guide"])

if page == "📊 Dashboard & Analytics":
    st.markdown('<div class="main-header">LLMHub Control Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Centralized monitoring, routing stats, and API metrics.</div>', unsafe_allow_html=True)

    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_reqs = len(REQUEST_LOGS)
    avg_latency = int(sum(r["latency_ms"] for r in REQUEST_LOGS) / total_reqs) if total_reqs > 0 else 0
    success_rate = round((sum(1 for r in REQUEST_LOGS if r["status"] == "Success") / total_reqs) * 100, 1) if total_reqs > 0 else 100.0

    col1.metric("Total Gateway Requests", total_reqs)
    col2.metric("Average Latency", f"{avg_latency} ms")
    col3.metric("Success Rate", f"{success_rate}%")
    col4.metric("Active Providers", "5 (OpenAI, Gemini, Claude, Groq, Grok)")

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📋 Recent Gateway Logs")
        if REQUEST_LOGS:
            df = pd.DataFrame(REQUEST_LOGS)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No requests logged yet. Head over to the **AI Playground** to test the router!")

    with col_right:
        st.subheader("🌐 Provider Traffic Distribution")
        if REQUEST_LOGS:
            df_counts = pd.DataFrame(REQUEST_LOGS)["provider"].value_counts().reset_index()
            df_counts.columns = ["Provider", "Requests"]
            st.bar_chart(df_counts.set_index("Provider"))
        else:
            st.caption("Distribution will appear once requests are sent.")

elif page == "🧪 AI Playground":
    st.markdown('<div class="main-header">Unified AI Playground</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Test unified routing across multiple LLMs seamlessly.</div>', unsafe_allow_html=True)

    col_cfg, col_chat = st.columns([1, 2])

    with col_cfg:
        st.subheader("⚙️ Gateway Configuration")
        model = st.selectbox(
            "Select Target Model",
            [
                "claude-3-5-sonnet-20240620",
                "gpt-4o",
                "gpt-3.5-turbo",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "grok-beta",
                "llama3-70b-8192"
            ],
            help="The Gateway automatically inspects the model name and routes to Anthropic, OpenAI, Gemini, Groq, or xAI Grok!"
        )
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
        api_key = st.text_input("Gateway API Key", value="llmhub_sk_showcase123", type="password")

    with col_chat:
        st.subheader("💬 Prompt Session")
        user_prompt = st.text_area("Enter your prompt:", "Explain quantum computing in one simple sentence.", height=120)

        if st.button("🚀 Send Through Gateway", type="primary"):
            if not user_prompt.strip():
                st.warning("Please enter a prompt.")
            else:
                with st.spinner(f"Routing request to model `{model}`..."):
                    messages = [{"role": "user", "content": user_prompt}]
                    response = asyncio.run(process_request(model, messages, temperature, api_key))

                if "error" in response:
                    st.error(response["error"])
                else:
                    st.success(f"Routed via {response.get('provider', 'Provider')}!")
                    if "choices" in response and len(response["choices"]) > 0:
                        content = response["choices"][0]["message"]["content"]
                        st.markdown(f"**Assistant Response:**\n\n{content}")
                    else:
                        st.json(response)

elif page == "🔑 API Keys":
    st.markdown('<div class="main-header">API Key Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Generate and manage access keys for your applications.</div>', unsafe_allow_html=True)

    st.info("The Showcase Edition includes a default active key for immediate integration.")

    st.code("llmhub_sk_showcase123", language="text")

    st.markdown("---")
    st.subheader("Generate New Key")
    key_name = st.text_input("Key Description / App Name", "Production App")
    if st.button("Generate Key"):
        import random, string
        rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        new_key = f"llmhub_sk_{rand_str}"
        st.success(f"Key Generated Successfully for `{key_name}`!")
        st.code(new_key, language="text")

elif page == "🔌 Integration Guide":
    st.markdown('<div class="main-header">Live Project Integration</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Connect your live applications to this LLMHub Gateway.</div>', unsafe_allow_html=True)

    st.markdown("""
    Your live applications only need to change their target base URL to this Gateway.

    ### 1. Python Request Example
    ```python
    import requests

    response = requests.post(
        "https://your-render-url.onrender.com/v1/chat/completions",
        headers={
            "Authorization": "Bearer llmhub_sk_showcase123",
            "Content-Type": "application/json"
        },
        json={
            "model": "claude-3-5-sonnet-20240620",  # or "grok-beta", "gemini-1.5-pro", "gpt-4o"
            "messages": [{"role": "user", "content": "Hello from my app!"}]
        }
    )

    print(response.json())
    ```

    ### 2. cURL Example
    ```bash
    curl -X POST https://your-render-url.onrender.com/v1/chat/completions \\
      -H "Authorization: Bearer llmhub_sk_showcase123" \\
      -H "Content-Type: application/json" \\
      -d '{
        "model": "claude-3-5-sonnet-20240620",
        "messages": [{"role": "user", "content": "Hello!"}]
      }'
    ```
    """)
