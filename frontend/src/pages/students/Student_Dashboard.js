import React, {useEffect,useState} from 'react';
import {Link} from 'react-router-dom';

const Student_Dashboard = () => {
  let loop_index = 1;
	const [loadedData,setLoadedData] = useState();
	const [filData,setfilData] = useState();
	let fData = []
	var now = new Date();
  var month = (now.getMonth() + 1);               
  var day = now.getDate();
  if (month < 10) 
      month = "0" + month;
  if (day < 10) 
      day = "0" + day;
  var today = now.getFullYear() + '-' + month + '-' + day;

  const startfilterData = (responseData) => {
		fData = [];
		let date = document.getElementById('Date').value;
		if(date !== '')
		{
			today = date;
		}
		for(let i= 0;i<responseData.length;i++)
		{
			if(responseData[i]['Date'] == today)
			{
				fData = [...fData, responseData[i]]
			}
		}
		setfilData([...fData]);
	}

  const filterData = () => {
		let date = document.getElementById('Date').value;
		let subject = document.getElementById('Subject').value;
		let batch = document.getElementById('Batch').value;
		if(subject === '--- All Subjects ---' && batch === '--- All Batches ---')
		{
			fData = [];
			for(let i= 0;i<loadedData.length;i++)
			{
				if(loadedData[i]['Date'] == date)
				{
					fData = [...fData, loadedData[i]]
				}
			}
			console.log(fData);
			setfilData([...fData]);
		}
		else if(subject === '--- All Subjects ---' && batch !== '--- All Batches ---')
		{
			fData = [];
			for(let i= 0;i<loadedData.length;i++)
			{
				if(loadedData[i]['Date'] == date && loadedData[i]['batch'] == batch)
				{
					fData = [...fData, loadedData[i]]
				}
			}
			setfilData([...fData]);
		}
		else if(subject !== '--- All Subjects ---' && batch === '--- All Batches ---')
		{
			fData = [];
			for(let i= 0;i<loadedData.length;i++)
			{
				if(loadedData[i]['Date'] == date && loadedData[i]['subject'] == subject)
				{
					fData = [...fData, loadedData[i]]
				}
			}
			console.log(fData);
			setfilData([...fData]);
		}
		else
		{
			fData = [];
			for(let i= 0;i<loadedData.length;i++)
			{
				if(loadedData[i]['Date'] == date && loadedData[i]['subject'] == subject &&  loadedData[i]['batch'] == batch)
				{
					fData = [...fData, loadedData[i]]
				}
			}
			setfilData([...fData]);
		}
		console.log(fData);
	}

  useEffect(() => {
    const sendRequest = async () => {
      try {
        const response = await fetch( "http://localhost:5000/student/181070029/student_dashboard");
        const responseData = await response.json();
        console.log(responseData)
        setLoadedData(responseData)
        startfilterData(responseData)
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
    <div className="card container bg-dark" style={{textAlign: "center", marginTop : "3rem", padding : "1rem"}}>
				<div className="row" >
					<div className="col-1" style={{padding: 0}}>
						<label style={{color: "white"}} htmlFor="Date" >Date:</label><br />
					</div>
					<div className="col-2" style={{padding: 0}}>
						<input type="date" id="Date" name="Date" defaultValue={today} onChange={(e) => filterData()}/>
					</div>
					<div className="col-1" style={{padding: 0}}>
						<label style={{color: "white"}} htmlFor="Subject">Subject:</label>
					</div>
					<div className="col-3" style={{padding: 0}}>
						<div className="form-group">
							<select placeholder="Subject" className="form-control" id="Subject" onChange={(e) => filterData()}>
								<option>--- All Subjects ---</option>
								<option>Maths</option>
								<option>DSA</option>
								<option>Blockchain Technology</option>
							</select>
						</div>
					</div>
					<div className="col-1" style={{padding: 0}}>
						<label style={{color: "white"}} htmlFor="Batch">Batch:</label>
					</div>
					<div className="col-3" style={{padding: 0}}>
						<div className="form-group">
							<select placeholder="Batch" className="form-control" id="Batch" onChange={(e) => filterData()}>
								<option>--- All Batches ---</option>
								<option>BTECH_COMPS_2018_2022</option>
							</select>
						</div>
					</div>
				</div>
				<br />
				
				<table className="table-dark table-striped table-hover table-bordered">
					<thead>
					<tr style={{height: "50px"}}>
						<th scope="col">Sr No</th>
						<th scope="col">Date</th>
						<th scope="col">Classroom</th>
						<th scope="col">Teacher</th>
						<th scope="col">Subject</th>
						<th scope="col">Start Time</th>
						<th scope="col">End Time</th>
						<th scope="col">Attendance</th>
					</tr>
					</thead>
					<tbody>
						{ filData && filData.map((value)=>  
							(
								<tr key={loop_index} style={{height: "50px"}}>
									<th scope="row">{loop_index++}</th>
									<td>{value.Date}</td>
									<td>{value.classroom}</td>
									<td>{value.teacher}</td>
									<td>{value.subject}</td>
									<td>{value.startTime}</td>
									<td>{value.endTime}</td>
									<td>{value.isPresent.toString().toUpperCase()}</td>
								</tr>
							)
						)
						}
					</tbody>
				</table>
			</div>
  )
}

export default Student_Dashboard