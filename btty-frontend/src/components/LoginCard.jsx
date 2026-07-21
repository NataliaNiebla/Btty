import React, { useState } from 'react';
import { styles } from '../styles/themeStyles';

export default function LoginCard({ token, onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(email, password);
  };

  return (
    <div style={{ ...styles.card, backgroundColor: token ? '#e8f5e9' : '#fff5d6' }}>
      <div style={styles.cardHeader}>
        <h3 style={styles.cardTitle}>{token ? '✅ Sesión Activa' : '🔐 Iniciar Sesión'}</h3>
        <div style={styles.badgeDecoration}>✦</div>
      </div>

      {!token ? (
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Correo Electrónico</label>
            <input 
              type="email" 
              placeholder="usuario@btty.com"
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              required 
              style={styles.input}
            />
          </div>
          <div style={styles.inputGroup}>
            <label style={styles.label}>Contraseña</label>
            <input 
              type="password" 
              placeholder="••••••••"
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
              style={styles.input}
            />
          </div>
          <button type="submit" style={styles.primaryBtn}>
            Ingresar al Sistema
          </button>
        </form>
      ) : (
        <div>
          <p style={{ fontSize: '13px', color: '#2e7d32', marginBottom: '15px' }}>
            Token JWT enmascarado y almacenado correctamente en LocalStorage.
          </p>
        </div>
      )}
    </div>
  );
}