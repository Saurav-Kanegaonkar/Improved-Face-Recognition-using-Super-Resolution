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

    
    const Logout = async () => {
        try {
          console.log("hi")
	        const response = await fetch("http://localhost:5000/logout");
			    const responseData = await response.json();
	        // console.log(responseData)
	        if (!response.ok) {
	          throw new Error(responseData.message);
	        }
          setUserData([])
          window.location.href = "/login";
	      } catch (err) {
	        console.log(err);
	      }
    }



    return(
      // <nav className="navbar navbar-expand-lg navbar-light" style={{backgroundColor : "#b3d5e3"}} id="ftco-navbar">
      //   <div className="collapse navbar-collapse" style={{backgroundColor : "#b3d5e3"}} id="ftco-nav">
	    //     <ul className="navbar-nav m-auto">
	    //     	<li className="nav-item active"><a href="/" className="nav-link">Home</a></li>
	    //     	<li className="nav-item dropdown">
      //         <a className="nav-link dropdown-toggle" href="/" id="dropdown04" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Page</a>
      //         <div className="dropdown-menu" aria-labelledby="dropdown04">
      //         	<a className="dropdown-item" href="/">Page 1</a>
      //           <a className="dropdown-item" href="/">Page 2</a>
      //           <a className="dropdown-item" href="/">Page 3</a>
      //           <a className="dropdown-item" href="/">Page 4</a>
      //         </div>
      //       </li>
	    //     	<li className="nav-item"><a href="/" className="nav-link">Catalog</a></li>
	    //     	<li className="nav-item"><a href="/" className="nav-link">Blog</a></li>
	    //       <li className="nav-item"><a href="/" className="nav-link">Contact</a></li>
	    //     </ul>
	    //   </div>
      // </nav>

      <nav className="navbar navbar-expand-lg navbar-light" style={{backgroundColor : "Black"}} id="ftco-navbar">
      <div className="collapse navbar-collapse" style={{backgroundColor : "Black"}} id="ftco-nav">
          {/* <a className="navbar-brand" style={{fontSize:"33px"}} href="/"><i className="fa-solid fa-user-astronaut"></i></a> */}
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
          </button>
          {userData['Role'] == 'teacher' ? (<a style={{color: 'white'}} className="nav-link active" href="/attendance_history">Attendance History</a>) : (<p></p>)}
          {userData['Role'] == 'teacher' ? (<a style={{color: 'white'}} className="nav-link active" href="/lectures">Lectures</a>) : (<p></p>)}
          {userData['Role'] == 'student' ? (<a style={{color: 'white'}} className="nav-link active" href="/student_dashboard">Dashboard</a>) : (<p></p>)}
          {userData['Role'] == 'student' ? (<a style={{color: 'white'}} className="nav-link active" href="/student_attendance_history">Attendance History</a>) : (<p></p>)}
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
              <ul className="navbar-nav ml-auto">
                  {userData['College ID'] ? (<li className="nav-item">
                      <a className="nav-link active" style={{color: 'white'}} aria-current="page" href="/">{userData['College ID']}</a>
                  </li>)
                      : (<li className="nav-item">
                          <a className="nav-link active" style={{color: 'white'}} aria-current="page" href="login">Login</a>
                      </li>)
                  }
                  
                  {userData['College ID'] ? (<li className="nav-item">
                      <a className="nav-link active" style={{color: 'white'}} aria-current="page" href="/login" onClick={() => Logout()}>Logout</a>
                  </li>)
                      : (<li className="nav-item">
                          <a className="nav-link active" style={{color: 'white'}} aria-current="page" href="auth">Register</a>
                      </li>)
                  }
                  
              </ul>
          </div>
      </div>
  </nav>
);
};

export default Navbar;