const express = require('express')
const path = require('path')
const app = express()
require('dotenv').config();

const cors = require('cors');
app.use(cors());
const port = 3000;
const fs = require('node:fs');
const methodOverride = require('method-override');

const mongoose = require('mongoose');
const Schema = mongoose.Schema;


mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Error connecting to MongoDB:', err));

const locationSchema = new Schema({
  latitude: Number,
  longitude: Number
}, { collection: 'Info'});

const Location = mongoose.model("Location", locationSchema);
app.use(express.json());

app.get('/locations', async (req, res) => {
  try {
    const locations = await Location.find();
    
    console.log('Fetched locations:', locations);
    
    res.json(locations);
  } catch (error) {
    console.error('Error fetching data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});