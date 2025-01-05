import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'


function Navbar() {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">Home</Link>
            </div>
            <ul className="navbar-links">
                <li><Link to="/home">Home</Link></li>
                <li><Link to="/song-levels">Order Song</Link></li>   
            </ul>
        </nav>
    );
}

export default Navbar;