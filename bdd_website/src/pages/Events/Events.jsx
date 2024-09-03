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
          <h3>Next event: Saturday 14th of September 2024</h3>
          <div className="event-content">
            <div className="event-image">
              <img src={process.env.PUBLIC_URL + "/poster_party.png"} alt="Event" className='event-image'/>
            </div>
            <div className="event-description">
              <p>Get ready for an unforgettable experience on Saturday, September 14th as Baile da Dom brings you a day packed with engaging workshops, 
                free practice sessions, and the first forró party of the season in Utrecht!</p>
              <h3>Workshops & Party</h3>
              <p>Join us for workshops led by the incredible teacher Hongsie from Bora forró in Amsterdam. Not only will she guide you through the sessions, but she'll also be spinning tracks for us later. Her vibrant music selection will be perfectly complemented by DJ Lanús' tunes.</p> 
              <p>Never danced forró before? Eager to introduce your friends to forró? Join our hour-long free crash course led by our in-house teacher, Empar.</p>
              <h3>Event schedule</h3>
              <ul className="center-list">
                <li>14:00 - 15:00: Open level workshop with Hongsie (Sala Gonzaga)</li>
                <li>15:30 - 16:30: Intermediate workshop with Hongsie (Sala Gonzaga)</li>
                <li>16:30 - 19:00: Free Practice for Everyone (Sala Gonzaga)</li>
                <li>19:00 - 20:00: Beginners Crash Course with Empar (Sala Gonzaguinha)</li>
                <li>19:00 - 23:00: Party with DJ Hongsie and DJ Lanús (Sala Gonzaga)</li>
              </ul>
              <p>📍 Location: Theaterhuis de Berenkuil, Biltstraat 166</p>
              <button>Tickets</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Events;
