import React, { useState } from 'react';
import './NewChatBotIcon.css';

interface NewChatBotIconProps {
  onClick: () => void;
}

const NewChatBotIcon: React.FC<NewChatBotIconProps> = ({ onClick }) => {
  const [isVisible, setIsVisible] = useState(true);

  const handleClick = () => {
    onClick();
    // Hide the icon when chat is opened
    setIsVisible(false);
  };

  if (!isVisible) {
    return null; // Don't render the icon when chat is open
  }

  return (
    <div className="new-chatbot-icon-container" onClick={handleClick}>
      <div className="new-chatbot-icon">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="new-chatbot-icon-svg"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </div>
      <span className="new-chatbot-badge">AI</span>
    </div>
  );
};

export default NewChatBotIcon;