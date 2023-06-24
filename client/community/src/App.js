import React, { useState, useEffect} from "react";
import axios from 'axios'; 
import { BrowserRouter as Router, Route, Link, Routes} from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import Register from "./components/Register";
import Home from "./components/Home";
import Login from "./components/Login";




function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);

  return(
    <Router>
        <div> 
          <nav> 
            <ul>
              <li>
                <Link to="/login">Login</Link>
              </li>
              <li> 
                <Link to="/Register"> Register </Link>
              </li>
              <li>
                <Link to="/"> Home </Link>
              </li>
            </ul>
          </nav>

          <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          </Routes>

        </div> 

    </Router>
  );
}
export default App;