import React, { useState, useEffect } from 'react';
import "./styles/postdisplay.css";
import axios from 'axios';

const Dashboard = () => {
  const [data, setData] = useState([]);

  const fetchData = async () => {
    const username = sessionStorage.getItem("username");
    try {
      const response = await axios.get("http://localhost:8000/giveposts/" + username);
      const jsonData = JSON.parse(response.data);
      setData(jsonData);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRefresh = () => {
    fetchData();
  };

  return (
    <div className = "container">
      <button onClick={handleRefresh}>Refresh</button>
      {data.length === 0 ? (
        <p>No posts available.</p>
      ) : (
        data.map((item) => (
          <div key={item.id}>
            <h2>{item.title}</h2>
            <p>{item.contents}</p>
            <h2> Summary or Alternate </h2>
            <p>{item.summary}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default Dashboard;
