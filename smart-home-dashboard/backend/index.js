const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Auth middleware (basic password check)
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  const dashboardPassword = process.env.DASHBOARD_PASSWORD;
  
  if (!dashboardPassword) {
    console.warn('Warning: DASHBOARD_PASSWORD not set');
    return next();
  }
  
  if (token !== dashboardPassword) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  next();
};

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Devices API
app.get('/api/devices', authMiddleware, require('./routes/devices'));
app.post('/api/devices/:id/control', authMiddleware, require('./routes/control'));

// Automations API
app.get('/api/automations', authMiddleware, require('./routes/automations'));
app.post('/api/automations', authMiddleware, require('./routes/automations'));

// Cameras API
app.get('/api/cameras', authMiddleware, require('./routes/cameras'));
app.get('/api/cameras/:id/stream', authMiddleware, require('./routes/cameras'));

// Groups API
app.get('/api/groups', authMiddleware, require('./routes/groups'));
app.post('/api/groups', authMiddleware, require('./routes/groups'));
app.post('/api/groups/:id/control', authMiddleware, require('./routes/groups'));

// Error handling
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
  console.log(`Smart Home Backend running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
