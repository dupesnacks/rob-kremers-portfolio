const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 8002;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Sonos speaker configuration
const SPEAKERS = {
  kitchen: { name: 'Kitchen', ip: '192.168.68.57', port: 1400 },
  office1: { name: 'Office 1', ip: '192.168.68.59', port: 1400 },
  office2: { name: 'Office 2', ip: '192.168.68.61', port: 1400 },
  office3: { name: 'Office 3', ip: '192.168.68.63', port: 1400 }
};

// Sonos UPnP helper
class SonosDevice {
  constructor(config) {
    this.name = config.name;
    this.ip = config.ip;
    this.port = config.port;
    this.baseUrl = `http://${this.ip}:${this.port}`;
  }

  async getDeviceInfo() {
    try {
      const response = await axios.get(`${this.baseUrl}/xml/device_description-1.xml`, {
        timeout: 3000
      });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to connect to ${this.name}: ${error.message}`);
    }
  }

  async sendRequest(service, action, args = {}) {
    try {
      const soapBody = this.buildSoapRequest(service, action, args);
      const response = await axios.post(
        `${this.baseUrl}:${this.port}/upnp/control/${service}1`,
        soapBody,
        {
          headers: {
            'Content-Type': 'text/xml; charset="utf-8"',
            'SOAPACTION': `"urn:schemas-upnp-org:service:${service}:1#${action}"`
          },
          timeout: 5000
        }
      );
      return response.data;
    } catch (error) {
      throw new Error(`${action} failed: ${error.message}`);
    }
  }

  buildSoapRequest(service, action, args) {
    let argsXml = '';
    for (const [key, value] of Object.entries(args)) {
      argsXml += `<${key}>${this.escapeXml(String(value))}</${key}>`;
    }

    return `<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
  <s:Body>
    <u:${action} xmlns:u="urn:schemas-upnp-org:service:${service}:1">
      ${argsXml}
    </u:${action}>
  </s:Body>
</s:Envelope>`;
  }

  escapeXml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
  }

  async play() {
    return await this.sendRequest('AVTransport', 'Play', { InstanceID: 0, Speed: '1' });
  }

  async pause() {
    return await this.sendRequest('AVTransport', 'Pause', { InstanceID: 0 });
  }

  async next() {
    return await this.sendRequest('AVTransport', 'Next', { InstanceID: 0 });
  }

  async previous() {
    return await this.sendRequest('AVTransport', 'Previous', { InstanceID: 0 });
  }

  async setVolume(volume) {
    return await this.sendRequest('RenderingControl', 'SetVolume', {
      InstanceID: 0,
      Channel: 'Master',
      DesiredVolume: Math.min(100, Math.max(0, volume))
    });
  }

  async getVolume() {
    const response = await this.sendRequest('RenderingControl', 'GetVolume', {
      InstanceID: 0,
      Channel: 'Master'
    });
    const match = response.match(/<CurrentVolume>(\d+)<\/CurrentVolume>/);
    return match ? parseInt(match[1]) : 0;
  }

  async setMuted(mute) {
    return await this.sendRequest('RenderingControl', 'SetMute', {
      InstanceID: 0,
      Channel: 'Master',
      DesiredMute: mute ? '1' : '0'
    });
  }

  async getMuted() {
    const response = await this.sendRequest('RenderingControl', 'GetMute', {
      InstanceID: 0,
      Channel: 'Master'
    });
    const match = response.match(/<CurrentMute>(\d+)<\/CurrentMute>/);
    return match ? parseInt(match[1]) === 1 : false;
  }

  async getTransportInfo() {
    const response = await this.sendRequest('AVTransport', 'GetTransportInfo', {
      InstanceID: 0
    });
    const match = response.match(/<CurrentTransportState>([^<]+)<\/CurrentTransportState>/);
    return match ? match[1] : 'UNKNOWN';
  }

  async getPositionInfo() {
    try {
      const response = await this.sendRequest('AVTransport', 'GetPositionInfo', {
        InstanceID: 0
      });
      
      const trackMatch = response.match(/<TrackMetaData>([^<]*)<\/TrackMetaData>/);
      const track = trackMatch ? trackMatch[1] : '';
      
      // Parse DIDL metadata if available
      let trackTitle = 'Unknown';
      if (track && track.includes('upnp:class')) {
        const titleMatch = track.match(/<dc:title>([^<]+)<\/dc:title>/);
        if (titleMatch) trackTitle = titleMatch[1];
      } else if (track) {
        trackTitle = track.substring(0, 100);
      }
      
      return { title: trackTitle, metadata: track };
    } catch (error) {
      return { title: 'Unable to get track info', metadata: '' };
    }
  }
}

// Create speaker instances
const speakers = {};
for (const [key, config] of Object.entries(SPEAKERS)) {
  speakers[key] = new SonosDevice(config);
}

// Get all speaker states
app.get('/api/speakers', async (req, res) => {
  try {
    const states = {};

    for (const [key, device] of Object.entries(speakers)) {
      try {
        const [state, track, volume, mute] = await Promise.all([
          device.getTransportInfo(),
          device.getPositionInfo(),
          device.getVolume(),
          device.getMuted()
        ]);

        states[key] = {
          name: device.name,
          ip: device.ip,
          state: state.toLowerCase(),
          track: track || { title: 'Nothing playing' },
          volume,
          mute,
          playing: state === 'PLAYING'
        };
      } catch (error) {
        console.error(`Error getting state for ${device.name}:`, error.message);
        states[key] = {
          name: device.name,
          ip: device.ip,
          state: 'error',
          error: error.message,
          volume: 0,
          mute: false,
          playing: false
        };
      }
    }

    res.json(states);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get single speaker state
app.get('/api/speaker/:name', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    const [state, track, volume, mute] = await Promise.all([
      device.getTransportInfo(),
      device.getPositionInfo(),
      device.getVolume(),
      device.getMuted()
    ]);

    res.json({
      name: device.name,
      ip: device.ip,
      state: state.toLowerCase(),
      track: track || { title: 'Nothing playing' },
      volume,
      mute,
      playing: state === 'PLAYING'
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Play
app.post('/api/speaker/:name/play', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    await device.play();
    res.json({ success: true, message: `${device.name} is now playing` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Pause
app.post('/api/speaker/:name/pause', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    await device.pause();
    res.json({ success: true, message: `${device.name} is paused` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Next track
app.post('/api/speaker/:name/next', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    await device.next();
    res.json({ success: true, message: `${device.name} skipped to next` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Previous track
app.post('/api/speaker/:name/previous', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    await device.previous();
    res.json({ success: true, message: `${device.name} skipped to previous` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Set volume
app.post('/api/speaker/:name/volume', async (req, res) => {
  try {
    const { name } = req.params;
    const { volume } = req.body;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    if (volume < 0 || volume > 100) {
      return res.status(400).json({ error: 'Volume must be between 0-100' });
    }

    await device.setVolume(volume);
    res.json({ success: true, message: `${device.name} volume set to ${volume}` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Mute
app.post('/api/speaker/:name/mute', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    await device.setMuted(true);
    res.json({ success: true, message: `${device.name} is muted` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Unmute
app.post('/api/speaker/:name/unmute', async (req, res) => {
  try {
    const { name } = req.params;
    const device = speakers[name];

    if (!device) {
      return res.status(404).json({ error: 'Speaker not found' });
    }

    await device.setMuted(false);
    res.json({ success: true, message: `${device.name} is unmuted` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', speakers: Object.keys(speakers) });
});

// Start server
app.listen(PORT, () => {
  console.log(`\n🔊 Sonos Controller running on http://localhost:${PORT}`);
  console.log(`📱 Dashboard: http://localhost:${PORT}`);
  console.log(`🎵 Speakers configured: ${Object.entries(SPEAKERS).map(([,c]) => c.name).join(', ')}\n`);
});
