# Cloud-Connected Smart Plant Care & Watering System 🌱

A beginner-friendly **IoT + Cloud Computing project** that simulates smart plant monitoring, automatic watering, water-tank management, alerts, and a real-time web dashboard.

The project demonstrates how a virtual IoT device can send sensor data to a backend API, store it in a database, process automation rules, and display the results through a React dashboard.

> **Project Author:** Ayush Kumar Dubey  
> **Project Series:** 5 Cloud Computing Projects  
> **Current Project:** Cloud-Connected Smart Plant Care & Watering System

---

## 📌 Project Overview

The **Cloud-Connected Smart Plant Care & Watering System** is a software-based smart agriculture/IoT prototype.

Instead of requiring physical hardware, the project uses a **Python virtual sensor simulator** to generate realistic:

- Soil moisture
- Temperature
- Humidity
- Light intensity

The generated data is sent to a **FastAPI backend** using REST APIs.

The backend:

1. Receives sensor data.
2. Stores readings in SQLite.
3. Checks plant moisture conditions.
4. Runs automatic watering logic.
5. Controls a virtual water pump.
6. Tracks virtual water-tank level.
7. Creates alerts.
8. Provides data to the React dashboard.

The frontend provides a simple monitoring interface where users can observe the plant condition, sensor values, watering history, alerts, and virtual water tank.

---

## 🎯 Objectives

The main objectives of this project are:

- Build an IoT-style plant monitoring system.
- Simulate sensor data without physical hardware.
- Create REST APIs using FastAPI.
- Store IoT data using SQLite and SQLAlchemy.
- Implement automatic watering logic.
- Simulate virtual pump operation.
- Track water consumption.
- Monitor virtual water-tank levels.
- Generate plant and system alerts.
- Create a responsive React dashboard.
- Demonstrate an architecture that can later be connected to real IoT hardware and cloud services.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │ Python Virtual Sensor   │
                    │ Simulator               │
                    │                         │
                    │ Moisture               │
                    │ Temperature            │
                    │ Humidity                │
                    │ Light                  │
                    └────────────┬────────────┘
                                 │
                              HTTP/REST
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ FastAPI Backend         │
                    │                         │
                    │ Sensor APIs              │
                    │ Device APIs              │
                    │ Watering APIs            │
                    │ Alert APIs               │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
        │ SQLite DB    │ │ Watering     │ │ Alert        │
        │              │ │ Engine       │ │ Service      │
        │ Sensors      │ │              │ │              │
        │ Devices      │ │ Pump Logic   │ │ Notifications│
        │ Events       │ │ Tank Logic   │ │ Status       │
        └──────────────┘ └──────────────┘ └──────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │ React + Vite Dashboard  │
                    │                         │
                    │ Live Sensor Data        │
                    │ Moisture Chart           │
                    │ Plant Health             │
                    │ Water Tank               │
                    │ Watering History         │
                    │ Alerts                   │
                    └─────────────────────────┘
```

---

## ✨ Main Features

### 1. Virtual IoT Sensor Simulation

The Python simulator generates changing sensor values such as:

- Soil moisture
- Temperature
- Humidity
- Light level

The simulator sends data to the backend at a configurable interval.

---

### 2. Real-Time Sensor Monitoring

The dashboard displays:

- Soil moisture
- Temperature
- Humidity
- Light level
- Latest sensor update
- Plant health condition

---

### 3. Automatic Watering

The watering engine checks soil moisture against the configured threshold.

Example:

```text
Soil moisture < threshold
        ↓
Check water tank
        ↓
Start virtual pump
        ↓
Monitor watering
        ↓
Moisture reaches target
        ↓
Stop virtual pump
        ↓
