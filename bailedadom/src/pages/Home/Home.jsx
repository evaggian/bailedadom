import React from 'react';
import { NavLink } from 'react-router-dom'; // Import NavLink
import './home.css';

function Home() {
  return (
    <div className="home-container">
      <header className="home-header">
        {/* Updated to use the actual logo path from Navigation */}
        {/* <img src={process.env.PUBLIC_URL + '/logo.png'} alt="Baile da Dom Logo" className="logo"/> */}
      </header>
      <main className="home-main">
        <section className="intro-section">
          <h1>Forró with Baile da Dom</h1>
          <p>Experience the joy of Forró with us. Forró is a partner dance from the northeast of Brazil. ...</p>
        </section>
        <section className="next-event-section">
          <h2>Next event</h2>
          {/* Event details */}
        </section>
        <div className="cards-container">
          {/* Convert buttons to NavLinks for consistency */}
          <div className="card classes">
            <h3>Classes</h3>
            <NavLink to="/" exact className="button">Sign up</NavLink>
          </div>
          <div className="card events">
            <h3>Events</h3>
            <NavLink to="/events" className="button">Event calendar</NavLink>
          </div>
          <div className="card about">
            <h3>About</h3>
            <NavLink to="/about" className="button">About</NavLink>
          </div>
        </div>
        <footer className="home-footer">
          <p>Contact:</p>
          {/* Contact details */}
        </footer>
      </main>
    </div>
  );
}

export default Home;
