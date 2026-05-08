const express = require('express');
const router = express.Router();

// TODO: Implement camera feeds
// This will:
// 1. Fetch camera list from Wyze & Nest APIs
// 2. Return stream URLs for live feeds
// 3. Handle camera status & recording

router.get('/', (req, res) => {
  res.json({
    cameras: [],
    message: 'Camera integration not yet implemented'
  });
});

router.get('/:id/stream', (req, res) => {
  const { id } = req.params;
  
  res.json({
    status: 'not_implemented',
    message: 'Camera stream not yet implemented',
    cameraId: id
  });
});

module.exports = router;
