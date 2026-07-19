const API_BASE = 'http://localhost:8000/v1/admin';

export interface APIKey {
  id: number;
  key: string;
  name: string;
}

export const adminApi = {
  getKeys: async (): Promise<APIKey[]> => {
    const res = await fetch(`${API_BASE}/keys`);
    if (!res.ok) throw new Error('Failed to fetch keys');
    return res.json();
  },
  
  createKey: async (name: string): Promise<APIKey> => {
    const res = await fetch(`${API_BASE}/keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name })
    });
    if (!res.ok) throw new Error('Failed to create key');
    return res.json();
  },
  
  deleteKey: async (id: number): Promise<void> => {
    const res = await fetch(`${API_BASE}/keys/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete key');
  }
};

export const modelsApi = {
  getModels: async (): Promise<any[]> => {
    const res = await fetch(`${API_BASE}/models`);
    if (!res.ok) throw new Error('Failed to fetch models');
    const response = await res.json();
    return response.data;
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
