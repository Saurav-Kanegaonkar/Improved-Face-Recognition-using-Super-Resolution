import React, {useEffect,useState} from 'react';
import {Link} from 'react-router-dom';


const T_lects = () =>{
	let loop_index = 1;
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

	// <div class="pa4">
	// 	<div class="overflow-auto">
	// 		<table class="f6 w-100 mw8 center" cellspacing="0">
	// 		<tbody class="lh-copy">
	// 			<tr class="stripe-dark">
	// 			<td class="pa3">{value.Date}</td>
	// 			<td class="pa3">{value.batch}</td>
	// 			<td class="pa3">{value.classroom}</td>
	// 			<td class="pa3">{value.subject}</td>
	// 			<td class="pa3">{value.startTime}</td>
	// 			<td class="pa3">{value.endTime}</td>
	// 			<td class="pa3">{value["Student List"][0].student_name}</td>
	// 			<br/>
	// 			<Link to={"/t_attendance"} state ={{loadedData:value}}> Take Attendance </Link>
	// 			</tr>
	// 		</tbody>
	// 		</table>
	// 	</div>
	// </div>
	return( 
			<div className="card container bg-dark" style={{textAlign: "center", marginTop : "3rem", padding : "1rem"}}>
				<table className="table-dark table-striped table-hover ">
					<thead>
					<tr>
						<th scope="col">Sr No</th>
						<th scope="col">Date</th>
						<th scope="col">Batch</th>
						<th scope="col">Classroom</th>
						<th scope="col">Subject</th>
						<th scope="col">Start Time</th>
						<th scope="col">End Time</th>
						<th scope="col">Attendance</th>
					</tr>
					</thead>
					<tbody>
						{ loadedData && loadedData.map((value)=>  
							(
								<tr key={loop_index}>
									<th scope="row">{loop_index++}</th>
									<td>{value.Date}</td>
									<td>{value.batch}</td>
									<td>{value.classroom}</td>
									<td>{value.subject}</td>
									<td>{value.startTime}</td>
									<td>{value.endTime}</td>
									<td><Link style={{color: 'white'}} to={"/t_attendance"} state ={{loadedData:value}}> <button type="button" className="btn btn-info">Attendance</button> </Link></td>
									{/* <td><a class="reset-a" href="/teach/{{g.user_id}}/lectures/{{lecture['batch']}}/{{lecture['Date']}}/{{lecture['startTime']}}"><button type="button" class="btn btn-info">Attendance</button></a></td> */}
								</tr>
							)
						)
						}
					</tbody>
				</table>
			</div>
	)
}

export default T_lects;