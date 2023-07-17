import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import axios from 'axios';
import config from './frontend_config.json';

import Logo from "./images/logo.png"


/* TODO: Pulire sto schifo
   TODO: migliorare loading animation
   TODO: Aggiungere immagini, descrizioni e contatti
*/

const App = () => {

  const [datasetNum, setDatasetNum] = useState(0)

  const [searchTerm, setSearchTerm] = useState('');
  const [conversation, setConversation] = useState([]);
  const [showChatBox, setShowChatBox] = useState(false);
  const [searchTrigger, setSearchTrigger] = useState(0)
  const [loading, setLoading] = useState(false);

  const [configData, setConfigData] = useState(config);
  const queryUrl = configData.use_test_endpoint ? "http://127.0.0.1:8000/query_datasets_test" : "http://127.0.0.1:8000/query_datasets";

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/list_datasets")
    .then(response => {
      setDatasetNum(response.data.names.length)
    })
    .catch(error => {
      console.error('Error:', error);
    });
    }, [])

  useEffect(() => {
    if (searchTrigger > 0) {
      setLoading(true);
      var bodyFormData = {
        query: searchTerm
      };
      
      axios.post(queryUrl, bodyFormData)
        .then(response => {
          const newMessage = `Answer: ${response.data.answer}`;
          console.log('Passed')
          setConversation([...conversation, newMessage]);
          setSearchTerm('');
          setShowChatBox(true);
        })
        .catch(error => {
          console.error('Error:', error);
        })
        .finally(() => {
          setLoading(false)
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

  const inputRef = useRef(null);

  return (
    <body>
    <header>
        <nav class="navbar">
            <ul>
                <li>
                    <a class="link" href="value4">Gmail</a>
                </li>
                <li>
                    <a class="link" href="value3">Images</a>
                </li>
                <li>
                    <div class="circle-shadow">
                        <a class="menu-icon" href="value2"><i class="fas fa-bars"></i></a>
                    </div>
                </li>
                <li>
                    <div class="circle-shadow">
                    <button className="new-chat-btn" onClick={handleNewChat}>New Search</button>
                    </div>
                </li>
            </ul>
        </nav>
    </header>

    <section class="content-section">
        <div class="content-wrapper">
          <img class="logo-img" src={Logo} alt="Logo" />
          <form onSubmit={handleSearchSubmit}>
            <div class="search-bar">
              <i class="fa-sharp fa-solid fa-magnifying-glass"></i>
              <input
                id="search-input"
                class="search-input"
                type="text"
                ref={inputRef}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSearchSubmit(e);
                  }
                }}
                value={searchTerm}
                onChange={handleSearchChange}
              />
            </div>
            
          </form>
          {loading && (
            <div className="loading-animation" style={{ color: "#2500FF" }}>
              Loading...
            </div>
          )}
          {showChatBox && (
                <div className="conversation">
                  {conversation.map((message, index) => (
                    <div key={index}>{message}</div>
                  ))}
                </div>
              )}
          <div class="search-btns">
              <button class="google-search-btn">Google Search</button>
              <button class="lucky-search-btn">I'm Feeling Lucky</button>
            </div>
            <div class="language">
              <p>Google Offered in: <a href="value">Maori</a></p>
            </div>
        </div>
      </section>

    <footer>
        <div class="footer-content upper-footer">
            <p>New Zealand</p>
        </div>
        <div class="footer-content lower-footer">
            <ul class="lower-left-footer">
                <li>
                    <a href="case">About</a>
                </li>
                <li>
                    <a href="case1">Advertising</a>
                </li>
                <li>
                    <a href="case2">Business</a>
                </li>
                <li>
                    <a href="case3">How Search Works</a>
                </li>
            </ul>
            <ul class="lower-right-footer">
                <li>
                    <a href="test">Privacy</a>
                </li>
                <li>
                    <a href="test2">Terms</a>
                </li>
                <li>
                    <a href="test3">Settings</a>
                </li>
            </ul>
        </div>
    </footer>
</body>

  )
};

export default App;
