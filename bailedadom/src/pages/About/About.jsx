import React from 'react';
import './about.css';

function About() {
  return (
    <div className="about-container">
      <header className="about-header">
        <h1>Meet our community.</h1>
        <p>Baile da Dom was started by passionate members of the dance community. To help this community grow and flourish we are always looking for people that want to volunteer or help in any way that they can.</p>
        <p>Do you have skills that might help our community grow, or do you have time to help us out at events? Send us a message and we will get back to you!</p>
      </header>
      <section className="community-section">
        <article className="community-member">
          <img src="charley-aimee.jpg" alt="Charley Aimée" />
          <h3>Charley Aimée</h3>
          <p>After ten years abroad, I couldn't believe this city did not have any Forró classes or teachers. It is my passion to share Forró, Samba de Gafieira, and...</p>
        </article>
        <article className="community-member">
          <img src="martijn.jpg" alt="Martijn" />
          <h3>Martijn</h3>
          <p>Martijn lives and works in Utrecht as a freelancer and team coach. In 2022 he got introduced to Forró and immediately got hooked. He now shares his passion...</p>
        </article>
        <article className="community-member">
          <img src="your-image.jpg" alt="You?" />
          <h3>You?</h3>
          <p>We are a small group of volunteers making things happen in Utrecht. Are you passionate about Forró or another aspect of Brazilian culture? Join us!</p>
        </article>
        {/* ... other members ... */}
      </section>
      {/* ... any additional sections ... */}
    </div>
  );
}

export default About;