Save watering event
```

---

### 4. Manual Watering

Users can manually start watering from the dashboard.

The system checks:

- Whether the device exists.
- Whether the pump is already running.
- Whether sufficient water is available.

---

### 5. Virtual Water Tank

The system maintains a virtual water tank represented as a percentage.

Example:

```text
100% → Full
70%  → Healthy
30%  → Low
10%  → Critical
0%   → Empty
```

Water consumption is calculated from watering duration.

```text
Water Consumed =
Watering Duration × Consumption Rate
```

The current implementation uses a virtual consumption rate of:

```text
1% tank level / second
```

---

### 6. Water Tank Refill

The dashboard provides a refill option.

When the pump is OFF, the virtual tank can be refilled to:

```text
100%
```

The system prevents tank refilling while the virtual pump is running.

---

### 7. Alert System

The backend can generate alerts for conditions such as:

- Low soil moisture
- Critical soil moisture
- High temperature
- Low water tank
- Offline device

Example:

```text
LOW_MOISTURE
HIGH_TEMPERATURE
LOW_WATER_TANK
DEVICE_OFFLINE
```

Alerts have levels such as:

```text
INFO
WARNING
CRITICAL
```

Alerts can also be acknowledged from the API.

---

### 8. Watering History

Every watering operation can be stored with:

- Event ID
- Device ID
- Trigger type
- Moisture before watering
- Moisture after watering
- Duration
- Timestamp

Trigger types include:

```text
AUTO
MANUAL
```

---

### 9. Plant Profiles

The automation system contains predefined plant profiles.

| Plant Type | Moisture Threshold |
|---|---:|
| Succulent | 20% |
| Tomato | 40% |
| Herb | 35% |
| Indoor Plant | 30% |

These values can be extended for additional plant types.

---

## 🛠️ Technologies Used

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- SQLite
- Python-dotenv
- HTTPX

### Frontend

- React
- Vite
- JavaScript
- CSS
- Recharts

### Testing

- Pytest

### Development Tools

- Visual Studio Code
- Git
- GitHub
- FastAPI Swagger UI

---

## 📁 Project Structure

```text
Cloud-Connected-Smart-Plant-Care/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── alert_routes.py
│   │   ├── device_routes.py
│   │   ├── sensor_routes.py
│   │   └── watering_routes.py
│   │
│   └── services/
│       ├── alert_service.py
│       └── watering_service.py
│
├── automation/
│   ├── __init__.py
│   ├── plant_profiles.py
│   └── watering_engine.py
│
├── sensor_simulator/
│   ├── __init__.py
│   ├── config.py
│   └── simulator.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
│
├── tests/
│   └── test_watering_engine.py
│
├── sample_data/
│
├── screenshots/
│
├── docs/
│
├── reports/
│
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Cloud-Connected-Smart-Plant-Care.git
cd Cloud-Connected-Smart-Plant-Care
```

Replace `YOUR_USERNAME` with your GitHub username.

---

### Step 2: Create Python Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell activation is blocked, use:

```powershell
.venv\Scripts\activate.bat
```

---

### Step 3: Install Backend Dependencies

```powershell
python -m pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv httpx pytest
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root.

Example:

```env
API_URL=http://127.0.0.1:8000
DEVICE_ID=PLANT-001
SIMULATOR_INTERVAL=5
OFFLINE_MODE=false
REQUEST_TIMEOUT=5
MAX_RETRIES=3
```

Do not upload `.env` to GitHub.

The repository includes `.env.example` for reference.

---

# ▶️ Running the Project

The project uses three main processes:

1. FastAPI backend
2. React frontend
3. Python sensor simulator

Run them in separate terminals.

---

## 1. Start the Backend

From the project root:

```powershell
python -m uvicorn backend.app:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

---

## 2. Open FastAPI Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the REST APIs.

Health check:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 3. Start the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

The Vite development server normally runs at:

```text
http://localhost:5173
```

---

## 4. Start the Sensor Simulator

Open another terminal from the project root:

```powershell
python -m sensor_simulator.simulator
```

The simulator sends sensor data approximately every 5 seconds according to `.env`.

---

# 🔄 Complete Project Workflow

```text
1. Sensor simulator generates data
             ↓
2. Data sent to FastAPI
             ↓
3. Backend validates sensor values
             ↓
4. Data stored in SQLite
             ↓
