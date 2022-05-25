import React, {useEffect,useState} from 'react';
import {Link} from 'react-router-dom';

const Student_Dashboard = () => {
  const [loadedData,setLoadedData] = useState();
  useEffect(() => {
    const sendRequest = async () => {
      try {
        const response = await fetch( "http://localhost:5000/teach/181070029/lectures");
        const responseData = await response.json();
        console.log(responseData)
        setLoadedData(responseData)
        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
    };
    sendRequest();
  }, []);

  return (
    <div>Student_Dashboard</div>
  )
}

export default Student_Dashboard