import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import "./Home.css";

const Home = () => {
  const [showPopup, setShowPopup] = useState(false);

  const handleBenchmarkClick = () => {
    setShowPopup(true);
  };

  const closePopup = () => {
    setShowPopup(false);
  };

  return (
    <div className="App">
      <nav className="navbar">
        <div className="logo" onClick={() => window.location.href = '/'}>
          VERITASIUM
        </div>
        <div className="nav-buttons">
          <button>Home</button>
          <button>Developers</button>
          <button onClick={handleBenchmarkClick}>Benchmark</button>
        </div>
      </nav>

      <section className="hero hero1">
        <h1>Why Fake News Detection Matters</h1>
        <p>In today's digital age, misinformation spreads rapidly. Our mission is to combat fake news and promote truth.</p>
      </section>

      <section className="hero hero2">
        <div className="developer">
          <img src="src/assets/aaron.jpg" alt="Aaron Alimbon" />
          <h2>Aaron Alimbon</h2>
          <p>Specialist in web development and user experience.</p>
        </div>
        <div className="developer">
          <img src="src/assets/matthew.jpg" alt="Matthew Centeno" />
          <h2>Matthew Centeno</h2>
          <p>Expert in machine learning and data analysis.</p>
        </div>
      </section>

      <section className="hero hero3">
        <h1>Start Benchmarking Today!</h1>
        <p>Join us in the fight against fake news. Click below to begin.</p>
        <button onClick={handleBenchmarkClick}>Benchmark</button>
      </section>

      {showPopup && (
        <div className="popup">
          <div className="popup-content">
            <span className="close" onClick={closePopup}>&times;</span>
            <h2>Account Required</h2>
            <p>You need to create an account for security and data storing purposes.</p>
            <NavLink to="/Login" className="navlink-button" onClick={closePopup}>Go to Login</NavLink>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;