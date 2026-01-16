import React, { useState, useEffect, useRef } from 'react';
import './NewChatInterface.css';
import { apiClient, ChatResponse, MessagesResponse, ConversationsResponse } from '../services/apiClient';

interface Message {
  id: number;
  sender_type: 'user' | 'assistant';
  content: string;
  timestamp: string;
  tool_calls?: any[];
}

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

interface NewChatInterfaceProps {
  userId: string;
  isOpen: boolean;
  onClose: () => void;
}

const NewChatInterface: React.FC<NewChatInterfaceProps> = ({ userId, isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [showConversations, setShowConversations] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Load conversation history when component mounts or when conversation changes
  useEffect(() => {
    if (currentConversationId) {
      loadConversationHistory();
    } else {
      // Load available conversations
      loadConversations();
    }
  }, [currentConversationId]);

  const loadConversations = async () => {
    try {
      const response: ConversationsResponse = await apiClient.getUserConversations(userId);
      setConversations(response.conversations);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadConversationHistory = async () => {
    if (!currentConversationId) return;

    try {
      const response: MessagesResponse = await apiClient.getConversationMessages(userId, currentConversationId);
      setMessages(response.messages);
    } catch (error) {
      console.error('Error loading conversation history:', error);
      // Show error message in the chat
      setMessages([
        {
          id: 1,
          sender_type: 'assistant',
          content: 'Sorry, I encountered an error loading the conversation history. Please try again.',
          timestamp: new Date().toISOString(),
        }
      ]);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: messages.length + 1,
      sender_type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send message to API
      const response: ChatResponse = await apiClient.sendMessage(userId, inputValue, currentConversationId || undefined);

      // Update conversation ID if this is a new conversation
      if (!currentConversationId) {
        setCurrentConversationId(response.conversation_id);
      }

      // Add assistant response to the chat
      const assistantMessage: Message = {
        id: messages.length + 2,
        sender_type: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        tool_calls: response.tool_calls
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: messages.length + 2,
        sender_type: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleNewConversation = () => {
    setCurrentConversationId(null);
    setMessages([]);
    setShowConversations(false);
  };

  const handleSelectConversation = (conversationId: number) => {
    setCurrentConversationId(conversationId);
    setShowConversations(false);
  };

  const handleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  const handleNewConversationClick = () => {
    setCurrentConversationId(null);
    setMessages([]);
    setShowConversations(false);
  };

  const handleSelectConversationClick = (conversationId: number) => {
    setCurrentConversationId(conversationId);
    setShowConversations(false);
  };

  if (isMinimized) {
    return (
      <div className="new-chat-interface minimized">
        <div className="chat-header">
          <div className="chat-title">AI Todo Assistant</div>
          <div className="chat-controls">
            <button
              className="header-button maximize-button"
              onClick={handleMinimize}
              title="Expand"
            >
              +
            </button>
            <button
              className="header-button close-button"
              onClick={onClose}
              title="Close"
            >
              ×
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`new-chat-interface ${isMinimized ? 'minimized' : ''} ${isOpen ? '' : 'hidden'}`}>
      {!isMinimized ? (
        <>
          <div className="chat-header">
            <div className="chat-header-left">
              <button
                className="header-button conversations-button"
                onClick={() => setShowConversations(!showConversations)}
                title="View conversations"
              >
                ≡
              </button>
              <div className="chat-title">AI Todo Assistant</div>
            </div>
            <div className="chat-controls">
              <button
                className="header-button minimize-button"
                onClick={handleMinimize}
                title="Minimize"
              >
                −
              </button>
              <button
                className="header-button close-button"
                onClick={onClose}
                title="Close"
              >
                ×
              </button>
            </div>
          </div>

          {showConversations && (
            <div className="conversations-list">
              <div className="conversations-header">
                <h3>Conversations</h3>
                <button
                  className="new-conversation-button"
                  onClick={handleNewConversationClick}
                >
                  <span>+ New</span>
                </button>
              </div>
              {conversations.map(conversation => (
                <div
                  key={conversation.id}
                  className={`conversation-item ${conversation.id === currentConversationId ? 'active' : ''}`}
                  onClick={() => handleSelectConversationClick(conversation.id)}
                >
                  <div className="conversation-title">
                    {conversation.title || `Conversation ${conversation.id}`}
                  </div>
                  <div className="conversation-date">
                    {new Date(conversation.updated_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
              {conversations.length === 0 && (
                <div className="no-conversations">No conversations yet</div>
              )}
            </div>
          )}

          <div className="chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.sender_type}-message`}
              >
                <div className="message-content">{message.content}</div>
                <div className="message-timestamp">
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="typing-indicator">
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
                <div className="typing-dot"></div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me to add, list, update, or complete tasks..."
              className="chat-input"
              rows={1}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="send-button"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="send-icon"
              >
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </>
      ) : (
        <div className="chat-header">
          <div className="chat-title">AI Todo Assistant</div>
          <div className="chat-controls">
            <button
              className="header-button maximize-button"
              onClick={handleMinimize}
              title="Expand"
            >
              +
            </button>
            <button
              className="header-button close-button"
              onClick={onClose}
              title="Close"
            >
              ×
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default NewChatInterface;