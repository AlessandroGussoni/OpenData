import React from 'react';

const ConversationSection = ({ conversation }) => {
  return (
    <div className="conversation">
      {conversation.map((message, index) => (
        <div key={index}>{message}</div>
      ))}
    </div>
  );
};

export default ConversationSection;