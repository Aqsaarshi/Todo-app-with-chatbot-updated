// frontend/src/services/apiClient.ts
import axios, { AxiosInstance } from 'axios';

interface MessageData {
  message: string;
  conversation_id?: number;  // Changed to number to match backend
}

interface ChatResponse {
  conversation_id: number;  // Changed to number to match backend
  response: string;
  tool_calls: Array<{
    tool_name: string;
    parameters: Record<string, any>;
    result: Record<string, any>;
  }>;
  timestamp: string;
}

interface ConversationsResponse {
  conversations: Array<{
    id: number;  // Changed to number to match backend
    title: string;
    created_at: string;
    updated_at: string;
  }>;
  total_count: number;
}

interface MessagesResponse {
  messages: Array<{
    id: number;  // Changed to number to match backend
    sender_type: 'user' | 'assistant';
    content: string;
    timestamp: string;
    tool_calls: any[];
  }>;
  total_count: number;
}

class ApiClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor() {
    // Use the environment variable for the API URL
    // The backend already includes '/api' in the route prefixes, so we don't add it here
    this.baseUrl = process.env.NEXT_PUBLIC_CHAT_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000, // 30 seconds timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Note: For the Hugging Face backend, tokens are passed as query parameters
    // rather than in the Authorization header, so we don't add the Authorization header

    // Handle responses globally
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  // Method to send a message to the chat endpoint
  async sendMessage(userId: string, message: string, conversationId?: string): Promise<ChatResponse> {
    try {
      // If the user ID is 'anonymous', redirect to login
      if (userId === 'anonymous') {
        // Redirect to login page
        window.location.href = '/login';
        throw new Error('Authentication required');
      } else {
        // Get token from localStorage
        const token = localStorage.getItem('auth_token');
        if (!token) {
          throw new Error('Authentication token not found');
        }

        const response = await this.client.post<ChatResponse>(
          `/api/${userId}/chat?token=${encodeURIComponent(token)}`,
          {
            message,
            conversation_id: conversationId,
          } as MessageData
        );
        return response.data;
      }
    } catch (error) {
      console.error(`Error sending message for user ${userId}:`, error);
      throw error;
    }
  }

  // Method to get user's conversations
  async getUserConversations(userId: string, limit: number = 10, offset: number = 0): Promise<ConversationsResponse> {
    try {
      // If the user ID is 'anonymous', redirect to login
      if (userId === 'anonymous') {
        // Redirect to login page
        window.location.href = '/login';
        throw new Error('Authentication required');
      } else {
        // Get token from localStorage
        const token = localStorage.getItem('auth_token');
        if (!token) {
          throw new Error('Authentication token not found');
        }

        const response = await this.client.get<ConversationsResponse>(
          `/api/${userId}/conversations?token=${encodeURIComponent(token)}`,
          {
            params: {
              limit,
              offset
            }
          }
        );
        return response.data;
      }
    } catch (error) {
      console.error(`Error getting conversations for user ${userId}:`, error);
      throw error;
    }
  }

  // Method to get messages for a specific conversation
  async getConversationMessages(
    userId: string,
    conversationId: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<MessagesResponse> {
    try {
      // If the user ID is 'anonymous', redirect to login
      if (userId === 'anonymous') {
        // Redirect to login page
        window.location.href = '/login';
        throw new Error('Authentication required');
      }

      // Get token from localStorage
      const token = localStorage.getItem('auth_token');
      if (!token) {
        throw new Error('Authentication token not found');
      }

      const response = await this.client.get<MessagesResponse>(
        `/api/${userId}/conversations/${conversationId}/messages?token=${encodeURIComponent(token)}`,
        {
          params: {
            limit,
            offset
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error(`Error getting messages for conversation ${conversationId} for user ${userId}:`, error);
      throw error;
    }
  }
}

// Export a singleton instance
export const apiClient = new ApiClient();

// Export types for use in components
export type { MessageData, ChatResponse, ConversationsResponse, MessagesResponse };