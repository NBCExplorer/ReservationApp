import { useEffect, useState } from 'react';

function Home({ onLogout }) {
  const [reservations, setReservations] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchReservations() {
      try {
        const res = await fetch('http://localhost:3000/api/reservations/host');
        const data = await res.json();
        console.log('📦 Received data:', data);
        if (!res.ok) throw new Error(data.message || 'Failed to fetch.');
        setReservations(data);
      } catch (err) {
        console.error('❌ Fetch error:', err);
        setError(err.message);
      }
    }

    fetchReservations();
  }, []);

  const handleStatusChange = async (id, newStatus) => {
  try {
    const res = await fetch(`http://localhost:3000/api/reservations/status/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: newStatus }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to update status');

    // Update the reservation locally
    setReservations(prev =>
      prev.map(r => (r._id === id ? { ...r, status: newStatus } : r))
    );
  } catch (err) {
    console.error(`❌ Failed to update reservation ${id}:`, err);
    alert(`Error updating reservation: ${err.message}`);
  }
};

  const handleConfirm = (id) => {
  handleStatusChange(id, 'confirmed');
  };

  const handleRefuse = (id) => {
  handleStatusChange(id, 'denied');
  };


  return (
    <div className="container">
      <h1>Welcome, Host!</h1>
      <h2>Reservations</h2>
      {error && <p className="error-message">{error}</p>}
      {reservations.length === 0 ? (
        <p>No reservations found.</p>
      ) : (
        <div className="reservation-list">
          {reservations.map((r) => (
            <div key={r._id} className="reservation-card">
              <div className="stat-container">
                <p><strong>Listing:</strong> {r.listing_name}</p>
                <p><strong>Guest:</strong> {r.guest?.name || 'Unknown'}</p>
                <p><strong>Arrival:</strong> {r.arrivalDate}</p>
                <p><strong>Departure:</strong> {r.departureDate}</p>
                <p><strong>Guests:</strong> {r.guest_count}</p>
                <p><strong>Total Cost:</strong> ${r.total_cost}</p>
                <p className={`status ${r.status === 'pending' ? 'pending' : ''}`}>
                  <strong>Status:</strong> {r.status}
                </p>
              </div>
              <div className="button-row">
                <button className="confirm-btn" onClick={() => handleConfirm(r._id)}>
                  Confirm the reservation
                </button>
                <button className="refuse-btn" onClick={() => handleRefuse(r._id)}>
                  Refuse the reservation
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    <button onClick={onLogout}>Sign Out</button>

    </div>
  );
}

export default Home;
