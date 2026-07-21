import React, { useState } from 'react';
import { styles } from '../styles/themeStyles';

export default function ProfileCard({ token, onUpdateProfile }) {
  const [roleId, setRoleId] = useState('');

  const handleSave = () => {
    const parsedRole = parseInt(roleId, 10);
    
    // Validación previa para asegurar que sea un rol válido (1, 2 o 3)
    if (!isNaN(parsedRole) && parsedRole > 0) {
      onUpdateProfile(parsedRole);
      setRoleId(''); // Limpia el input tras guardar
    }
  };

  return (
    <div style={{ ...styles.card, backgroundColor: 'var(--card-blue, #e3f2fd)' }}>
      <div style={styles.cardHeader}>
        <h3 style={styles.cardTitle}>✏️ Modificar Perfil</h3>
        <div style={{ ...styles.badgeDecoration, backgroundColor: 'var(--accent-blue)' }}>★</div>
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
          min="1"
          max="3"
        />
      </div>
      <button 
        onClick={handleSave} 
        disabled={!token || !roleId}
        style={{ ...styles.primaryBtn, backgroundColor: 'var(--accent-blue)' }}
      >
        Guardar y Registrar Log
      </button>
    </div>
  );
}