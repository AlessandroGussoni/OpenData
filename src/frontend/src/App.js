import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import axios from 'axios';

import config from './frontend_config.json';

import ImageSection from "./components/ImageSection"
import AboutSection from "./components/AboutSection"
import Header from "./components/Header"
import SearchSection from "./components/SearchSection"

import Logo from "./images/logo.png"
import OpenData from "./images/opendata.png"
import Inps from "./images/inps2.png"
import PortalOpenData from "./images/popendata.png"


/* TODO: migliorare loading animation
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
    .then(response => {setDatasetNum(response.data.names.length)})
    .catch(error => {console.error('Error:', error)});
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
        .catch(error => {console.error('Error:', error)})
        .finally(() => {setLoading(false)});
    }
  }, [searchTrigger]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm !== '') {setSearchTrigger(searchTrigger => searchTrigger + 1)} 
    else {return}
  };

  const handleNewChat = () => {
    setConversation([]);
    setShowChatBox(false);
  };

  const inputRef = useRef(null);

  return (
    <body>
      <Header handleNewChat={handleNewChat} />

      <section class="content-section">
        <div class="content-wrapper">
          <img class="logo-img" src={Logo} alt="Logo" />
          <SearchSection searchTerm={searchTerm} handleSearchChange={handleSearchChange} handleSearchSubmit={handleSearchSubmit} />
          {loading && (<div className="loading-animation" style={{ color: "#2500FF" }}>Loading...</div>)}
          {showChatBox && (<div className="conversation">{conversation.map((message, index) => (<div key={index}>{message}</div>))}</div>)}
          <ImageSection OpenData={OpenData} Inps={Inps} PortalOpenData={PortalOpenData}/>
        </div>
      </section>
    
      <AboutSection />
    </body>

  )
};

export default App;
