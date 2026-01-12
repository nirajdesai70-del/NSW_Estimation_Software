import { useEffect, useState } from 'react'
import { apiClient } from '../services/api'

function Home() {
  const [health, setHealth] = useState<string>('Checking...')

  useEffect(() => {
    apiClient
      .get('/health')
      .then((response) => {
        setHealth(JSON.stringify(response.data, null, 2))
      })
      .catch((error) => {
        setHealth(`Error: ${error.message}`)
      })
  }, [])

  return (
    <div>
      <h2>Welcome to NSW Estimation Software</h2>
      <p>New build - React + FastAPI + PostgreSQL</p>
      <div>
        <h3>API Health Check:</h3>
        <pre>{health}</pre>
      </div>
    </div>
  )
}

export default Home

