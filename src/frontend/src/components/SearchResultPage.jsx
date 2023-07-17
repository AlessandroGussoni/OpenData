import React from 'react';

const SearchResultPage = ({ location }) => {
  const { conversation } = location.state;

  return (
    <body>
      <Header handleNewChat={handleNewChat} />

      <div className="search-result">
        <ConversationSection conversation={conversation} />
      </div>

      <Footer />
    </body>
  );
};

export default SearchResultPage;
