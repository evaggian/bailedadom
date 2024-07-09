import React from 'react';
import { NavLink } from 'react-router-dom'; // Import NavLink
import './classes.css';

function Classes() {
  return (
    <div className="classes-container">
      <header className="classes-header">
        <h1>Forró Classes</h1>
        <p>We have regular classes on Wednesdays with our great teacher Bruna Azevedo from Forró The Hague. Classes are on two levels: beginners and an open level...</p>
        {/* ... */}
      </header>

      <section className="schedule">
        <h2>Program Spring 2024</h2>
        <div className="block">
          <h3>Block 2</h3>
          {/* ... */}
        </div>
        <div className="block">
          <h3>Block 3</h3>
          {/* ... */}
        </div>
      </section>

      <footer className="register-footer">
        {/* Convert register button to NavLink */}
        <NavLink to="/register" className="register-button">Register for classes</NavLink>
      </footer>
    </div>
  );
}

export default Classes;
