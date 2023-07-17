import React from 'react';

const Header = ({ handleNewChat }) => {
  return (
    <header>
      <nav className="navbar">
        <ul>
          <li>
            <a className="link" href="value4">
              Gmail
            </a>
          </li>
          <li>
            <a className="link" href="value3">
              Images
            </a>
          </li>
          <li>
            <div className="circle-shadow">
              <a className="menu-icon" href="value2">
                <i className="fas fa-bars"></i>
              </a>
            </div>
          </li>
          <li>
            <div className="circle-shadow">
              <button className="new-chat-btn" onClick={handleNewChat}>
                New Search
              </button>
            </div>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
