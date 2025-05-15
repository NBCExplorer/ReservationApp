const mongoose = require('mongoose');

const ReservationSchema = new mongoose.Schema({
  guest_email: { type: String, required: true },
  listing_id: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'Listing' },
  listing_name: { type: String, required: true },  
  guest_count: { type: Number, required: true },
  arrival_date: { type: String, required: true },
  leaving_date: { type: String, required: true },
  total_cost: { type: Number, required: true },    
  status: { type: String, default: 'pending' }
}, { collection: 'reservations' });

module.exports = mongoose.model('Reservation', ReservationSchema);
