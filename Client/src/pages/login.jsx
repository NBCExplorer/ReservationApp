import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // Hardcoded check
    if (email === "host@example.com" && password === "admin123") {
      setError("");
      onLogin();
      navigate("/");
    } else {
      setError("Login failed. Try again.");
    }
  };

  return (
    <div>
      <h1>Host Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Sign In</button>
      </form>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button onClick={() => {
        setError(""); // Clear message on navigation
        navigate("/register");
      }}>Register</button>
    </div>
  );
}

export default Login;
