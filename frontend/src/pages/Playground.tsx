import React, { useState } from 'react';
import { chatApi } from '../services/api';
import './Playground.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export const Playground: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('gemini-1.5-pro');
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !apiKey.trim()) return;

    const userMessage: Message = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await chatApi.chat(apiKey, model, newMessages);
      setMessages([...newMessages, { role: 'assistant', content: response }]);
    } catch (e: any) {
      console.error(e);
      setMessages([...newMessages, { role: 'assistant', content: `Error: ${e.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="playground-page">
      <header className="page-header stagger-1">
        <h1>Playground</h1>
        <p>Test and interact with your connected LLMs in real-time.</p>
      </header>

      <div className="playground-layout stagger-2">
        <aside className="settings-panel glass-panel">
          <div className="section-header">
            <h3>Configuration</h3>
            <p className="section-description">Set up your test request.</p>
          </div>
          
          <div className="form-group">
            <label>LLMHub API Key</label>
            <input 
              type="password" 
              placeholder="llmhub-xxxxx"
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
            />
            <small className="form-help">Enter a key generated in the API Keys tab.</small>
          </div>

          <div className="form-group">
            <label>Model</label>
            <select value={model} onChange={e => setModel(e.target.value)}>
              <optgroup label="Google (Gemini)">
                <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
              </optgroup>
              <optgroup label="OpenAI">
                <option value="gpt-4o">GPT-4o</option>
                <option value="gpt-4o-mini">GPT-4o Mini</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
              </optgroup>
              <optgroup label="Anthropic">
                <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
                <option value="claude-3-opus">Claude 3 Opus</option>
                <option value="claude-3-haiku">Claude 3 Haiku</option>
              </optgroup>
              <optgroup label="Groq">
                <option value="llama3-8b-8192">Llama 3 8B</option>
                <option value="mixtral-8x7b-32768">Mixtral 8x7B</option>
              </optgroup>
              <optgroup label="Cohere">
                <option value="command-r">Command R</option>
                <option value="command-r-plus">Command R+</option>
              </optgroup>
              <optgroup label="Mistral">
                <option value="mistral-large-latest">Mistral Large</option>
                <option value="open-mixtral-8x22b">Mixtral 8x22B</option>
              </optgroup>
              <optgroup label="Together AI">
                <option value="meta-llama/Llama-3-70b-chat-hf">Llama 3 70B</option>
                <option value="Qwen/Qwen2-72B-Instruct">Qwen 2 72B</option>
              </optgroup>
              <optgroup label="AWS Bedrock">
                <option value="anthropic.claude-3-sonnet-20240229-v1:0">Claude 3 Sonnet (AWS)</option>
                <option value="meta.llama3-70b-instruct-v1:0">Llama 3 70B (AWS)</option>
              </optgroup>
              <optgroup label="Azure OpenAI">
                <option value="azure-gpt-4o">GPT-4o (Azure)</option>
                <option value="azure-gpt-35-turbo">GPT-3.5 Turbo (Azure)</option>
              </optgroup>
              <optgroup label="Ollama (Local)">
                <option value="gemma:7b">Gemma 7B</option>
                <option value="llama3:8b">Llama 3 8B</option>
              </optgroup>
            </select>
            <small className="form-help">The request will automatically be routed to the corresponding provider based on the model name.</small>
          </div>
          
          <div className="settings-footer">
            <button 
              className="btn-secondary w-100" 
              onClick={() => setMessages([])}
              disabled={messages.length === 0}
            >
              Clear Conversation
            </button>
          </div>
        </aside>

        <section className="chat-interface glass-panel">
          <div className="chat-history">
            {messages.length === 0 && (
              <div className="empty-state">
                <span className="emoji">💬</span>
                <p>Send a message to start testing <strong>{model}</strong>.</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`message-wrapper ${m.role}`}>
                <div className="message-bubble">
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message-wrapper assistant">
                <div className="message-bubble loading-bubble">
                  <span className="dot-typing"></span>
                </div>
              </div>
            )}
          </div>
          
          <form className="chat-input-area" onSubmit={handleSend}>
            <input 
              type="text" 
              placeholder={apiKey ? `Message ${model}...` : "Please enter your LLMHub API key first..."}
              value={input}
              onChange={e => setInput(e.target.value)}
              disabled={!apiKey || loading}
            />
            <button type="submit" className="btn-primary" disabled={!apiKey || loading || !input.trim()}>
              Send
            </button>
          </form>
        </section>
      </div>
    </div>
  );
};
