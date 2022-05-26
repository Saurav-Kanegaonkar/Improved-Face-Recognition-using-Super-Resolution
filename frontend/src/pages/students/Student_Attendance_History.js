import React, {useEffect,useState} from 'react';

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);


const Student_Attendance_History = () => {
  const [chartData,setChartData] = useState();
  const [dataset,setDataset] = useState();

  const fillData = (responseData) =>{
		let keys = Object.keys(responseData['single_lectures']);
		let single_lectures = responseData['single_lectures'];
		let chart_dataset = [];
		for (let i=0; i<keys.length; i++)
		{
			let chart_labels = single_lectures[keys[i]].map((lecture) => lecture['Date']);
			let mini_dataset = {}
			mini_dataset['label'] = single_lectures[keys[i]][0]['subject'] + " : Single Lectures";
			mini_dataset['data'] = single_lectures[keys[i]].map((lecture) => lecture['isPresent']);
			mini_dataset['backgroundColor'] = 'rgba(' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) +')';
      mini_dataset['borderColor'] = 'black';
			
			chart_dataset = [...chart_dataset, {"labels": chart_labels, "datasets":[mini_dataset]}];
		}

		keys = Object.keys(responseData['monthly_lectures']);
		let monthly_lectures = responseData['monthly_lectures'];
		for (let i=0; i<keys.length; i++)
		{
			let chart_labels = monthly_lectures[keys[i]].map((lecture) => lecture['Month']);
			let mini_dataset = {}
			mini_dataset['label'] = monthly_lectures[keys[i]][0]['Subject'] + " : Monthly Lectures";
			mini_dataset['data'] = monthly_lectures[keys[i]].map((lecture) => (lecture['Presentees']/(lecture['Presentees'] + lecture['Absentees']))*100 );
			mini_dataset['backgroundColor'] = 'rgba(' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) +')';
			chart_dataset = [...chart_dataset, {"labels": chart_labels, "datasets":[mini_dataset]}];
		}	
		setDataset(chart_dataset);
		console.log(chart_dataset);
  };

  useEffect(() => {
    const sendRequest = async () => {
      try {
        const response = await fetch( "http://localhost:5000/student/181070029/attendance");
        const responseData = await response.json();
        console.log(responseData)
        setChartData(responseData)
        fillData(responseData)
        if (!response.ok) {
          throw new Error(responseData.message);
        }
        
      } catch (err) {
        console.log(err);
      }
    };
    sendRequest();
  }, []);

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Personal Attendance Percentage',
      },
    },
  };
  
  return (
    <div style={{width:"75%", backgroundColor: "white", marginLeft: "180px", marginTop:"50px"}}>
	  	{ dataset && dataset.map((value, index)=>  
              ( 
                <div key={index}>
                  <Bar options={options} data={value} />
                  <br></br>
                </div>
              )
            )
        }
    </div>
  );
}

export default Student_Attendance_History