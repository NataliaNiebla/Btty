export const styles = {
  appContainer: {
    minHeight: '100vh',          
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    boxSizing: 'border-box'
  },

  windowFrame: {
    backgroundColor: 'var(--beige-general)',
    width: '100%',
    height: '100vh', // 
    maxWidth: '100%',          
    minHeight: 'calc(100vh - 32px)',   
    display: 'flex',
    overflow: 'hidden',
  },

  sidebar: {
    backgroundColor: 'var(--brown-dark)',
    color: 'var(--text-tertiary)',
    width: '240px',
    padding: '30px 20px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    flexShrink: 0,
    borderRadius: '0 24px 24px 0',
    boxShadow: 'var(--shadow-dark)'
  },

  logo: {
    fontSize: 'var(--text-large)',
    fontWeight: 'var(--text-weight-bold)',
    letterSpacing: '-1px',
    margin: '2rem 0 3rem 0',
    textAlign: 'center'
  },

  navMenu: { display: 'flex', flexDirection: 'column', gap: '.8rem' },
  navItem: {
    padding: '12px 16px',
    borderRadius: '16px',
    fontSize: '14px',
    fontWeight: 'var(--text-weight-regular)',
    color: 'var(--text-secondary)',
    cursor: 'pointer'
  },

  navActive: { backgroundColor: 'var(--brown-light)', color: 'var(--text-tertiary)', fontWeight: 'var(--text-weight-medium)' },
  mainContent: {
    flex: 1,
    padding: '2rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '1.25rem',
    overflowY: 'auto'
  },

  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  welcomeText: { fontSize: 'var(--text-large)', fontWeight: 'var(--text-weight-bold)', color: 'var(--text-primary)', margin: 0 },
  subWelcome: { fontSize: 'var(--text-small)', color: 'var(--text-secondary)', margin: '0.25rem 0 0 0' },
  logoutBtn: {
    backgroundColor: 'var(--brown-dark)',
    color: 'var(--text-tertiary)',
    border: 'none',
    padding: 'var(--padding-medium) var(--padding-large)',
    borderRadius: 'var(--border-radius-small)',
    fontSize: 'var(--text-small)',
    fontWeight: 'var(--text-weight-regular)',
    cursor: 'pointer'
  },
  
  gridContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '1.5rem',
  },

  card: {
    borderRadius: 'var(--border-radius-regular)',
    padding: 'var(--padding-large)',
    border: 'var(--border-mix)',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    boxShadow: 'var(--shadow-light)'
  },

  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' },
  cardTitle: { fontSize: 'var(--text-medium)', fontWeight: 'var(--text-weight-regular)', color: 'var(--text-primary)', margin: 0 },
  badgeDecoration: {
    width: '28px',
    height: '28px',
    backgroundColor: 'var(--accent-yellow)',
    color: 'var(--bg-general)',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '12px' 
  },

  cardDesc: { fontSize: 'var(--text-small)', color: 'var(--text-secondary)', lineHeight: '1.4' },
  form: { display: 'flex', flexDirection: 'column', gap: '12px' },
  inputGroup: { display: 'flex', flexDirection: 'column', gap: '6px' },
  label: { fontSize: 'var(--text-small)', fontWeight: 'var(--text-weight-regular)', color: 'var(--text-primary)' },
  input: {
    padding: 'var(--padding-medium)',
    borderRadius: 'var(--border-radius-small)',
    border: 'var(--border-mix)',
    backgroundColor: 'var(--bg-general)',
    fontSize: 'var(--text-small)',
    outline: 'none'
  },

  primaryBtn: {
    backgroundColor: 'var(--brown-dark)',
    color: 'var(--text-tertiary)',
    border: 'none',
    padding: 'var(--padding-medium) var(--padding-large)',
    borderRadius: 'var(--border-radius-small)',
    fontWeight: 'var(--text-weight-regular)',
    fontSize: 'var(--text-small)',
    cursor: 'pointer',
    marginTop: 'var(--padding-large)'
  },

  buttonStack: { display: 'flex', flexDirection: 'column', gap: '10px' },
  roleBtn: {
    padding: 'var(--padding-medium) var(--padding-large)',
    borderRadius: 'var(--border-radius-small)',
    border: 'var(--border-mix)',
    fontSize: 'var(--text-small)',
    fontWeight: 'var(--text-weight-regular)',
    color: 'var(--text-primary)',
    cursor: 'pointer',
    textAlign: 'left'
  },
  terminalCard: { backgroundColor: '#1a1a1a', borderRadius: '24px', padding: '20px', color: '#ffffff' },
  terminalHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 'var(--padding-medium)',
    borderBottom: 'var(--border-mix)',
    paddingBottom: 'var(--padding-small)'
  },
  terminalTitle: { fontSize: '13px', fontWeight: '700', color: '#aaa' },
  dotRed: { width: '10px', height: '10px', backgroundColor: '#ff5f56', borderRadius: '50%' },
  dotYellow: { width: '10px', height: '10px', backgroundColor: '#ffbd2e', borderRadius: '50%' },
  dotGreen: { width: '10px', height: '10px', backgroundColor: '#27c93f', borderRadius: '50%' },
  jsonCode: {
    backgroundColor: '#111',
    padding: 'var(--padding-medium)',
    borderRadius: 'var(--border-radius-small)',
    fontSize: 'var(--text-small)',
    color: '#a5d6a7',
    overflowX: 'auto',
    margin: 0,
    fontFamily: 'monospace'
  }
};