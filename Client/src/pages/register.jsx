import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Normally send registration info to server
    alert("Host registered!");
    navigate("/login");
  };

  return (
    <div>
      <h1>Host Registration</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Name" required />
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
