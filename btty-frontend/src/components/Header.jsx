import React from 'react';
import { styles } from '../styles/themeStyles';

export default function Header({ token, onLogout }) {
  return (
    <header style={styles.header}>
      <div>
        <h1 style={styles.welcomeText}>Welcome back, Btty System</h1>
        <p style={styles.subWelcome}>Gestión de accesos, auditoría de seguridad y control RBAC en tiempo real.</p>
      </div>
      {token && (
        <button onClick={onLogout} style={styles.logoutBtn}>
          Cerrar Sesión ➔
        </button>
      )}
    </header>
  );
}