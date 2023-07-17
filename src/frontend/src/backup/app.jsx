(
    <div className="app">
      <header>
      <h1 className="title">Open Search</h1>
        <Navigation />
        <button className="new-chat-btn" onClick={handleNewChat}>
          New Chat
        </button>    

      </header>
      <main>
        <SearchSection
          searchTerm={searchTerm}
          datasetNum={datasetNum}
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


# search 

<section id="search-section" className="search-section">
      <h2 className="section-title">Gli Open Data Italia incontrano l'AI</h2>
      <h4>Interagisci con più di {datasetNum} datasets con la semplicità del linguaggio naturale</h4>
      <form className="search-form" onSubmit={onSearchSubmit}></form>

      <button type="submit">Start Conversation</button>

      </form>