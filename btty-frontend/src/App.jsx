import React, { useState } from 'react';
import { styles } from './styles/themeStyles';

import Sidebar from './components/Sidebar';
import Header from './components/Header';
import LoginCard from './components/LoginCard';
import RoleCard from './components/RoleCard';
import ProfileCard from './components/ProfileCard';
import TerminalMonitor from './components/TerminalMonitor';

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [responseLog, setResponseLog] = useState(null);

  // Handlers de la API
  const handleLogin = async (email, password) => {
    setResponseLog({ status: '⏳ Procesando...', data: 'Enviando credenciales al servidor...' });
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      });
      const data = await res.json();
      
      if (res.ok) {
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        setResponseLog({ status: `🟢 HTTP ${res.status} OK (Log INFO generado)`, data });
      } else {
        setResponseLog({ status: `🟡 HTTP ${res.status} Error (Log WARNING generado)`, data });
      }
    } catch (err) {
      setResponseLog({ status: '🔴 HTTP 500 / Error Red (Log ERROR generado)', data: err.message });
    }
  };

  const handleTestRole = async (endpoint) => {
    try {
      const res = await fetch(`${API_URL}/auth/${endpoint}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setResponseLog({ 
        status: res.ok ? `🟢 HTTP ${res.status} Acceso Concedido` : `🟡 HTTP ${res.status} Acceso Denegado (RBAC Warning)`, 
        data 
      });
    } catch (err) {
      setResponseLog({ status: '🔴 Error al probar endpoint', data: err.message });
    }
  };

  const handleUpdateProfile = async (roleId) => {
    try {
      const res = await fetch(`${API_URL}/auth/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ role_id: parseInt(roleId) })
      });
      const data = await res.json();
      setResponseLog({ status: `🟢 HTTP ${res.status} Actualización completada (Log Auditoría)`, data });
    } catch (err) {
      setResponseLog({ status: '🔴 Error al actualizar perfil', data: err.message });
    }
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('token');
    setResponseLog({ status: '⚪ Sesión Cerrada', data: { message: 'Token eliminado' } });
  };

  return (
    <div style={styles.appContainer}>
      <div style={styles.windowFrame}>
        <Sidebar />
        <main style={styles.mainContent}>
          <Header token={token} onLogout={handleLogout} />
          
          <div style={styles.gridContainer}>
            <LoginCard token={token} onLogin={handleLogin} />
            <RoleCard token={token} onTestRole={handleTestRole} />
            <ProfileCard token={token} onUpdateProfile={handleUpdateProfile} />
          </div>

          <TerminalMonitor responseLog={responseLog} />
        </main>
      </div>
    </div>
  );
}

export default App;