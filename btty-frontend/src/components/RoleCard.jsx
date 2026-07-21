import React from 'react';
import { styles } from '../styles/themeStyles';

export default function RoleCard({ token, onTestRole }) {
  return (
    <div style={{ ...styles.card, backgroundColor: '#ffe3ec' }}>
      <div style={styles.cardHeader}>
        <h3 style={styles.cardTitle}>👥 Control de Roles (RBAC)</h3>
        <div style={{ ...styles.badgeDecoration, backgroundColor: '#ff77a8' }}>♥</div>
      </div>
      <p style={styles.cardDesc}>Prueba el acceso a rutas según tu nivel de permisos:</p>
      
      <div style={styles.buttonStack}>
        <button 
          onClick={() => onTestRole('patient-dashboard')} 
          style={{ ...styles.roleBtn, backgroundColor: '#e2f0d9' }}
          disabled={!token}
        >
          🟢 Portal Paciente (Roles 1, 2, 3)
        </button>
        <button 
          onClick={() => onTestRole('psychologist-dashboard')} 
          style={{ ...styles.roleBtn, backgroundColor: '#fff2cc' }}
          disabled={!token}
        >
          🟡 Panel Clínico (Roles 1, 2)
        </button>
        <button 
          onClick={() => onTestRole('admin-dashboard')} 
          style={{ ...styles.roleBtn, backgroundColor: '#fce4d6' }}
          disabled={!token}
        >
          🔴 Panel Admin (Exclusivo Rol 1)
        </button>
      </div>
    </div>
  );
}