const API_BASE = 'http://localhost:8000/v1/admin';

export interface APIKey {
  id: number;
  key: string;
  name: string;
}

export interface AIProfile {
  id: string;
  name: string;
  description: string;
  model_id: string;
  provider_id: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export const adminApi = {
  getKeys: async (): Promise<APIKey[]> => {
    try {
      const res = await fetch(`${API_BASE}/keys`);
      if (!res.ok) throw new Error("Failed to fetch keys");
      return await res.json();
    } catch (e) {
      console.warn("API Keys fetch failed, returning mock fallback.", e);
      return [{ id: 1, name: "Default Key (Fallback)", key: "llmhub-mock-key-12345" }];
    }
  },
  
  createKey: async (name: string): Promise<APIKey> => {
    const res = await fetch(`${API_BASE}/keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    if (!res.ok) throw new Error("Failed to create key");
    return await res.json();
  },
  
  deleteKey: async (id: number): Promise<void> => {
    const res = await fetch(`${API_BASE}/keys/${id}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error("Failed to delete key");
  }
};

export const profilesApi = {
  getProfiles: async (): Promise<AIProfile[]> => {
    const res = await fetch(`${API_BASE}/profiles/`);
    if (!res.ok) throw new Error("Failed to fetch profiles");
    return await res.json();
  },
  
  createProfile: async (profile: Partial<AIProfile>): Promise<AIProfile> => {
    const res = await fetch(`${API_BASE}/profiles/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to create profile");
    }
    return await res.json();
  },
  
  updateProfile: async (id: string, profile: Partial<AIProfile>): Promise<AIProfile> => {
    const res = await fetch(`${API_BASE}/profiles/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to update profile");
    }
    return await res.json();
  },
  
  deleteProfile: async (id: string): Promise<void> => {
    const res = await fetch(`${API_BASE}/profiles/${id}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error("Failed to delete profile");
  }
};

export const modelsApi = {
  getModels: async (): Promise<any[]> => {
    try {
      const res = await fetch('http://localhost:8000/v1/models/');
      if (!res.ok) throw new Error();
      const body = await res.json();
      return body.data;
    } catch (e) {
      console.warn("Models catalog fetch failed, returning mock fallback.", e);
      return [
        { id: 'openai', name: 'OpenAI', best_for: 'General purpose, coding, complex reasoning.', models: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'], status: 'active' },
        { id: 'anthropic', name: 'Anthropic', best_for: 'Nuanced writing, large context analysis.', models: ['claude-3-5-sonnet', 'claude-3-opus', 'claude-3-haiku'], status: 'active' },
        { id: 'google', name: 'Google (Gemini)', best_for: 'Multimodal tasks, high volume fast queries.', models: ['gemini-1.5-pro', 'gemini-1.5-flash'], status: 'active', free_tier: true },
        { id: 'mistral', name: 'Mistral AI', best_for: 'Cost-effective performance, European languages.', models: ['mistral-large-latest', 'open-mixtral-8x22b'], status: 'planned' },
        { id: 'groq', name: 'Groq', best_for: 'Ultra-fast real-time inference (Llama, Mixtral).', models: ['llama3-8b-8192', 'mixtral-8x7b-32768'], status: 'planned' },
        { id: 'cohere', name: 'Cohere', best_for: 'RAG, enterprise search, embeddings.', models: ['command-r', 'command-r-plus'], status: 'planned' },
        { id: 'together', name: 'Together AI', best_for: 'Running massive open-source models efficiently.', models: ['Llama-3-70b-chat', 'Qwen2-72B-Instruct'], status: 'planned' },
        { id: 'aws', name: 'AWS Bedrock', best_for: 'Enterprise security, AWS ecosystem integration.', models: ['claude-3-sonnet-aws', 'llama3-70b-aws'], status: 'planned' },
        { id: 'azure', name: 'Azure OpenAI', best_for: 'Enterprise-grade OpenAI access with compliance.', models: ['azure-gpt-4o', 'azure-gpt-35-turbo'], status: 'planned' },
        { id: 'ollama', name: 'Ollama (Local)', best_for: 'Free local development, privacy.', models: ['gemma:7b', 'llama3:8b'], status: 'active', free_tier: true },
      ];
    }
  }
};

export const chatApi = {
  chat: async (
    apiKey: string,
    model: string,
    messages: { role: string; content: string }[],
    temperature: number = 0.7
  ): Promise<string> => {
    const res = await fetch('http://localhost:8000/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': apiKey,
      },
      body: JSON.stringify({
        model,
        messages,
        temperature
      })
    });
    
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Chat error: ${err}`);
    }
    
    const data = await res.json();
    return data.choices[0].message.content;
  }
};
