const express = require('express');
const cors = require('cors');

const authRoutes = require('./routes/Auth');
const reservationRoutes = require('./routes/Reservations'); 

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/reservations', reservationRoutes); 

app.get('/', (req, res) => {
  res.send('Server is running!');
});

module.exports = app;
