import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import '../styles/Dashboard.css'

function Dashboard() {
  const [devices, setDevices] = useState([])
  const [groups, setGroups] = useState([])
  const [cameras, setCameras] = useState([])
  const [automations, setAutomations] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('devices')
  const navigate = useNavigate()

  const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('dashboardToken')}`
    }
  })

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [devicesRes, groupsRes, camerasRes, automationsRes] = await Promise.all([
        apiClient.get('/api/devices'),
        apiClient.get('/api/groups'),
        apiClient.get('/api/cameras'),
        apiClient.get('/api/automations')
      ])

      setDevices(devicesRes.data.devices || [])
      setGroups(groupsRes.data.groups || [])
      setCameras(camerasRes.data.cameras || [])
      setAutomations(automationsRes.data.automations || [])
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('dashboardToken')
    navigate('/login')
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>🏠 Smart Home Control</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </header>

      <nav className="dashboard-nav">
        <button 
          className={`nav-btn ${activeTab === 'devices' ? 'active' : ''}`}
          onClick={() => setActiveTab('devices')}
        >
          Devices
        </button>
        <button 
          className={`nav-btn ${activeTab === 'groups' ? 'active' : ''}`}
          onClick={() => setActiveTab('groups')}
        >
          Groups
        </button>
        <button 
          className={`nav-btn ${activeTab === 'cameras' ? 'active' : ''}`}
          onClick={() => setActiveTab('cameras')}
        >
          Cameras
        </button>
        <button 
          className={`nav-btn ${activeTab === 'automations' ? 'active' : ''}`}
          onClick={() => setActiveTab('automations')}
        >
          Automations
        </button>
      </nav>

      <main className="dashboard-content">
        {activeTab === 'devices' && (
          <section className="section">
            <h2>All Devices</h2>
            {devices.length === 0 ? (
              <p className="empty-state">No devices discovered. Set up Alexa integration to get started.</p>
            ) : (
              <div className="devices-grid">
                {devices.map(device => (
                  <div key={device.id} className="device-card">
                    <h3>{device.name}</h3>
                    <p className="device-type">{device.type}</p>
                    <p className="device-status">{device.connected ? '🟢 Online' : '🔴 Offline'}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {activeTab === 'groups' && (
          <section className="section">
            <h2>Device Groups</h2>
            {groups.length === 0 ? (
              <p className="empty-state">No groups created yet.</p>
            ) : (
              <div className="groups-grid">
                {groups.map(group => (
                  <div key={group.id} className="group-card">
                    <h3>{group.name}</h3>
                    <p>{group.devices?.length || 0} devices</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {activeTab === 'cameras' && (
          <section className="section">
            <h2>Live Cameras</h2>
            {cameras.length === 0 ? (
              <p className="empty-state">No cameras available.</p>
            ) : (
              <div className="cameras-grid">
                {cameras.map(camera => (
                  <div key={camera.id} className="camera-card">
                    <h3>{camera.name}</h3>
                    <div className="camera-placeholder">Live Feed</div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}

        {activeTab === 'automations' && (
          <section className="section">
            <h2>Automations</h2>
            {automations.length === 0 ? (
              <p className="empty-state">No automations set up yet.</p>
            ) : (
              <div className="automations-list">
                {automations.map(automation => (
                  <div key={automation.id} className="automation-item">
                    <h3>{automation.name}</h3>
                    <p>{automation.trigger}</p>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default Dashboard
