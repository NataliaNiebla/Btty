import React from 'react';
import { styles } from '../styles/themeStyles';

export default function Sidebar() {
  return (
    <aside style={styles.sidebar}>
      <div>
        <div style={styles.logo}>btty<span style={{ color: '#ff77a8' }}>.</span></div>
        <nav style={styles.navMenu}>
          <div style={{ ...styles.navItem, ...styles.navActive }}>
            <span>🔒 Autenticación</span>
          </div>
          <div style={styles.navItem}>
            <span>👥 Pacientes</span>
          </div>
          <div style={styles.navItem}>
            <span>📊 Auditoría & Logs</span>
          </div>
          <div style={styles.navItem}>
            <span>⚙️ Configuración</span>
          </div>
        </nav>
      </div>
      <div>
        <p style={{ fontSize: '11px', opacity: 0.6 }}>Btty Clinical Platform v1.0</p>
      </div>
    </aside>
  );
}