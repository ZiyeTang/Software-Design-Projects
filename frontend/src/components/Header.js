import React, { useState } from 'react';
import "./Header.css"
import Login from './Login';

function Header() {
  const [loginVisible, setLoginVisible] = useState(false);
  const [profile, setProfile] = useState('');

  const openLogin = () => {
    setLoginVisible(true);
  }

  const closeLogin = () => {
    setLoginVisible(false);
  }

  return (
      <header className="header">
        <div className="header-title">Classroom Availability</div>
        {profile === '' ?
        <>
        <button className="login-button" onClick={openLogin}>Login</button>
        {loginVisible && <Login onClose={closeLogin} setProfile={setProfile}/>}
        </>
        : <div className='profile-name'>{profile}</div>}
      </header>
      
    );
}
export default Header;