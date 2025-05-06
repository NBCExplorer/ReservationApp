const express = require('express');
const bcrypt = require('bcryptjs');
const User = require('../models/User'); // Adjust path if needed
const mongoose = require('mongoose');

const router = express.Router();

// Register route
router.post('/register', async (req, res) => {
  const { role, name, email, password, hostId } = req.body;

  try {
    // Check if email is already taken
    const existingEmail = await User.findOne({ email });
    if (existingEmail) {
      return res.status(400).json({ message: 'Email already in use' });
    }

    if (role === 'host') {
      if (!hostId) {
        return res.status(400).json({ message: 'Host ID is required for hosts' });
      }

      // ✅ Check if hostId already in use
      const existingHostId = await User.findOne({ hostId });
      if (existingHostId) {
        return res.status(400).json({ message: 'Host ID already in use' });
      }

      // ✅ Check if hostId exists in listings collection (as host.host_id)
      try {
        const db = mongoose.connection.db;
        const hostExists = await db.collection('listings').findOne({ 'host.host_id': hostId });

        if (!hostExists) {
          return res.status(400).json({ message: 'Host ID not found in listings' });
        }
      } catch (dbErr) {
        console.error('Error accessing listings collection:', dbErr);
        return res.status(500).json({ message: 'Database error while verifying host ID' });
      }
    }

    // Hash password
    const salt = await bcrypt.genSalt(10);
    const passwordHash = await bcrypt.hash(password, salt);

    // Create and save user
    const newUser = new User({
      role,
      name,
      email,
      passwordHash,
      ...(role === 'host' && { hostId })
    });

    await newUser.save();
    res.status(201).json({ message: 'User registered successfully' });

  } catch (err) {
    console.error('Registration error:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Login route remains unchanged
router.post('/login', async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.findOne({ email });
    if (!user) return res.status(400).json({ message: 'Invalid email or password' });

    const isMatch = await bcrypt.compare(password, user.passwordHash);
    if (!isMatch) return res.status(400).json({ message: 'Invalid email or password' });

    res.json({ message: 'Login successful', user: { id: user._id, role: user.role, name: user.name } });

  } catch (err) {
    console.error('Login error:', err);
    res.status(500).json({ message: 'Internal server error' });
  }
});

module.exports = router;
