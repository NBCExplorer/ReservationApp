const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const Reservation = require('../models/Reservation');
const Listing = require('../models/Listing');
const User = require('../models/User');

router.get('/host', async (req, res) => {
  try {
    const reservations = await Reservation.find();

    const guestEmails = reservations.map(r => r.guest_email);
    const guests = await User.find({ email: { $in: guestEmails } });

    const guestMap = new Map();
    guests.forEach(g => guestMap.set(g.email, g));

    const result = reservations.map(r => ({
      _id: r._id,
      listing_name: r.listing_name,
      guest: guestMap.get(r.guest_email) || { name: "Unknown" },
      arrivalDate: r.arrival_date,
      departureDate: r.leaving_date,
      guest_count: r.guest_count,
      total_cost: r.total_cost,
      status: r.status,
    }));

    res.json(result);
  } catch (err) {
    console.error('Error fetching reservations:', err);
    res.status(500).json({ message: 'Server error' });
  }
});

router.patch('/status/:id', async (req, res) => {
  try {
    const { status } = req.body;
    if (!['confirmed', 'denied'].includes(status)) {
      return res.status(400).json({ message: 'Invalid status value' });
    }

    const result = await Reservation.findByIdAndUpdate(
      req.params.id,
      { status },
      { new: true }
    );

    if (!result) return res.status(404).json({ message: 'Reservation not found' });

    res.json({ message: 'Status updated', reservation: result });
  } catch (err) {
    console.error('Error updating status:', err);
    res.status(500).json({ message: 'Server error' });
  }
});


module.exports = router;