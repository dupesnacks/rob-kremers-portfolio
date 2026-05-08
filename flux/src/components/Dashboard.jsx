import React, { useState, useEffect } from 'react';
import volvoAPI from '../api/volvoClient';
import '../styles/Dashboard.css';

export default function Dashboard({ onLogout }) {
  const [vehicleData, setVehicleData] = useState({
    details: null,
    fuel: null,
    doors: null,
    statistics: null,
    odometer: null,
    engineStatus: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionLoading, setActionLoading] = useState({});

  // Fetch vehicle data on mount
  useEffect(() => {
    fetchVehicleData();
    // Refresh every 30 seconds
    const interval = setInterval(fetchVehicleData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchVehicleData = async () => {
    try {
      setError(null);
      const [details, fuel, doors, stats, odometer, engine] = await Promise.all([
        volvoAPI.getVehicleDetails(),
        volvoAPI.getFuelStatus(),
        volvoAPI.getDoorStatus(),
        volvoAPI.getStatistics(),
        volvoAPI.getOdometer(),
        volvoAPI.getEngineStatus(),
      ]);

      setVehicleData({
        details: details.data,
        fuel: fuel.data,
        doors: doors.data,
        statistics: stats.data,
        odometer: odometer.data,
        engineStatus: engine.data,
      });
      setLoading(false);
    } catch (err) {
      setError(err.message || 'Failed to fetch vehicle data');
      setLoading(false);
    }
  };

  const handleCommand = async (command, label) => {
    setActionLoading((prev) => ({ ...prev, [command]: true }));
    try {
      const result = await volvoAPI[command]();
      console.log(`${label} command sent:`, result.data);
      // Refresh data after command
      setTimeout(fetchVehicleData, 1000);
    } catch (err) {
      setError(`Failed to ${label}: ${err.message}`);
    } finally {
      setActionLoading((prev) => ({ ...prev, [command]: false }));
    }
  };

  if (loading) {
    return <div className="flux-container loading">Loading vehicle data...</div>;
  }

  const fuelData = vehicleData.fuel?.fuelAmount;
  const statsData = vehicleData.statistics?.data;
  const odometerData = vehicleData.odometer?.odometer;
  const doorsData = vehicleData.doors;
  const engineData = vehicleData.engineStatus?.engineStatus;

  return (
    <div className="flux-container">
      <div className="flux-header">
        <div className="header-top">
          <h1>⚡ Flux</h1>
          <button className="logout-btn" onClick={onLogout}>
            🚪 Sign Out
          </button>
        </div>
        <p className="vin-label">{import.meta.env.VITE_VEHICLE_VIN}</p>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {/* Status Cards */}
      <div className="status-grid">
        {/* Battery / Fuel */}
        <div className="status-card battery-card">
          <h3>🔋 Battery / Fuel</h3>
          <div className="value">
            {fuelData?.value ? `${fuelData.value.toFixed(1)} ${fuelData.unit}` : 'N/A'}
          </div>
          <p className="timestamp">{fuelData?.timestamp}</p>
        </div>

        {/* Range / Distance */}
        <div className="status-card range-card">
          <h3>🗺️ Range</h3>
          <div className="value">
            {statsData?.distanceToEmpty?.value 
              ? `${statsData.distanceToEmpty.value} ${statsData.distanceToEmpty.unit}` 
              : 'N/A'}
          </div>
          <p className="timestamp">{statsData?.distanceToEmpty?.timestamp}</p>
        </div>

        {/* Odometer */}
        <div className="status-card odometer-card">
          <h3>📊 Odometer</h3>
          <div className="value">
            {odometerData?.value ? `${odometerData.value} ${odometerData.unit}` : 'N/A'}
          </div>
          <p className="timestamp">{odometerData?.timestamp}</p>
        </div>

        {/* Engine Status */}
        <div className="status-card engine-card">
          <h3>🚗 Engine</h3>
          <div className="value">{engineData?.value || 'OFF'}</div>
          <p className="timestamp">{engineData?.timestamp}</p>
        </div>

        {/* Lock Status */}
        <div className="status-card lock-card">
          <h3>🔒 Doors</h3>
          <div className="value">
            {doorsData?.centralLock?.value?.toUpperCase() || 'UNKNOWN'}
          </div>
          <p className="timestamp">{doorsData?.centralLock?.timestamp}</p>
        </div>

        {/* Avg Speed */}
        <div className="status-card speed-card">
          <h3>⚙️ Avg Speed</h3>
          <div className="value">
            {statsData?.averageSpeed?.value 
              ? `${statsData.averageSpeed.value} ${statsData.averageSpeed.unit}` 
              : 'N/A'}
          </div>
          <p className="timestamp">{statsData?.averageSpeed?.timestamp}</p>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="controls-section">
        <h2>Quick Controls</h2>
        <div className="control-grid">
          <button
            className="control-btn lock-btn"
            onClick={() => handleCommand('lock', 'Lock')}
            disabled={actionLoading.lock}
          >
            {actionLoading.lock ? '⏳' : '🔒'} Lock
          </button>

          <button
            className="control-btn unlock-btn"
            onClick={() => handleCommand('unlock', 'Unlock')}
            disabled={actionLoading.unlock}
          >
            {actionLoading.unlock ? '⏳' : '🔓'} Unlock
          </button>

          <button
            className="control-btn honk-btn"
            onClick={() => handleCommand('honk', 'Honk')}
            disabled={actionLoading.honk}
          >
            {actionLoading.honk ? '⏳' : '📢'} Honk
          </button>

          <button
            className="control-btn flash-btn"
            onClick={() => handleCommand('flash', 'Flash')}
            disabled={actionLoading.flash}
          >
            {actionLoading.flash ? '⏳' : '💡'} Flash
          </button>

          <button
            className="control-btn honk-flash-btn"
            onClick={() => handleCommand('honkFlash', 'Honk & Flash')}
            disabled={actionLoading.honkFlash}
          >
            {actionLoading.honkFlash ? '⏳' : '🎪'} Honk & Flash
          </button>

          <button
            className="control-btn climate-btn"
            onClick={() => handleCommand('climatizationStart', 'Start Climate')}
            disabled={actionLoading.climatizationStart}
          >
            {actionLoading.climatizationStart ? '⏳' : '❄️'} Climate
          </button>
        </div>
      </div>

      {/* Refresh button */}
      <div className="footer">
        <button className="refresh-btn" onClick={fetchVehicleData}>
          ↻ Refresh Now
        </button>
      </div>
    </div>
  );
}
