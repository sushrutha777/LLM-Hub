# LLMHub 🚀 (Streamlit + Render Edition)

> A 100% Python, Streamlit-powered AI Gateway to deploy, manage, route, and monitor Large Language Models.

This edition of LLMHub combines the AI routing engine and administration dashboard into a single, elegant Streamlit app. It can be deployed to **Render** in 1 click for free!

## 🌟 Features

* 📊 **Dashboard & Analytics:** Live tracking of total requests, provider traffic distribution, and latency.
* 🧪 **AI Playground:** Interactively route prompts to OpenAI (`gpt-4o`) or Google (`gemini-1.5-pro`).
* 🔑 **API Keys:** View and generate gateway access keys.
* 🔌 **Integration Guide:** Complete code examples for linking your live projects.

## 🚀 Quick Start (Local)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Add your API keys to `.env`:
   ```env
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   ```

3. Launch Streamlit:
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser!

## ☁️ Deploy to Render (1-Click)

1. Push your repository to GitHub.
2. Log in to [Render.com](https://render.com/).
3. Click **New +** -> **Blueprint**.
4. Connect your repo. Render reads `render.yaml` and deploys your Streamlit app automatically!
5. In Render's dashboard, set your `OPENAI_API_KEY` and `GEMINI_API_KEY` under **Environment**.
