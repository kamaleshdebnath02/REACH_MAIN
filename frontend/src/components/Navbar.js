import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
    return (
        <nav className="navbar">
            <div className="logo">
                <img src="/images/reach.png" alt="REACH AI Health Awareness" />
                <h1>REACH AI Health Awareness</h1>
            </div>
            <ul className="nav-links">
                <li><Link to="/">Home</Link></li> {/* Link to Chatbot */}
                <li><Link to="/dashboard">Dashboard</Link></li> {/* Link to Dashboard */}
                <li><Link to="/about">About</Link></li>
                <li><Link to="/contact">Contact</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;
