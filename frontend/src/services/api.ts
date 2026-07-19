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
