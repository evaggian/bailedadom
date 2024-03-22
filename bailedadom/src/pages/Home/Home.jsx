import React from 'react';
import { NavLink } from 'react-router-dom';
import './home.css';

function Home() {
  return (
    <div className="home-container">
      <header className="home-header">
      </header>
      <main className="home-main">
      <div className="section-container">
        <section className="intro-section">
          <h1>Forró with Baile da Dom</h1>
          <p>Experience the joy of Forró with us. Forró is a partner dance from the northeast of Brazil. We are bringing this beautiful dance and its culture to Utrecht. Join us in our regular classes on Wednesdays and a party each month. We also organize workshops with outside teachers.</p>
          <p>And if you like Samba de Gafiera, we are planning to organize classes for that as well.</p>
        </section>
        <section className="next-event-section">
          <img src={process.env.PUBLIC_URL + '/forro_party.jpg'} alt="Next Event" className="event-image" />
        </section>
      </div>
        <div className="cards-container">
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
