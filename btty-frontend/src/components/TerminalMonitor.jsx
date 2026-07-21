import React from 'react';
import { styles } from '../styles/themeStyles';

export default function TerminalMonitor({ responseLog }) {
  return (
    <div style={styles.terminalCard}>
      <div style={styles.terminalHeader}>
        <span style={styles.terminalTitle}>📡 Monitor de Respuestas HTTP & Logs Activos</span>
        <div style={{ display: 'flex', gap: '6px' }}>
          <div style={styles.dotRed}></div>
          <div style={styles.dotYellow}></div>
          <div style={styles.dotGreen}></div>
        </div>
      </div>
      
      {responseLog ? (
        <div>
          <div style={{ color: '#ff77a8', fontWeight: '700', fontSize: '13px', marginBottom: '8px' }}>
            {responseLog.status}
          </div>
          <pre style={styles.jsonCode}>{JSON.stringify(responseLog.data, null, 2)}</pre>
        </div>
      ) : (
        <p style={{ color: '#888', fontSize: '13px', margin: 0 }}>
          Esperando interacción... Realiza una acción arriba para ver la respuesta del servidor FastAPI.
        </p>
      )}
    </div>
  );
}