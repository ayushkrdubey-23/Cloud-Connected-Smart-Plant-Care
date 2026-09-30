import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [device, setDevice] = useState(null);
  const [latestReading, setLatestReading] = useState(null);
  const [sensorHistory, setSensorHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [wateringHistory, setWateringHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connectionError, setConnectionError] = useState(false);

  const [watering, setWatering] = useState(false);
  const [refilling, setRefilling] = useState(false);
  const [wateringMessage, setWateringMessage] = useState("");

  const [settingsOpen, setSettingsOpen] = useState(false);
  const [savingSettings, setSavingSettings] = useState(false);
  const [settingsMessage, setSettingsMessage] = useState("");

  const [settings, setSettings] = useState({
    plant_name: "",
    plant_type: "TOMATO",
    location: "Indoor",
    moisture_threshold: 40,
    auto_water: true,
  });

  const deviceId = "PLANT-001";

  const fetchDashboardData = async () => {
    try {
      setConnectionError(false);

      const [
        deviceResponse,
        readingResponse,
        historyResponse,
        alertResponse,
        wateringResponse,
      ] = await Promise.all([
        axios.get(`${API_URL}/api/devices/${deviceId}`),
        axios.get(`${API_URL}/api/sensors/${deviceId}/latest`),
        axios.get(
          `${API_URL}/api/sensors/${deviceId}/history?limit=20`
        ),
        axios.get(`${API_URL}/api/alerts/${deviceId}`),
        axios.get(
          `${API_URL}/api/watering/${deviceId}/history`
        ),
      ]);

      const deviceData = deviceResponse.data;

      setDevice(deviceData);
      setLatestReading(readingResponse.data);

      const history = historyResponse.data.history || [];

      const chartData = [...history]
        .reverse()
        .map((item) => ({
          time: new Date(item.timestamp).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
          }),
          moisture: Number(item.soil_moisture),
          temperature: Number(item.temperature),
          humidity: Number(item.humidity),
        }));

      setSensorHistory(chartData);

      setAlerts(alertResponse.data.alerts || []);

      setWateringHistory(
        wateringResponse.data.history || []
      );

      if (!settingsOpen) {
        setSettings({
          plant_name: deviceData.plant_name || "",
          plant_type: deviceData.plant_type || "INDOOR_PLANT",
          location: deviceData.location || "Indoor",
          moisture_threshold:
            deviceData.moisture_threshold ?? 30,
          auto_water: Boolean(deviceData.auto_water),
        });
      }
    } catch (error) {
      console.error("Dashboard API error:", error);
      setConnectionError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();

    const interval = setInterval(
      fetchDashboardData,
      5000
    );

    return () => clearInterval(interval);
  }, [settingsOpen]);

  const openSettings = () => {
    if (device) {
      setSettings({
        plant_name: device.plant_name || "",
        plant_type: device.plant_type || "INDOOR_PLANT",
        location: device.location || "Indoor",
        moisture_threshold:
          device.moisture_threshold ?? 30,
        auto_water: Boolean(device.auto_water),
      });
    }

    setSettingsMessage("");
    setSettingsOpen(true);
  };

  const closeSettings = () => {
    if (!savingSettings) {
      setSettingsOpen(false);
      setSettingsMessage("");
    }
  };

  const handleSettingsChange = (event) => {
    const { name, value, type, checked } = event.target;

    setSettings((previous) => ({
      ...previous,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSaveSettings = async (event) => {
    event.preventDefault();

    try {
      setSavingSettings(true);
      setSettingsMessage("");

      const payload = {
        plant_name: settings.plant_name.trim(),
        plant_type: settings.plant_type,
        location: settings.location.trim(),
        moisture_threshold: Number(
          settings.moisture_threshold
        ),
        auto_water: settings.auto_water,
      };

      if (!payload.plant_name) {
        setSettingsMessage(
          "⚠️ Plant name cannot be empty."
        );
        return;
      }

      if (!payload.location) {
        setSettingsMessage(
          "⚠️ Location cannot be empty."
        );
        return;
      }

      if (
        Number.isNaN(payload.moisture_threshold) ||
        payload.moisture_threshold < 0 ||
        payload.moisture_threshold > 100
      ) {
        setSettingsMessage(
          "⚠️ Moisture threshold must be between 0 and 100."
        );
        return;
      }

      const response = await axios.put(
        `${API_URL}/api/devices/${deviceId}`,
        payload
      );

      if (response.data.message) {
        setSettingsMessage(
          "✅ Device settings updated successfully."
        );
      }

      await fetchDashboardData();

      setTimeout(() => {
        setSettingsOpen(false);
        setSettingsMessage("");
      }, 1200);
    } catch (error) {
      console.error("Device settings error:", error);

      const message =
        error.response?.data?.detail ||
        "Unable to update device settings.";

      setSettingsMessage(`⚠️ ${message}`);
    } finally {
      setSavingSettings(false);
    }
  };

  const handleManualWatering = async () => {
    if (watering || device?.pump_status) {
      return;
    }

    try {
      setWatering(true);
      setWateringMessage("");

      const response = await axios.post(
        `${API_URL}/api/watering/${deviceId}/manual`
      );

      if (response.data.success) {
        setWateringMessage(
          "💧 Manual watering started successfully."
        );

        await fetchDashboardData();
      }
    } catch (error) {
      console.error("Manual watering error:", error);

      const message =
        error.response?.data?.detail ||
        "Unable to start manual watering.";

      setWateringMessage(`⚠️ ${message}`);
    } finally {
      setWatering(false);

      setTimeout(() => {
        setWateringMessage("");
      }, 4000);
    }
  };

  const handleRefillTank = async () => {
    if (refilling || device?.pump_status) {
      return;
    }

    try {
      setRefilling(true);
      setWateringMessage("");

      const response = await axios.post(
        `${API_URL}/api/watering/${deviceId}/refill`
      );

      if (response.data.success) {
        setWateringMessage(
          "🚰 Water tank refilled successfully to 100%."
        );

        await fetchDashboardData();
      }
    } catch (error) {
      console.error("Water tank refill error:", error);

      const message =
        error.response?.data?.detail ||
        "Unable to refill the water tank.";

      setWateringMessage(`⚠️ ${message}`);
    } finally {
      setRefilling(false);

      setTimeout(() => {
        setWateringMessage("");
      }, 4000);
    }
  };

  const getPlantHealth = () => {
    if (!latestReading || !device) {
      return {
        text: "Waiting for data",
        className: "health-neutral",
      };
    }

    const moisture = latestReading.soil_moisture;
    const threshold = device.moisture_threshold;

    if (moisture < threshold - 15) {
      return {
        text: "Needs Water",
        className: "health-danger",
      };
    }

    if (moisture < threshold) {
      return {
        text: "Needs Attention",
        className: "health-warning",
      };
    }

    return {
      text: "Healthy",
      className: "health-good",
    };
  };

  const getTankStatus = () => {
    const tankLevel = Number(
      device?.water_tank_level
    );

    if (!device || Number.isNaN(tankLevel)) {
      return {
        text: "Waiting for data",
        className: "tank-neutral",
      };
    }

    if (tankLevel <= 10) {
      return {
        text: "Critical",
        className: "tank-critical",
      };
    }

    if (tankLevel <= 30) {
      return {
        text: "Low",
        className: "tank-warning",
      };
    }

    return {
      text: "Healthy",
      className: "tank-good",
    };
  };

  const plantHealth = getPlantHealth();
  const tankStatus = getTankStatus();

  const tankLevel =
    device?.water_tank_level !== undefined &&
    device?.water_tank_level !== null
      ? Number(device.water_tank_level)
      : null;

  const displayedTankLevel =
    tankLevel !== null && !Number.isNaN(tankLevel)
      ? tankLevel.toFixed(1)
      : "--";

  if (loading) {
    return (
      <div className="app loading-screen">
        <div className="loading-card">
          <div className="loading-icon">🌱</div>

          <h2>Loading Smart Plant Care...</h2>

          <p>
            Connecting to the plant monitoring system.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">🌱</div>

          <div>
            <h1>Smart Plant Care</h1>
            <p>Cloud-Connected IoT Monitoring</p>
          </div>
        </div>

        <div className="navbar-actions">
          <button
            className="settings-button"
            onClick={openSettings}
          >
            ⚙️ Settings
          </button>

          <div
            className={`connection-status ${
              connectionError ? "offline" : "online"
            }`}
          >
            <span className="status-dot"></span>

            {connectionError
              ? "Backend Offline"
              : "System Online"}
          </div>
        </div>
      </header>

      <main className="dashboard">
        <section className="welcome-section">
          <div>
            <p className="eyebrow">
              PLANT MONITORING DASHBOARD
            </p>

            <h2>
              Hello! Your plant is being monitored.
            </h2>

            <p className="welcome-text">
              Real-time sensor data and automatic watering
              status for your smart plant.
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={fetchDashboardData}
          >
            ↻ Refresh
          </button>
        </section>

        {connectionError && (
          <div className="error-banner">
            ⚠️ Unable to connect to the FastAPI backend.
            Make sure the backend server is running.
          </div>
        )}

        {wateringMessage && (
          <div className="watering-message">
            {wateringMessage}
          </div>
        )}

        <section className="plant-card">
          <div className="plant-info">
            <div className="plant-avatar">🪴</div>

            <div>
              <p className="card-label">
                CURRENT PLANT
              </p>

              <h3>
                {device?.plant_name || "Tomato Plant"}
              </h3>

              <p>
                {device?.plant_type || "TOMATO"} ·{" "}
                {device?.location || "Indoor"}
              </p>
            </div>
          </div>

          <div className="plant-status-area">
            <div className="health-status">
              <span className="card-label">
                PLANT STATUS
              </span>

              <strong className={plantHealth.className}>
                {plantHealth.text}
              </strong>
            </div>

            <div className="pump-status">
              <span className="card-label">
                VIRTUAL PUMP
              </span>

              <strong
                className={
                  device?.pump_status
                    ? "pump-on"
                    : "pump-off"
                }
              >
                {device?.pump_status
                  ? "● ON"
                  : "● OFF"}
              </strong>
            </div>

            <button
              className="water-button"
              onClick={handleManualWatering}
              disabled={
                watering ||
                refilling ||
                device?.pump_status ||
                tankLevel === null ||
                tankLevel <= 10
              }
            >
              {watering
                ? "Starting..."
                : device?.pump_status
                ? "Pump Running"
                : tankLevel !== null && tankLevel <= 10
                ? "Tank Empty"
                : "💧 Water Plant"}
            </button>
          </div>
        </section>

        <section className="metrics-grid">
          <MetricCard
            icon="💧"
            label="Soil Moisture"
            value={
              latestReading
                ? `${latestReading.soil_moisture.toFixed(
                    1
                  )}%`
                : "--"
            }
            description={`Target: ${
              device?.moisture_threshold ?? "--"
            }%`}
          />

          <MetricCard
            icon="🌡️"
            label="Temperature"
            value={
              latestReading
                ? `${latestReading.temperature.toFixed(
                    1
                  )}°C`
                : "--"
            }
            description="Current temperature"
          />

          <MetricCard
            icon="💦"
            label="Humidity"
            value={
              latestReading
                ? `${latestReading.humidity.toFixed(
                    1
                  )}%`
                : "--"
            }
            description="Air humidity"
          />

          <MetricCard
            icon="☀️"
            label="Light Level"
            value={
              latestReading
                ? `${latestReading.light_level.toFixed(
                    1
                  )}%`
                : "--"
            }
            description="Current light"
          />
        </section>

        <section className="tank-panel">
          <div className="tank-header">
            <div>
              <p className="card-label">
                WATER RESERVOIR
              </p>

              <h3>Virtual Water Tank</h3>
            </div>

            <div
              className={`tank-status ${tankStatus.className}`}
            >
              {tankStatus.text}
            </div>
          </div>

          <div className="tank-content">
            <div className="tank-visual">
              <div className="tank-outline">
                <div
                  className={`tank-fill ${tankStatus.className}`}
                  style={{
                    height: `${Math.max(
                      0,
                      Math.min(100, tankLevel ?? 0)
                    )}%`,
                  }}
                ></div>
              </div>

              <span className="tank-percent">
                {displayedTankLevel}%
              </span>
            </div>

            <div className="tank-details">
              <strong>{displayedTankLevel}%</strong>

              <span>
                Remaining water level
              </span>

              <div className="tank-progress">
                <div
                  className={`tank-progress-fill ${tankStatus.className}`}
                  style={{
                    width: `${Math.max(
                      0,
                      Math.min(100, tankLevel ?? 0)
                    )}%`,
                  }}
                ></div>
              </div>

              <p>
                {tankLevel !== null && tankLevel <= 10
                  ? "⚠️ Refill required before watering."
                  : tankLevel !== null &&
                    tankLevel <= 30
                  ? "⚠️ Water tank is getting low."
                  : "✓ Sufficient water available."}
              </p>

              <button
                className="refill-button"
                onClick={handleRefillTank}
                disabled={
                  refilling ||
                  watering ||
                  device?.pump_status
                }
              >
                {refilling
                  ? "Refilling..."
                  : "🚰 Refill Water Tank"}
              </button>
            </div>
          </div>
        </section>

        <section className="panel chart-panel">
          <div className="panel-header">
            <div>
              <p className="card-label">
                LIVE SENSOR HISTORY
              </p>

              <h3>Soil Moisture Trend</h3>
            </div>

            <span className="live-badge">
              ● LIVE
            </span>
          </div>

          {sensorHistory.length < 2 ? (
            <div className="empty-state chart-empty">
              <span>📈</span>

              <p>
                Waiting for more sensor readings...
              </p>
            </div>
          ) : (
            <div className="chart-container">
              <ResponsiveContainer
                width="100%"
                height={300}
              >
                <LineChart data={sensorHistory}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#dfe8e1"
                  />

                  <XAxis
                    dataKey="time"
                    tick={{
                      fontSize: 11,
                      fill: "#718078",
                    }}
                  />

                  <YAxis
                    domain={[0, 100]}
                    tick={{
                      fontSize: 11,
                      fill: "#718078",
                    }}
                    tickFormatter={(value) =>
                      `${value}%`
                    }
                  />

                  <Tooltip
                    formatter={(value) => [
                      `${Number(value).toFixed(1)}%`,
                      "Moisture",
                    ]}
                  />

                  <Line
                    type="monotone"
                    dataKey="moisture"
                    stroke="#28784b"
                    strokeWidth={3}
                    dot={{ r: 3 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <div>
                <p className="card-label">
                  WATERING ACTIVITY
                </p>

                <h3>Recent Watering Events</h3>
              </div>

              <span className="count-badge">
                {wateringHistory.length}
              </span>
            </div>

            {wateringHistory.length === 0 ? (
              <div className="empty-state">
                <span>💧</span>

                <p>No watering events yet.</p>
              </div>
            ) : (
              <div className="history-list">
                {wateringHistory
                  .slice(0, 5)
                  .map((event) => (
                    <div
                      className="history-item"
                      key={event.id}
                    >
                      <div className="history-icon">
                        💦
                      </div>

                      <div className="history-details">
                        <strong>
                          {event.trigger_type} watering
                        </strong>

                        <span>
                          {event.moisture_before}% →{" "}
                          {event.moisture_after}%
                        </span>
                      </div>

                      <div className="history-duration">
                        {event.duration}s
                      </div>
                    </div>
                  ))}
              </div>
            )}
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <p className="card-label">
                  ALERT CENTER
                </p>

                <h3>Recent Alerts</h3>
              </div>

              <span className="count-badge">
                {alerts.length}
              </span>
            </div>

            {alerts.length === 0 ? (
              <div className="empty-state">
                <span>✅</span>

                <p>No active alerts.</p>
              </div>
            ) : (
              <div className="alert-list">
                {alerts.slice(0, 5).map((alert) => (
                  <div
                    className={`alert-item ${alert.level.toLowerCase()}`}
                    key={alert.id}
                  >
                    <div className="alert-icon">
                      ⚠️
                    </div>

                    <div>
                      <strong>
                        {alert.alert_type.replace(
                          /_/g,
                          " "
                        )}
                      </strong>

                      <p>{alert.message}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        <section className="settings-panel">
          <div className="settings-header">
            <div>
              <p className="card-label">
                DEVICE CONFIGURATION
              </p>

              <h3>Remote Plant Settings</h3>

              <p>
                Update plant and automatic watering
                configuration remotely.
              </p>
            </div>

            <button
              className="settings-open-button"
              onClick={openSettings}
            >
              ⚙️ Open Settings
            </button>
          </div>

          <div className="settings-summary">
            <div>
              <span>Plant Name</span>
              <strong>
                {device?.plant_name || "--"}
              </strong>
            </div>

            <div>
              <span>Plant Type</span>
              <strong>
                {device?.plant_type || "--"}
              </strong>
            </div>

            <div>
              <span>Location</span>
              <strong>
                {device?.location || "--"}
              </strong>
            </div>

            <div>
              <span>Moisture Target</span>
              <strong>
                {device?.moisture_threshold ?? "--"}%
              </strong>
            </div>

            <div>
              <span>Auto Watering</span>
              <strong
                className={
                  device?.auto_water
                    ? "setting-enabled"
                    : "setting-disabled"
                }
              >
                {device?.auto_water
                  ? "Enabled"
                  : "Disabled"}
              </strong>
            </div>
          </div>
        </section>

        <section className="system-info">
          <div>
            <span>Device ID</span>

            <strong>
              {device?.device_id || "--"}
            </strong>
          </div>

          <div>
            <span>Automatic Watering</span>

            <strong>
              {device?.auto_water
                ? "Enabled"
                : "Disabled"}
            </strong>
          </div>

          <div>
            <span>Water Tank</span>

            <strong>
              {displayedTankLevel}%
            </strong>
          </div>

          <div>
            <span>Last Sensor Update</span>

            <strong>
              {latestReading?.timestamp
                ? new Date(
                    latestReading.timestamp
                  ).toLocaleTimeString()
                : "--"}
            </strong>
          </div>
        </section>
      </main>

      <footer>
        <p>
          Cloud-Connected Smart Plant Care · IoT +
          FastAPI + React
        </p>
      </footer>

      {settingsOpen && (
        <div
          className="settings-overlay"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeSettings();
            }
          }}
        >
          <div className="settings-modal">
            <div className="settings-modal-header">
              <div>
                <p className="card-label">
                  DEVICE SETTINGS
                </p>

                <h3>Configure Your Plant</h3>

                <p>
                  These settings are saved to the
                  FastAPI backend.
                </p>
              </div>

              <button
                className="modal-close"
                onClick={closeSettings}
                disabled={savingSettings}
              >
                ×
              </button>
            </div>

            <form
              className="settings-form"
              onSubmit={handleSaveSettings}
            >
              <div className="form-group">
                <label htmlFor="plant_name">
                  Plant Name
                </label>

                <input
                  id="plant_name"
                  name="plant_name"
                  type="text"
                  value={settings.plant_name}
                  onChange={handleSettingsChange}
                  placeholder="Example: Tomato Plant"
                  maxLength={100}
                />
              </div>

              <div className="form-group">
                <label htmlFor="plant_type">
                  Plant Type
                </label>

                <select
                  id="plant_type"
                  name="plant_type"
                  value={settings.plant_type}
                  onChange={handleSettingsChange}
                >
                  <option value="SUCCULENT">
                    Succulent
                  </option>

                  <option value="TOMATO">
                    Tomato
                  </option>

                  <option value="HERB">
                    Herb
                  </option>

                  <option value="INDOOR_PLANT">
                    Indoor Plant
                  </option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="location">
                  Location
                </label>

                <input
                  id="location"
                  name="location"
                  type="text"
                  value={settings.location}
                  onChange={handleSettingsChange}
                  placeholder="Example: Indoor"
                  maxLength={100}
                />
              </div>

              <div className="form-group">
                <label htmlFor="moisture_threshold">
                  Soil Moisture Threshold
                </label>

                <div className="threshold-input">
                  <input
                    id="moisture_threshold"
                    name="moisture_threshold"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={settings.moisture_threshold}
                    onChange={handleSettingsChange}
                  />

                  <span>%</span>
                </div>

                <small>
                  Automatic watering starts when soil
                  moisture goes below this level.
                </small>
              </div>

              <label className="auto-water-toggle">
                <input
                  type="checkbox"
                  name="auto_water"
                  checked={settings.auto_water}
                  onChange={handleSettingsChange}
                />

                <span className="toggle-track">
                  <span className="toggle-thumb"></span>
                </span>

                <span className="toggle-content">
                  <strong>
                    Automatic Watering
                  </strong>

                  <small>
                    Allow the system to automatically
                    water the plant.
                  </small>
                </span>
              </label>

              {settingsMessage && (
                <div className="settings-message">
                  {settingsMessage}
                </div>
              )}

              <div className="settings-actions">
                <button
                  type="button"
                  className="cancel-button"
                  onClick={closeSettings}
                  disabled={savingSettings}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="save-settings-button"
                  disabled={savingSettings}
                >
                  {savingSettings
                    ? "Saving..."
                    : "💾 Save Settings"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

function MetricCard({
  icon,
  label,
  value,
  description,
}) {
  return (
    <div className="metric-card">
      <div className="metric-icon">{icon}</div>

      <div className="metric-content">
        <span>{label}</span>

        <strong>{value}</strong>

        <small>{description}</small>
      </div>
    </div>
  );
}

export default App;