import React, {createContext, useState} from 'react'; 

const UserContext = createContext(); 

const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false); // New state variable
  
    const loginUser = (userData) => {
      setUser(userData.username);
      setIsLoggedIn(true); // Set isLoggedIn to true when user logs in
    };
  
    const logoutUser = () => {
      setUser(null);
      setIsLoggedIn(false); // Set isLoggedIn to false when user logs out
    };
  
    const contextValue = {
        user, // Add the username value to the context
        loginUser,
        logoutUser,
      };
  
    return (
      <UserContext.Provider value={contextValue}>{children}</UserContext.Provider>
    );
  };
  

export {UserContext, UserProvider}; 