import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Login.css'

function Login({ setIsAuthenticated }) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      // For now, just store the password as token
      // In production, this would call an auth endpoint
      localStorage.setItem('dashboardToken', password)
      setIsAuthenticated(true)
      navigate('/')
    } catch (err) {
      setError('Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Smart Home Dashboard</h1>
        <p className="subtitle">Myron's Control Center</p>
        
        <form onSubmit={handleLogin}>
          <input
            type="password"
            placeholder="Enter dashboard password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
          />
          
          {error && <p className="error">{error}</p>}
          
          <button type="submit" disabled={loading || !password}>
            {loading ? 'Unlocking...' : 'Unlock Dashboard'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Login
