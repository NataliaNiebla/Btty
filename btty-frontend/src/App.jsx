import { useEffect, useState } from 'react'

function App() {
  const [mensaje, setMensaje] = useState("Esperando al backend...")

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/saludo')
      .then(response => response.json())
      .then(data => setMensaje(data.mensaje))
      .catch(error => setMensaje("Error de conexión ❌"))
  }, [])

  return (
    <div style={{ textAlign: 'center', marginTop: '100px', fontFamily: 'Arial' }}>
      <h1>Proyecto Psicóloga 🧠</h1>
      <div style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '10px', display: 'inline-block' }}>
        <p>{mensaje}</p>
      </div>
    </div>
  )
}

export default App