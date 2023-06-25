import React, {useState, useContext} from "react"; 
import "./styles/entrance.css"
import axios from "axios"

const Register = ({ onRegisterSuccess } ) => {

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
        if (password !== confirmPassword) {
          alert("Passwords do not match");
          return;
        }
      
        const registrationData = {
          username: username,
          password: password,
        };
      
        try {
          const response = await axios.post(
            'http://localhost:8000/register',
            registrationData
          );
          const userData = response.data;
          console.log(userData);
          onRegisterSuccess();
          console.log(userData.username)
          sessionStorage.setItem("username", registrationData.username);
          //loginUser(userData); // Set only the username in loginUser
        } catch (error) {
          console.error('Error', error);
          // Handle any errors that occurred during the request
        }
      
        setConfirmPassword('');
        setPassword('');
        setUsername('');
      };


    return (
        <div className = "container"> 
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