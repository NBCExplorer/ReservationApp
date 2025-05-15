const mongoose = require('mongoose');
require('dotenv').config();
const app = require('./app'); 
const cors = require('cors');
app.use(cors()); 
const PORT = process.env.PORT || 3000;

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('Connected to MongoDB');
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
  console.log(`🚀 Server is running on http://localhost:${PORT}`);
});}).catch(err => {
  console.error('MongoDB connection error:', err);
});
