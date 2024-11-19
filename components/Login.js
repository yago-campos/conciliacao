import React, { useState } from 'react';
import { useRouter } from 'next/router';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  // Lista de usuários e senhas
  const validUsers = [
    { username: 'cs', password: 'cs' },
    { username: 'admin', password: 'admin' },
    { username: 'coordenadorcs', password: 'coordenador' },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();

    // Verifica se o usuário e senha correspondem a algum na lista
    const isValid = validUsers.some(
      (user) => user.username === username && user.password === password
    );

    if (isValid) {
      router.push('/home'); // Redireciona para a página inicial após login bem-sucedido
    } else {
      alert('Usuário ou senha incorretos'); // Falha no login
    }
  };

  return (
    <div
      className="login-container"
      style={{
        backgroundImage: 'url(/images/fundoverdefuncional.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        padding: '20px',
      }}
    >
      <form
        onSubmit={handleSubmit}
        style={{
          textAlign: 'center',
          backgroundColor: 'rgba(255, 255, 255, 0.8)',
          padding: '20px',
          borderRadius: '8px',
        }}
      >
        <p style={{ textAlign: 'center', fontSize: '1.5rem', marginBottom: '20px' }}>Seja bem-vindo!</p>
        <label htmlFor="username" style={{ display: 'block', marginBottom: '5px' }}>Usuário:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{
            padding: '10px',
            marginBottom: '10px',
            width: '100%',
            maxWidth: '300px',
          }}
        />
        <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>Senha:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{
            padding: '10px',
            marginBottom: '20px',
            width: '100%',
            maxWidth: '300px',
          }}
        />
        <button
          type="submit"
          className="animated-button"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007BFF',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Entrar
        </button>
      </form>
    </div>
  );
};

export default Login;
