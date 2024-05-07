import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const Login = ({ onClose, setProfile }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  // eslint-disable-next-line
  var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

  const handleLogin = () => {
    if (reg.test(username) === false) 
    {
        alert('Invalid Email Address');
    }
    else {
      const apiUrl = 'http://127.0.0.1:8080/users';
      axios.get(apiUrl, { params: {email: username, password: password} })
      .then((response) => {
        console.log('Server response:', response.data);
        setProfile(response.data.email);
        onClose();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    } 
  }

  const handleCreate = () => {
    const json = JSON.stringify({email: username, password: password});

    if (reg.test(username) === false) 
    {
        alert('Invalid Email Address');
    } else {
      const apiUrl = 'http://127.0.0.1:8080/users';
      axios.post(apiUrl, json, {
        headers: {
          'Content-Type': 'application/json'
        }      
      })
      .then((response) => {
        console.log('Server response:', response.data);
        onClose();
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  }

  return (
    <div className="login-overlay">
      <div className="login-container">
        <div className="close-button" onClick={onClose}>X</div>
        <h2>Login Page</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Login</button>
        <button onClick={handleCreate}>Create Account</button>
      </div>
    </div>
  );
}

export default Login;