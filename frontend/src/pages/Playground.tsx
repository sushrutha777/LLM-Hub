import React, { useState } from 'react';
import { chatApi } from '../services/api';
import './Playground.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export const Playground: React.FC = () => {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('gemini-1.5-flash');
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
      <header className="page-header">
        <h1>Playground</h1>
        <p className="text-muted">Test and chat with your connected LLMs.</p>
      </header>

      <div className="playground-layout">
        <aside className="settings-panel glass-panel">
          <h3>Settings</h3>
          
          <div className="form-group">
            <label>LLMHub API Key</label>
            <input 
              type="password" 
              placeholder="llmhub-xxxxx"
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
            />
            <small className="text-muted">Enter a key generated in the API Keys tab.</small>
          </div>

          <div className="form-group">
            <label>Model</label>
            <select value={model} onChange={e => setModel(e.target.value)}>
              <optgroup label="Google">
                <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
              </optgroup>
              <optgroup label="Groq (Ultra-Fast)">
                <option value="llama3-8b-8192">Llama 3 8B (Groq)</option>
                <option value="mixtral-8x7b-32768">Mixtral 8x7B (Groq)</option>
              </optgroup>
              <optgroup label="Cohere">
                <option value="command-r">Command R</option>
              </optgroup>
              <optgroup label="OpenAI">
                <option value="gpt-4o">GPT-4o</option>
              </optgroup>
              <optgroup label="Local (Ollama)">
                <option value="gemma">Gemma</option>
                <option value="llama3">Llama 3</option>
              </optgroup>
            </select>
          </div>
        </aside>

        <section className="chat-interface glass-panel">
          <div className="chat-history">
            {messages.length === 0 && (
              <div className="empty-chat">
                <span className="emoji">💬</span>
                <p>Send a message to start the conversation.</p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.role}`}>
                <div className="message-bubble">
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message assistant loading">
                <div className="message-bubble">Thinking...</div>
              </div>
            )}
          </div>
          
          <form className="chat-input-area" onSubmit={handleSend}>
            <input 
              type="text" 
              placeholder={apiKey ? "Type your message..." : "Please enter your LLMHub API key first..."}
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
