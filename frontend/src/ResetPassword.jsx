import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaEye, FaEyeSlash, FaArrowLeft } from 'react-icons/fa';

import './Login.css';

const ResetPassword = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [isValidUsername, setIsValidUsername] = useState(true);
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isPasswordVisible, setIsPasswordVisible] = useState(false); // State for password visibility

    const [activeButton, setActiveButton] = useState('login');

    const nav = useNavigate();

    const handleButtonClick = (button) => {
        setActiveButton(button);
    };

    const validateUsername = (username) => {
        // Regular expression to allow only alphanumeric characters
        const regex = /^[a-zA-Z0-9]+$/;
        return regex.test(username);
    };

    const handleUsernameChange = (e) => {
        const username = e.target.value;
        setName(username);
        setIsValidUsername(validateUsername(username));
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        if (!isValidUsername) {
            setMessage("Username can only contain letters and numbers.");
            return;
        }
        try {
            const response = await axios.post('http://localhost:8080/register', {
                name,
                email,
                password,
            });
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response ? error.response.data.error : "An error occurred");
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8080/login', {
                name,
                password,
            });
            setMessage(response.data.message);
            localStorage.setItem('username', name);
            nav('/AccountHome');
        } catch (error) {
            setMessage(error.response.data.error);
        }
    };

    const togglePasswordVisibility = () => {
        setIsPasswordVisible(!isPasswordVisible);
    };

    return (
        <div className='login-container'>
            <div className='padding'>
                <button className="back-button" onClick={() => nav('/')}>
                    <FaArrowLeft /> <p>Back to Home</p>
                </button>

                <div className='login-toggle'>
                    <button 
                        className={`toggle-button ${activeButton === 'login' ? 'active' : ''}`} 
                        onClick={() => handleButtonClick('login')}
                        autoFocus
                    >
                        <h2>Login</h2>
                    </button>
                    <button 
                        className={`toggle-button ${activeButton === 'admin' ? 'active' : ''}`} 
                        onClick={() => handleButtonClick('admin')}
                    >
                        <h2>Admin Login</h2>
                    </button>
                    <button 
                        className={`toggle-button ${activeButton === 'register' ? 'active' : ''}`} 
                        onClick={() => handleButtonClick('register')}
                    >
                        <h2>Register</h2>
                    </button>
                </div>

                {activeButton === 'register' ? (
                    <form onSubmit={handleRegister}>
                        <input className='input' type="email" placeholder="Input email" value={email} onChange={(e) => setEmail(e.target.value)} required />
                        <input className='input' type="text" placeholder="Input username" value={name} onChange={handleUsernameChange} required />
                        <div className='password-container'>
                            <input
                                className='password' type={isPasswordVisible ? 'text' : 'password'}
                                placeholder="Input password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <button type="button" onClick={togglePasswordVisibility} className='eye-button'>
                                {isPasswordVisible ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                        {message && <p>{message}</p>}
                        <button className='butt' type='submit'>Register</button>
                    </form>
                ) : (
                    <form onSubmit={handleLogin}>
                        <input
                            className='input'
                            type="text"
                            placeholder="Input username"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                        <div className='password-container'>
                            {message && <p>{message}</p>}
                            <input
                                className='password' type={isPasswordVisible ? 'text' : 'password'}
                                placeholder="Input password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <button type="button" onClick={togglePasswordVisibility} className='eye-button'>
                                {isPasswordVisible ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                        <NavLink className="Nav" to="/ResetPassword">Forgot Password?</NavLink>
                        <br/>
                        <button className='butt' type='submit'>Login</button>
                    </form>
                )}
            </div>
        </div>
    );
};

export default ResetPassword;