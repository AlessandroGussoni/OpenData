import React from 'react';

const SearchSection = ({searchTerm,
                        datasetNum,
                        conversation,
                        showChatBox,
                        onSearchChange,
                        onSearchSubmit,}) => {
  return (
    <>
        <input
          type="text"
          placeholder="Enter your search term..."
          value={searchTerm}
          onChange={onSearchChange}
        />
        
      
      {showChatBox && (
        <div className="conversation">
          {conversation.map((message, index) => (
            <div key={index}>{message}</div>
          ))}
        </div>
      )}
    </>
  );
};

export default SearchSection;
