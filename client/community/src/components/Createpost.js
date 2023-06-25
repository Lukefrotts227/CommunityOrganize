import React, { useState } from 'react'; 
import axios from 'axios'; 


const Creatpost = () => {
    const [title, setTitle] = useState(''); 
    const [content, setContent] = useState(''); 

    const handleTitle = (e) => {
        setTitle(e.target.value); 
    }
    const handleContent = (e) => {
        setContent(e.target.value); 
    }

    const data = {
        title: title,
        content: content,
        user: sessionStorage.getItem('username')
    }

    const handleSubmit = async (e) => {
        e.preventDefault(); 
        await axios.post('http://localhost:8000/createpost', data)

        setTitle(''); 

    }
    return(
        <div>
            <h1> MAX OF 50 WORDS AND GIVE A UNIQUE TITLE</h1>
            <form onSubmit={handleSubmit}>
                <div> 
                    <label htmlfor="title"> Title: </label>
                    <input type="text" id="title" value={title} onChange={handleTitle}/>
                </div> 
                <div>
                    <label htmlfor="content"> Content Here: </label>
                    <input type="text" id="content" value={content} onChange={handleContent}/>
                </div>
                <button type="submit"> Submit data </button>
            </form>
            
        </div>
    );
}

export default Creatpost; 