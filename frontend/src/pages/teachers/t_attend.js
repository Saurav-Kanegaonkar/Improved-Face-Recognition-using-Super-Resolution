import React, { useState, useEffect} from 'react';
import ReactDOM from 'react-dom/client';
import {useLocation} from 'react-router-dom';
const T_attend = () =>{
  let loadedData = "adu"
  let loadedInfo = "1"
  let loop_index = 1
  const location = useLocation()
  loadedData = location.state.loadedData["Student_List"]
  loadedInfo = location.state.loadedData
  // console.log(loadedData)
  // console.log(loadedInfo)
  let response;
  let responseData;
  const [loadedAtt,setLoadedAtt] = useState([]);
  useEffect(() => {
    const sendRequest = async () => {
      try {
        response = await fetch("http://localhost:5000/teach/181070029/lectures");
        responseData = await response.json();
        for(let i =0;i<responseData.length;i++){
          if (responseData[i]["Date"] == loadedInfo["Date"] && responseData[i]["subject"] == loadedInfo["subject"] && responseData[i]["startTime"] == loadedInfo["startTime"]){
            responseData = responseData[i];
            break;
          }
        }
        // console.log(responseData)
        setLoadedAtt(responseData["Student_List"])
        // console.log(loadedAtt)
        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
    };
    sendRequest();
  }, []);

  const updateAttendanceCheckbox = async (studentID, isPresent) =>{
    console.log("Update hututu")
    
    try {
        console.log(loadedAtt)
        loadedData = loadedAtt
        for(let i= 0;i<loadedData.length;i++){
          
            if(loadedData[i].studentID == studentID){
              //console.log("HERE")
              //console.log(studentID)
              //console.log(loadedData[i].studentID)
              loadedData[i].isPresent = isPresent;
              console.log(loadedData[i].isPresent)
            }
          }
        
        //console.log(loadedData)
        setLoadedAtt([...loadedData])
        const response = await fetch(`http://localhost:5000/teach/181070029/lectures/${loadedInfo.batch}/${loadedInfo.Date}/${loadedInfo.startTime}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Access-Control-Allow-Origin':'*'
        },
        body: JSON.stringify(loadedData),
      });
        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
  }

  const updateAttendance = async () =>{
    try {
        response = await fetch("http://localhost:5000/updateAttendance");
        responseData = await response.json();
        //setLoadedAtt(responseData)
        // console.log(responseData)
        //console.log(loadedAtt)

        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
  
    try {
        for(let i= 0;i<loadedData.length;i++){
          let stud_name = loadedData[i].studentName.substring(0, loadedData[i].studentName.indexOf(' '))
          Object.entries(responseData).map(([key, value]) =>{
            if(key == stud_name.toLowerCase()){
              loadedData[i].isPresent = value;
            }
          })
        }
        setLoadedAtt(loadedData)
        const response = await fetch(`http://localhost:5000/teach/181070029/lectures/${loadedInfo.batch}/${loadedInfo.Date}/${loadedInfo.startTime}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Access-Control-Allow-Origin':'*'
        },
        body: JSON.stringify(loadedData),
      });
        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
  }

	return(
    <div>
      <div className="card container bg-dark" style={{textAlign: "center", marginTop : "3rem", padding : "1rem"}}>
        <table className="table-dark table-striped table-hover table-bordered">
          <thead>
          <tr style={{height: "50px"}}>
            <th scope="col">Sr No</th>
            <th scope="col">College ID</th>
            <th scope="col">Student Name</th>
            <th scope="col">Attendance</th>
          </tr>
          </thead>
          <tbody>
            { loadedAtt && loadedAtt.map((value)=>  
              ( 
                <tr key={loop_index} style={{height: "50px"}}>
                  <th scope="row">{loop_index++}</th>
                  <td>{value.studentID}</td>
                  <td>{value.studentName}</td>
                  <td><input style={{width:"20px", height:"20px"}} type="checkbox" checked = {value.isPresent} onChange= {() => updateAttendanceCheckbox(value.studentID, !value.isPresent)}/></td>
                </tr>
              )
            )
            }
          </tbody>
        </table>
			</div>
      <br></br>
      <button className="btn btn-dark" onClick = {updateAttendance}>UPDATE ATTENDANCE</button>
      <br></br>
      <br></br>
    </div>);
}

export default T_attend;