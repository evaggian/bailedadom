import React from 'react';
import { NavLink } from 'react-router-dom';
import './home.css';
import icon1 from '../../assets/Sanfona.svg';
import icon2 from '../../assets/Triangulo.svg';
import icon3 from '../../assets/Zabumba.svg';

function Home() {
  return (
    <div className="home-container">
      <header className="home-header"></header>
      <main className="home-main">
        <div className="section-container">
          <section className="intro-section">
            <h1>Forró with Baile da Dom</h1>
            <p>Experience the joy of Forró with us. Forró is a partner dance from the northeast of Brazil. We are bringing this beautiful dance and its culture to Utrecht.</p>
            <p>Join us in our regular classes on Wednesdays and a party each month. We also organize workshops with teachers from all over the world.</p>
          </section>
          <section className="next-event-section">
            <img src={process.env.PUBLIC_URL + '/IMG_5870.jpeg'} alt="" className="event-image" />
          </section>
        </div>
        <div className="cards-container">
          <NavLink to="/classes" className="card-link">
            <div className="card classes">
              <h4>Classes</h4>
              <p>Find out more about our weekly classes and sign up.</p>
              <img src={icon1} alt="Sanfona" className="svg-icon" />
            </div>
          </NavLink>
          <NavLink to="/events" className="card-link">
            <div className="card events">
              <h4>Parties</h4>
              <p>Join our monthly parties and get your tickets here.</p>
              <img src={icon2} alt="Triangulo" className="svg-icon" />
            </div>
          </NavLink>
          <NavLink to="/events" className="card-link">
            <div className="card workshops">
              <h4>Calendar</h4>
              <p>Check out our calendar and don't miss out on the upcoming forró events.</p>
              <img src={icon3} alt="Zabumba" className="svg-icon" />
            </div>
          </NavLink>
        </div>

        <div className="instagram-section">
          <h4>Interested in our latest news? Follow us on Instagram <a href="https://www.instagram.com/bailedadom_utrecht">@bailedadom_utrecht</a></h4>
        </div>
        <div className="spotify-section">
          <h4>Listen to our forró playlists</h4>
          <div className="playlists-container">
            <iframe src="https://open.spotify.com/embed/playlist/2fqqpz3yeI50Mbji6nQqUk?utm_source=generator" width="300" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            <iframe src="https://open.spotify.com/embed/playlist/4wLUxqsC8TzQwCAzMD6ajI?utm_source=generator" width="300" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Home;
