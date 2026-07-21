import React, { useState } from 'react';
import { styles } from '../styles/themeStyles';

export default function ProfileCard({ token, onUpdateProfile }) {
  const [roleId, setRoleId] = useState('');

  const handleSave = () => {
    onUpdateProfile(roleId);
  };

  return (
    <div style={{ ...styles.card, backgroundColor: '#e3f2fd' }}>
      <div style={styles.cardHeader}>
        <h3 style={styles.cardTitle}>✏️ Modificar Perfil</h3>
        <div style={{ ...styles.badgeDecoration, backgroundColor: '#64b5f6' }}>★</div>
      </div>
      <p style={styles.cardDesc}>Cambia el Role ID para registrar el evento en `audit_logs`:</p>
      
      <div style={styles.inputGroup}>
        <input 
          type="number" 
          placeholder="Nuevo Role ID (1, 2 o 3)" 
          value={roleId} 
          onChange={(e) => setRoleId(e.target.value)} 
          disabled={!token}
          style={styles.input}
        />
      </div>
      <button 
        onClick={handleSave} 
        disabled={!token || !roleId}
        style={{ ...styles.primaryBtn, backgroundColor: '#1e88e5' }}
      >
        Guardar y Registrar Log
      </button>
    </div>
  );
}