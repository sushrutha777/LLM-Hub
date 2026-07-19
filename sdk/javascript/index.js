class Client {
  /**
   * Initialize the LLMHub JavaScript client.
   * @param {Object} config - Client configuration.
   * @param {string} config.apiKey - The API Key for authorization.
   * @param {string} [config.baseUrl="http://localhost:8000"] - The base URL of the LLMHub gateway.
   */
  constructor({ apiKey, baseUrl = 'http://localhost:8000' }) {
    if (!apiKey) {
      throw new Error('API Key is required to initialize the LLMHub Client.');
    }
    this.apiKey = apiKey;
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  /**
   * Send a chat completion request to the LLMHub Gateway.
   * @param {Object} options - Chat completion request parameters.
   * @param {string} options.profile - The active model profile (e.g. 'rag-chat', 'invoice-extractor').
   * @param {Array<Object>} options.messages - A list of messages (e.g. [{ role: 'user', content: 'Hello' }]).
   * @param {Object} [options.extraParams] - Additional parameters passed to the gateway (e.g. temperature, max_tokens).
   * @returns {Promise<Object>} The chat completion response payload.
   */
  async chat({ profile, messages, ...extraParams }) {
    const url = `${this.baseUrl}/api/v1/chat`;
    const payload = {
      profile,
      messages,
      ...extraParams
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`LLMHub Error: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`LLMHub request failed: ${error.message}`);
    }
  }
}

module.exports = { Client };
