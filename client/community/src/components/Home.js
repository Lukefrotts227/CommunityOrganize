import React, { useState, useEffect } from "react";
import axios from 'axios';
import "./styles/back.css";

function Home() {
  const [data, setData] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/');
      setData(response.data.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className="container">
      <h1>Welcome To The Community Action Organizer</h1>
      <h2>Do you Feel disconnected from local politics?</h2>
      <p>{data}</p>
    </div>
  );
}

export default Home;
