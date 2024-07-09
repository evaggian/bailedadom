import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './navigation.css';

function Navigation() {
    const [isNavExpanded, setIsNavExpanded] = useState(false);

    return (
      <nav className="navigation">
        <div className="nav-brand-and-logo">
          <NavLink to="/">
            <img src={process.env.PUBLIC_URL + '/logo.png'} alt="Baile da Dom Logo" className="logo" />
          </NavLink>
        </div>
        <span className="brand-text">Baile da Dom</span>
        <div
          className="nav-toggle"
          onClick={() => setIsNavExpanded(!isNavExpanded)}
        >
          <i className="fas fa-bars"></i> {/* Ensure Font Awesome is included */}
        </div>
        <div className={`nav-links ${isNavExpanded ? 'active' : ''}`}>
          <NavLink to="/" exact activeClassName="active" onClick={() => setIsNavExpanded(false)}>Home</NavLink>
          <NavLink to="/classes" activeClassName="active" onClick={() => setIsNavExpanded(false)}>Classes</NavLink>
          <NavLink to="/events" activeClassName="active" onClick={() => setIsNavExpanded(false)}>Events</NavLink>
          <NavLink to="/about" activeClassName="active" onClick={() => setIsNavExpanded(false)}>About</NavLink>
          <NavLink to="/contact" activeClassName="active" onClick={() => setIsNavExpanded(false)}>Contact</NavLink>
        </div>
      </nav>
    );
  }


export default Navigation;
