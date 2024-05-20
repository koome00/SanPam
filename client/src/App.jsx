import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'
function App() {
  const [count, setCount] = useState(0);
  const [array, setArray] = useState([]);
  
  const fetchAPI = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8080/api/users");
      if (!response.ok) {
        throw new Error("Response not OK!");
      }
      const data = await response.json();
      setArray(data.users);
    } catch (err) {
      console.log(err instanceof Error ? err.message : err.toString())
    }
  };
  useEffect(() => {
    fetchAPI();
  }, [])
  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        
          {
            array.map((user, index) => (
              <div key={index}>
              <span >{user}</span>
              <br />
              </div>
            ))
          }
       
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
