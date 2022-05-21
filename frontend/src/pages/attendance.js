import React,{useState,useEffect} from 'react';


const Attendance = (props) =>{
	console.log("HEY")
	
	let response;
	let responseData;
	const [loadedAtt,setLoadedAtt] = useState({});
	useEffect(() => {
    const sendRequest = async () => {
      try {
        response = await fetch(
          `http://localhost:5000/`
        );
        responseData = await response.json();
        console.log(responseData)
        setLoadedAtt(responseData)
        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
    };
    sendRequest();
  }, []);
	const updateAttendance = async () =>{
		try {
        response = await fetch(
          `http://localhost:5000/updateAttendance`
        );
        responseData = await response.json();
        setLoadedAtt(responseData)
        console.log(responseData)

        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
	}
	return (
		<div>
				<div class="pa4">
		  <div class="overflow-auto">
		  <button onClick = {updateAttendance}>UPDATE ATTENDANCE</button>
		    <table class="f6 w-100 mw9 center" cellspacing="0">
		      <thead>
		        <tr>
		          <th class="fw6 bb b--black-20 tl pb3 pr1 bg-white">Name</th>
		          <th class="fw6 bb b--black-20 tl pb3 pr1 bg-white">Attendance</th>
		        </tr>
		      </thead>
		      <tbody class="lh-copy">
		          {Object.entries(loadedAtt).map(([key, value]) => {
		          	if (value){ 
					return(

						<tr>
							
							<td class="pv3 pr3 bb b--black-20 ">{key}</td>
							<td class="pv3 pr3 bb b--black-20 green">{value.toString().toUpperCase()}</td>
						</tr>
						) } 
					return(

						<tr>
							
							<td class="pv3 pr3 bb b--black-20 ">{key}</td>
							<td class="pv3 pr3 bb b--black-20 red">{value.toString().toUpperCase()}</td>
						</tr>
						) 


				})}
		        
		        
		      </tbody>
		    </table>
		  </div>
		</div>
			
		</div>	
			
		)
}

export default Attendance;