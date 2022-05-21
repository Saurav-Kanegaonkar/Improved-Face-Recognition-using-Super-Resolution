import React, { useState, useEffect } from "react";

const Navbar = (props) => {

    const [userData,setUserData] = useState({});

    useEffect(() => {
	    const sendRequest = async () => {
	      try {
	        const response = await fetch( "http://localhost:5000/profile");
			const responseData = await response.json();
	        // console.log(responseData)
	        setUserData(responseData)
	        if (!response.ok) {
	          throw new Error(responseData.message);
	        }
	        
	      } catch (err) {
	        console.log(err);
	      }
	    };
	    sendRequest();
	  }, []);

    return(
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
            <a className="navbar-brand" style={{fontSize:"33px"}} href="/"><i className="fa-solid fa-user-astronaut"></i></a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav ml-auto">
                    {userData['College ID'] ? (<li className="nav-item">
                        <a className="nav-link active" aria-current="page" href="/">{userData['College ID']}</a>
                    </li>)
                        : (<li className="nav-item">
                            <a className="nav-link active" aria-current="page" href="login">Login</a>
                        </li>)
                    }
                    
                    {userData['College ID'] ? (<li className="nav-item">
                        <a className="nav-link active" aria-current="page" href="/">Logout</a>
                    </li>)
                        : (<li className="nav-item">
                            <a className="nav-link active" aria-current="page" href="auth">Register</a>
                        </li>)
                    }
                    
                </ul>
            </div>
        </div>
    </nav>
);
};

export default Navbar;