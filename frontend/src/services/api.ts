const API_BASE = 'http://localhost:8000/v1/admin';

export interface APIKey {
  id: number;
  key: string;
  name: string;
}

export const adminApi = {
  getKeys: async (): Promise<APIKey[]> => {
    // Mock data until backend is built
    return [{ id: 1, name: "Default Key", key: "llmhub-mock-key-12345" }];
  },
  
  createKey: async (name: string): Promise<APIKey> => {
    return { id: Date.now(), name, key: `llmhub-${Math.random().toString(36).substr(2, 9)}` };
  },
  
  deleteKey: async (id: number): Promise<void> => {
    return;
  }
};

export const modelsApi = {
  getModels: async (): Promise<any[]> => {
    // Mock data based on the 10 providers we configured
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
