import React from 'react';

const Search = ({ searchTerm, handleSearchChange, handleSearchSubmit }) => {
  return (
    <form onSubmit={handleSearchSubmit}>
      <div className="search-bar">
        <i className="fa-sharp fa-solid fa-magnifying-glass"></i>
        <input
          id="search-input"
          className="search-input"
          type="text"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>
    </form>
  );
};

export default Search;
