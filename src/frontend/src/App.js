import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import Navigation from './components/Navigation';
import SearchSection from './components/SearchSection';
import ImageSection from './components/ImageSection';
import AboutSection from './components/AboutSection';
import config from './frontend_config.json';

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [conversation, setConversation] = useState([]);
  const [showChatBox, setShowChatBox] = useState(false);
  const [searchTrigger, setSearchTrigger] = useState(0)
  const [configData, setConfigData] = useState(config);
  const url = configData.use_test_endpoint ? "http://127.0.0.1:8000/query_datasets_test" : "http://127.0.0.1:8000/query_datasets";

  console.log(url)
  useEffect(() => {
    if (searchTrigger > 0) {

      var bodyFormData = {
        query: searchTerm
      };
      console.log(searchTerm)
      
      axios.post(url, bodyFormData)
        .then(response => {
          const newMessage = `Answer: ${response.data.answer}`;
          console.log('Passed')
          setConversation([...conversation, newMessage]);
          setSearchTerm('');
          setShowChatBox(true);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }, [searchTrigger]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm !== '') {
      setSearchTrigger(searchTrigger => searchTrigger + 1)
    } else {
      return;
    }
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
