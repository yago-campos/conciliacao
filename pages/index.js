// pages/index.js
import React, { useState } from 'react';
import Login from '../components/Login'; // Importando o componente de Login

const Home = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <div>
      {!isLoggedIn ? (
        <Login onLogin={handleLogin} />
      ) : (
        <h1>Bem-vindo ao sistema!</h1>
      )}
    </div>
  );
};

export default Home;