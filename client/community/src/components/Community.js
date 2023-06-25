import React, { useState } from 'react'; 
import axios from 'axios'; 
import "./styles/entrance.css"


const Community = ({ onCommunitySuccess }) => {
    const [town, setTown] = useState(''); 
    const [state, setState] = useState(''); 

    const handleTownChange = (e) => { 
        setTown(e.target.value); 
    }

    const handleStateChange = (e) => { 
        setState(e.target.value);
    }
    const dataOfMine = {
        state: state, 
        town: town,
        user: sessionStorage.getItem("username")
    }; 
   
    const handleCommunity = async (e) => { 
        e.preventDefault();
        try{
            const response = await axios.post( 'http://localhost:8000/community', 
            dataOfMine);
            console.log("got it")
            onCommunitySuccess(true);

        } catch (error){
            console.error('Error', error); 
        }

    }


    return(
        <div className = "container">
            <h1> {sessionStorage.getItem("username")}, we notice that you are not part of a community. Allow us to fix that </h1> 
            <form onSubmit={handleCommunity}>
            <input type="text" placeholder="town" value={town} onChange={handleTownChange}/>
            <input type="text" placeholder="state" value={state} onChange={handleStateChange}/>
            <button type="submit"> Submit Data </button>
            </form>
        </div>
    ); 
}
export default Community; 