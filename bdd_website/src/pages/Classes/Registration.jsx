import React from 'react';
import './registration.css';

function Registration() {
  return (
    <div className="register-container">
      <div className="register-header">
        <h1>Registration for classes</h1>
      </div>
      <form className="register-form">
        <label htmlFor="first-name">First name*</label>
        <input type="text" id="first-name" name="first-name" />

        <label htmlFor="last-name">Last name*</label>
        <input type="text" id="last-name" name="last-name" />

        <label htmlFor="email">E-mail address*</label>
        <input type="email" id="email" name="email" />

        <label htmlFor="course">Course*</label>
        <select id="course" name="course">
          <option value="block-2">Block 2</option>
          <option value="trial">Trial class (only for Level 0)</option>
          <option value="individual-class">Individual class</option>
        </select>

        <label htmlFor="role">Dance role*</label>
        <select id="role" name="role">
          <option value="follower">Follower</option>
          <option value="leader">Leader</option>
          <option value="fluid">Fluid</option>
        </select>

        <label htmlFor="level">Level*</label>
        <select id="level" name="level">
          <option value="level-0">Level 0</option>
          <option value="level-1">Level 1</option>
          <option value="level-2">Level 2</option>
        </select>

        <label htmlFor="phone">Phone number</label>
        <input type="phone" id="phone" name="phone" />

        <button type="submit" className="register-button">Book class</button>
      </form>
    </div>
  );
}

export default Registration;
