const mongoose = require('mongoose');

const listingSchema = new mongoose.Schema({
  _id: String, 
  title: {
    type: String,
    required: true
  },
  description: String,
  location: String,
  price: {
    type: Number,
    required: true
  },
  host: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  images: [String],
  amenities: [String],
  availability: {
    type: Boolean,
    default: true
  }
}, { timestamps: true });

module.exports = mongoose.model('Listing', listingSchema);