5. Watering engine checks moisture
             ↓
6. Virtual pump starts/stops when required
             ↓
7. Water tank level is updated
             ↓
8. Alert service checks abnormal conditions
             ↓
9. React dashboard requests latest data
             ↓
10. User monitors the complete system
```

---

# 🔌 API Overview

Base URL:

```text
http://127.0.0.1:8000
```

## Health

```http
GET /health
```

---

## Sensor APIs

### Send Sensor Data

```http
POST /api/sensors/data
```

Example:

```json
{
  "device_id": "PLANT-001",
  "soil_moisture": 35.4,
  "temperature": 27.5,
  "humidity": 62.0,
  "light_level": 70.0
}
```

### Latest Reading

```http
GET /api/sensors/PLANT-001/latest
```

### Sensor History

```http
GET /api/sensors/PLANT-001/history
```

### Device Sensor Status

```http
GET /api/sensors/PLANT-001/status
```

---

## Device APIs

```http
GET /api/devices
```

```http
POST /api/devices
```

```http
GET /api/devices/{device_id}
```

```http
PUT /api/devices/{device_id}
```

---

## Watering APIs

### Manual Watering

```http
POST /api/watering/{device_id}/manual
```

### Refill Water Tank

```http
POST /api/watering/{device_id}/refill
```

### Watering History

```http
GET /api/watering/{device_id}/history
```

---

## Alert APIs

### Get Alerts

```http
GET /api/alerts/{device_id}
```

### Check Device Offline

```http
POST /api/alerts/{device_id}/check-offline
```

### Acknowledge Alert

```http
PATCH /api/alerts/{alert_id}/acknowledge
```

---

# 🗄️ Database Design

The project uses SQLite with SQLAlchemy.

Main tables:

### Device

Stores plant/device information.

Important fields:

```text
device_id
plant_name
plant_type
location
moisture_threshold
pump_status
auto_water
water_tank_level
last_seen
created_at
```

### SensorReading

Stores sensor measurements.

```text
device_id
soil_moisture
temperature
humidity
light_level
timestamp
```

### WateringEvent

Stores watering operations.

```text
device_id
trigger_type
moisture_before
moisture_after
duration
timestamp
```

### Alert

Stores system alerts.

```text
device_id
alert_type
message
level
status
created_at
```

---

# 🧠 Automatic Watering Logic

The automatic watering engine checks:

### Start Conditions

```text
Automatic watering enabled
        +
Pump currently OFF
        +
Soil moisture below target
        +
Water tank level above minimum
```

Then:

```text
PUMP ON
```

### Stop Conditions

Watering stops when one of the following conditions is reached:

```text
Soil moisture reaches threshold
OR
Maximum watering duration reached
OR
Water tank reaches minimum level
```

Then:

```text
PUMP OFF
```

The watering event is completed and stored in the database.

---

# 🧪 Testing

Run the watering-engine tests:

```powershell
pytest
```

The test suite covers scenarios including:

- Dry soil triggers watering.
- Moist soil does not trigger watering.
- Low water tank prevents watering.
- Pump can be stopped correctly.

The project also includes manual integration testing through:

- Swagger UI
- React dashboard
- Virtual sensor simulator

---

# 📊 Dashboard

The React dashboard provides:

### Live Monitoring

```text
Soil Moisture
Temperature
Humidity
Light Level
```

### Plant Health

Displays the current plant condition based on sensor values.

### Soil Moisture Trend

A chart visualizes recent soil moisture readings.

### Virtual Water Tank

Displays:

- Current tank level
- Tank health
- Tank progress
- Refill control

### Watering History

Displays recent automatic and manual watering events.

### Alert Center

Displays active system alerts.

### System Information

Displays:

- Device ID
- Automatic watering status
- Water tank level
- Last sensor update

---

# 📸 Project Screenshots

Recommended screenshots for project documentation:

```text
screenshots/
├── 01_backend_swagger.png
├── 02_dashboard_overview.png
├── 03_live_sensor_monitoring.png
├── 04_soil_moisture_chart.png
├── 05_plant_health_status.png
├── 06_virtual_water_tank.png
├── 07_manual_watering.png
├── 08_watering_history.png
├── 09_alert_center.png
├── 10_refill_water_tank.png
├── 11_sensor_simulator.png
└── 12_complete_system_running.png
```

These screenshots provide evidence of the major project features.

---

# ☁️ Cloud Computing Relevance

Although the current version runs locally for development and demonstration, its architecture is designed around cloud/IoT principles.

The backend API separates the sensor layer, business logic, database, and frontend.

A future cloud deployment can replace:

```text
Local SQLite
```

with:

```text
PostgreSQL / Firebase / Supabase
```

The local virtual sensor simulator can also later be replaced with:

```text
ESP32 / ESP8266 / Raspberry Pi
```

A future deployment architecture can be:

```text
ESP32 Sensors
      ↓
