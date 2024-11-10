const express = require('express');
const path = require('path');
const app = express();
require('dotenv').config();

const cors = require('cors');
app.use(cors());
const port = 3000;
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Error connecting to MongoDB:', err));

const locationSchema = new Schema({
  latitude: Number,
  longitude: Number, 
  facility_name: String
}, { collection: 'Info' });

const Location = mongoose.model("Location", locationSchema);
app.use(express.json());

const calculateDistance = (lat1, long1, lat2, long2) => {
  const convertRadians = (inputD) => inputD * (Math.PI / 180);
  lat1 = convertRadians(lat1);
  lat2 = convertRadians(lat2);
  long1 = convertRadians(long1);
  long2 = convertRadians(long2);
  return Math.acos(Math.sin(lat1) * Math.sin(lat2) + Math.cos(lat1) * Math.cos(lat2) * Math.cos(long2 - long1)) * 6371; 
};

app.get('/allLocs', async (req, res) => {
  try {
    const locations = await Location.find();
    const locStorage = [];

    for (let i = 0; i < locations.length; i++) {
      const { latitude, longitude, facility_name } = locations[i];
      if (latitude == null || longitude == null) continue;
      const loc = {
        latitude,
        longitude,
        facility_name
      };
      locStorage.push(loc);
    }
    // console.log(locStorage);
    res.json(locStorage);
  } catch (error) {
    console.error('Error fetching all locations:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/closest', async (req, res) => {
  const latO = 40.748817;
  const longO = -73.985428; 
  try {
    const locations = await Location.find(); 
    const locStorage = [];

    for (let i = 0; i < locations.length; i++) {
      const { latitude, longitude } = locations[i];
      if (latitude == null || longitude == null) continue;
      const dist = calculateDistance(latO, longO, latitude, longitude);
      const loc = {
        latitude,
        longitude,
        distance: dist
      };
      locStorage.push(loc);
    }

    locStorage.sort((a, b) => a.distance - b.distance);
    const closestLocations = locStorage.slice(0, 10);
    res.json(closestLocations);
  } catch (error) {
    console.error('Error fetching nearest locations:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
	console.log('Listening on *:3000')
});
