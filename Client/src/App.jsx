import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/register";
import Home from "./pages/Home";
import { useState } from "react";

function App() {
  // Manage authentication state (simple for now)
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Fake login and logout handlers (replace with real server logic later)
  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Home onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

export default App;
