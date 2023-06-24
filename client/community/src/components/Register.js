import React, {useState} from "react"; 
import {Link, useNavigate} from "react-router-dom"
import axios from "axios"

const Register = () => {

    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState(''); 

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    }

    const handlePasswordChange = (e) => { 
        setPassword(e.target.value); 
    }
    const handleConfirmPasswordChange = (e) => {
        setConfirmPassword(e.target.value); 
    }

    const handleRegister = async (e) => { 
        e.preventDefault(); 
        if (password !== confirmPassword){
            alert("Passwords do not match"); 
            return;
        }
        const registrationData = {
            username: username,
            password: password,
          };
      
          // Send a POST request to the backend API endpoint
          fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(registrationData),
          })
            .then((response) => response.json())
            .then((data) => {
              // Handle the response from the backend
              console.log(data); // Display the response data
              // Perform any necessary actions based on the response
            })
            .catch((error) => {
              console.error('Error', error);
              // Handle any errors that occurred during the request
            });
        setConfirmPassword('');
        setPassword('');
        setUsername('');
    }


    return (
        <div> 
            <h2> Registration </h2>
            <form onSubmit={handleRegister}>
            <input type = "username" placeholder="Username" value={username} onChange ={handleUsernameChange}/>
            <input type = "password" placeholder="Password" value={password} onChange ={handlePasswordChange}/>
            <input type = "password" placeholder="Confirm Password" value={confirmPassword} onChange ={handleConfirmPasswordChange}/>
            <button type = "submit"> Register </button>
            </form> 
        </div> 
    );
}

export default Register;