import React from 'react';
import './events.css';

function Events() {
  return (
    <div className="events">
      <div className="events-header">
        <h1>Events</h1>
      </div>
      <div className="event-list">
        <div className="event-card">
          <h2>Party at the Kweekvijver</h2>
          <p>20:00 - 00:00</p>
          <button>Tickets</button>
        </div>
        <div className="event-card">
          <h2>Party at the Kweekvijver</h2>
          <p>20:00 - 00:00</p>
          <button>Tickets</button>
        </div>
      </div>
      <div className="past-events">
        <h2>Past events</h2>
        <div className="event-card">
          <h2>Party at the Kweekvijver</h2>
          <p>20:00 - 00:00</p>
          <button>Impression</button>
        </div>
      </div>
    </div>
  );
}

export default Events;
