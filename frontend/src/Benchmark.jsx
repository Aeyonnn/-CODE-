import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import axios from "axios";
import "./Benchmark.css";

const Benchmark = () => {
    const [array, setArray] = useState([]);
    const [showResults, setShowResults] = useState(false);
    const [article, setArticle] = useState("");
    const username = localStorage.getItem('username');

    const fetchapi = async () => {
        try {
            const response = await axios.get("http://localhost:8080/api/algo");
            setArray(response.data);
            setShowResults(true);
        } catch (error) {
            console.error("Error fetching data", error);
        }
    };

    const handlePredict = async (event) => {
        event.preventDefault();
        await fetchapi(); 
    };

    return (
        <div className="container">
            <div className="topnav">
                <div className="nav-left">
                    <h2>VERITASIUM: FAKE NEWS DETECTION</h2>
                </div>
                <div className="nav-right">
                    <h2>Hello, {username}!</h2>
                    <img className="icon" src="icon.png" alt="User Icon" />
                    <h2>|</h2>
                    <h2>
                        <NavLink className="Nav" to="/">Logout</NavLink>
                    </h2>
                </div>
            </div>

            <div className="box">
                <form onSubmit={handlePredict}>    
                    <h2 className="box-text-header">Input News Article</h2>
                    <input
                        type="text"
                        className="text-box"
                        value={article}
                        onChange={(e) => setArticle(e.target.value)} // Capture input
                        placeholder="Enter your news article here..."
                    />
                    <div style={{ padding: "15px" }}>
                        <button className="butt" style={{ fontSize: '20px' }} type="submit">
                            PREDICT
                        </button>
                    </div>
                </form>
            </div>         

            {showResults && (
                <div className="container-vertical">
                    {array.length > 0 ? (
                        array.map((algo) => (
                            <div className="container-horizontal" key={algo.model_name}>
                                <h2 className="container-text">
                                    {algo.model_name}: {algo.accuracy}%
                                </h2>
                                <a href="https://www.geeksforgeeks.org/machine-learning-algorithms/" target="_blank" rel="noopener noreferrer">
                                    More Details
                                </a>
                            </div>
                        ))
                    ) : (
                        <h2 className="container-text">No results found</h2>
                    )}
                </div>
            )}
        </div>
    );
};

export default Benchmark;