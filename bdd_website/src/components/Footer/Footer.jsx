import React from 'react';
import './footer.css'; // Make sure this CSS file contains the necessary styles
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faFacebook, faInstagram } from "@fortawesome/free-brands-svg-icons";
import { faEnvelope } from '@fortawesome/free-solid-svg-icons';


function Footer() {
  return (
    <footer className="footer">
      <div className="footer-social">
        Contact us
        <a href="https://www.facebook.com/BailedaDom">
          <FontAwesomeIcon icon={faFacebook} />
        </a>
        <a href="https://www.instagram.com/bailedadom_utrecht">
          <FontAwesomeIcon icon={faInstagram} />
        </a>
        <a href="mailto:contact@bailedadom.nl">
          <FontAwesomeIcon icon={faEnvelope} />
        </a>
      </div>
      <div className="footer-rights">
        <p>©2024 by Stichting Baile da Dom - KvK: 90262999</p>
      </div>
    </footer>
  );
}

export default Footer;
