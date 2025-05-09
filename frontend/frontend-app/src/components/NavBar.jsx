import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'


function Navbar() {

    return (
        <nav className="navbar">
            <div className='navbar-container'>
                <div className="navbar-brand">
                    <Link to="/">Home</Link>
                    
                </div>
                <ul className="navbar-links">
                    {/*<li><Link to="/personalized-songs-blogs">Blogs</Link></li>*/}
                    <li><Link to="/personalized-song-levels">Order Song</Link></li>   
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;