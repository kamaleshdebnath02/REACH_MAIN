import React from 'react';
import './Footer.css';  // Make sure to create a corresponding CSS file for styling

function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">
                <p>© 2024 REACH AI Health Awareness. All rights reserved.</p>
                <ul className="footer-links">
                    <li><a href="#about">About Us</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#contact">Contact</a></li>
                    <li><a href="#privacy">Privacy Policy</a></li>
                </ul>
            </div>
            <div className="social-media-links">
                <a href="https://facebook.com" target="_blank" rel="noopener noreferrer"><img src="/icons/facebook-icon.png" alt="Facebook" /></a>
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer"><img src="/icons/twitter-icon.png" alt="Twitter" /></a>
                <a href="https://instagram.com" target="_blank" rel="noopener noreferrer"><img src="/icons/instagram-icon.png" alt="Instagram" /></a>
            </div>
        </footer>
    );
}

export default Footer;
