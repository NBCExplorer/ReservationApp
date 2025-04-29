import { useNavigate } from "react-router-dom";

function Login({ onLogin }) {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Normally validate credentials here
    onLogin();
    navigate("/");
  };

  return (
    <div>
      <h1>Host Login</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <button type="submit">Sign In</button>
      </form>
      <button onClick={() => navigate("/register")}>Register</button>
    </div>
  );
}

export default Login;
