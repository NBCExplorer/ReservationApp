import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginHost } from "../services/auth";

function Login({ onLogin }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await loginHost(email, password);
      setError("");
      onLogin();
      navigate("/");
    } catch (err) {
      setError(err.message);
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
      <button
        onClick={() => {
          setError("");
          navigate("/register");
        }}
      >
        Register
      </button>
    </div>
  );
}

export default Login;