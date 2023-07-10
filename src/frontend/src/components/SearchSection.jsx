import React from 'react';

const SearchSection = ({searchTerm,
                        conversation,
                        showChatBox,
                        onSearchChange,
                        onSearchSubmit,}) => {
  return (
    <section id="search-section" className="search-section">
      <h2 className="section-title">Search</h2>
      <form className="search-form" onSubmit={onSearchSubmit}>
        <input
          type="text"
          placeholder="Enter your search term..."
          value={searchTerm}
          onChange={onSearchChange}
        />
        <button type="submit">Start Conversation</button>
      </form>
      {showChatBox && (
        <div className="conversation">
          {conversation.map((message, index) => (
            <div key={index}>{message}</div>
          ))}
        </div>
      )}
    </section>
  );
};

export default SearchSection;