Internet
      ↓
Cloud API
      ↓
Cloud Database
      ↓
Automation Engine
      ↓
React Web Dashboard
      ↓
User
```

---

# 🔮 Future Scope

Possible future improvements include:

- ESP32 hardware integration
- Real soil moisture sensor
- Real water pump and relay
- Cloud database deployment
- Cloud hosting
- User authentication
- Multiple plant/device support
- Push notifications
- Email alerts
- SMS alerts
- Historical analytics
- Weather API integration
- Plant-specific AI recommendations
- Machine learning for watering prediction
- Advanced water consumption analytics
- Role-based access control
- Production-grade API security
- HTTPS deployment
- Monitoring and logging

These are future enhancements and are not represented as implemented features of the current MVP.

---

# 🔒 Security Notes

For this educational project:

- Environment variables are kept outside source control.
- `.env` is ignored through `.gitignore`.
- API input validation is implemented with Pydantic.
- Database access is handled through SQLAlchemy.
- CORS is configured for the local frontend.
- Production deployment should use HTTPS and stronger authentication/security controls.

**Never commit API keys, passwords, tokens, or other secrets to GitHub.**

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

- IoT architecture
- REST API development
- FastAPI
- React
- Vite
- SQLAlchemy
- SQLite
- Sensor simulation
- Automation logic
- Alert management
- Database design
- Frontend-backend integration
- API testing
- Git/GitHub workflow
- Cloud-ready system architecture

---

# 🤝 Guidance & Acknowledgement

Special thanks to **Mr. Umesh Yadav, Founder, IIP**, with collaboration with **eDC IIT Delhi**, for providing guidance and industry-oriented learning opportunities during the project development journey.

---

# 👨‍💻 Author

**Ayush Kumar Dubey**

Computer Science Engineering Student

Project series focused on practical **Cloud Computing, IoT, Software Development, Data Science, and AI/ML** applications.

---

# 📄 Documentation

Additional project documentation is available in the `docs/` folder:

```text
docs/
├── PROJECT_OVERVIEW.md
├── ARCHITECTURE.md
├── API_DOCUMENTATION.md
├── DATABASE_DESIGN.md
├── WATERING_LOGIC.md
├── ALERT_SYSTEM.md
├── TESTING.md
├── SETUP_AND_RUN.md
├── SCREENSHOTS.md
├── FUTURE_SCOPE.md
├── SECURITY.md
├── PROJECT_WORKFLOW.md
├── SUBMISSION_CHECKLIST.md
└── PROJECT_REPORT_SUMMARY.md
```

---

# ⭐ Project Status

```text
Status: MVP Completed
Backend: Completed
Frontend: Completed
Sensor Simulator: Completed
Automatic Watering: Completed
Virtual Water Tank: Completed
Alert System: Completed
Watering History: Completed
Testing: Completed
Documentation: Completed
```

---

## 📌 Final Note

This project is an educational MVP designed to demonstrate the complete flow of a smart IoT application:

```text
Sensing → API → Database → Automation → Alerts → Dashboard
```

It provides a foundation that can later be extended into a real-world cloud-connected smart agriculture and plant-care platform.
