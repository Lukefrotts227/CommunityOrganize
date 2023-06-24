import React, {useState} from "react"; 
import {Link, useNavigate} from "react-router-dom"
import axios from "axios"


const Login = () => {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState(''); 

    const handleUsernameChange = (e) => {

        setUsername(e.target.value); 
    }

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    }


    const handleLogin = async (e) => {

        const response = await 
        axios
        .post('http://localhost:8000//login', {
            username: username, 
            password: password
        })
        .then((response) => {
            console.log(response.data); 
        })
        .catch((error) => {
            console.log("Error", error); 
        })

        setPassword(''); 
        setUsername(''); 

    }





    return(
        <div> 
        <h2> Login </h2> 
        <form onSubmit={handleLogin}>
            <input type="username" placeholder="Username" value={username} onChange={handleUsernameChange}/>
            <input type="password" placeholder="Password" value={password} onChange={handlePasswordChange}/>
            <button type="submit"> Login </button>
        </form>

        </div>

    );
}

export default Login;