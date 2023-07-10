import React, { useState } from 'react';
import './App.css';
import Navigation from './components/Navigation';
import SearchSection from './components/SearchSection';
import ImageSection from './components/ImageSection';
import AboutSection from './components/AboutSection';

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [conversation, setConversation] = useState([]);
  const [showChatBox, setShowChatBox] = useState(false);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm !== '') {
    const newMessage = `You entered: ${searchTerm}`;
    setConversation([...conversation, newMessage]);
    setSearchTerm('');
    setShowChatBox(true);
    }
    else return
  };

  const handleNewChat = () => {
    setConversation([]);
    setShowChatBox(false);
  };

  return (
    <div className="app">
      <header>
        
        <Navigation />
        <button className="new-chat-btn" onClick={handleNewChat}>
          New Chat
        </button>
      </header>
      <h1 className="title">Open Search</h1>
      <main>
        <SearchSection
          searchTerm={searchTerm}
          conversation={conversation}
          showChatBox={showChatBox}
          onSearchChange={handleSearchChange}
          onSearchSubmit={handleSearchSubmit}
        />
        <ImageSection />
        <AboutSection />
      </main>
    </div>
  );
};

export default App;
