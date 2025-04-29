function Home({ onLogout }) {
  return (
    <div>
      <h1>Welcome, Host!</h1>
      <button onClick={onLogout}>Sign Out</button>
    </div>
  );
}

export default Home;
