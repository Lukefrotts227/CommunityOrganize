import React, { useState } from "react";
import axios from "axios";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    const loginData = {
      username: username,
      password: password,
    };

    try {
      console.log(loginData);
      const data = JSON.stringify(loginData);
      console.log(data)
      const response = await axios.post("http://localhost:8000/login", loginData);
      console.log(response.data); // Display the response data
      // Perform any necessary actions based on the response
    } catch (error) {
      if (error.response.status === 422) {
        const errorMessage = error.response.data.message; // Access the error message
        setError(errorMessage);
      } else {
        console.error("Error", error.response); // Log the error response
      }
    }

    setPassword("");
    setUsername("");
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={handleUsernameChange}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={handlePasswordChange}
        />
        <button type="submit">Login</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
};

export default Login;
