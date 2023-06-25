import React, { useState, useEffect} from "react";
import axios from 'axios'; 
import { BrowserRouter as Router, Route, Link, Routes} from 'react-router-dom';
import { useHistory } from 'react-router-dom';
import Register from "./components/Register";
import Home from "./components/Home";
import Login from "./components/Login";
import Community from "./components/Community";
import Dashboard from "./components/Dashboard"; 
import Creatpost from "./components/Createpost";





function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isRegistered, setIsRegistered] = useState(false);
  const [inCommunity, setInCommunity] = useState(false);
  const [advance1, setAdvance] = useState(false);

 

  const handleRegisterSuccess = () => {
    setIsRegistered(true);
    if (isRegistered && inCommunity){
      setAdvance(true); 
  }

  };

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    if (isLoggedIn){
      console.log("here")
      setAdvance(true); 
  }
    setAdvance(true)
    console.log(advance1)
    console.log(true)

  };

  const handleCommunitySuccess = () => {
    setInCommunity(true); 
    console.log(advance1);
    if (isRegistered && inCommunity){
      setAdvance(true); 
  }
  }


  if (!isLoggedIn && !isRegistered)
  {
    return(
      <Router>
        <div>
          <nav>
            <ul>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/register">Register</Link>
            </li>
            <li>
              <Link to="/"> Home </Link>
            </li>  
            </ul>
          </nav>
          <Routes>
           <Route
                path="/register"
                element={<Register onRegisterSuccess={handleRegisterSuccess} />}
              />
          <Route
                path="/login"
                element={<Login onLoginSuccess={handleLoginSuccess} />}
              />
          <Route path="/" element={<Home/>}/>
          </Routes>
          
        </div>


      </Router> 
    ); 
  }

  if (isRegistered && !advance1){
    return(
    <Router>
      <div>
        <Community onCommunitySuccess={handleCommunitySuccess} />
      </div>
    </Router>
    );
  }
  if(advance1){
    return(
      <Router>
      <div>
        <nav> 
          <ul>
            <li>
                <Link to="/dashboard" > Main dash </Link>
            </li>
            <li> 
                <Link to="/createpost"> Click to make a post </Link> 
            </li>
          </ul>
        </nav>
        <Routes> 
          <Route path="/dashboard" element = {<Dashboard/>}/>
          <Route path="/createpost" element ={<Creatpost/>}/>
        </Routes> 
      </div>

      </Router> 
    ); 
  }

}
export default App;