const express = require('express');
const router = express.Router();

// TODO: Implement Alexa device discovery
// This will:
// 1. Call Alexa Smart Home API to list all devices
// 2. Filter & normalize device data
// 3. Return categorized device list

router.get('/', (req, res) => {
  res.json({
    devices: [],
    message: 'Alexa device discovery not yet implemented',
    status: 'pending'
  });
});

module.exports = router;
