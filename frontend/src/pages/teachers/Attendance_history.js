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



const Attendance_history = () => {

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
			mini_dataset['label'] = single_lectures[keys[i]][0]['Subject'] + ' - ' + single_lectures[keys[i]][0]['Batch'] + " : Single Lectures";
			mini_dataset['data'] = single_lectures[keys[i]].map((lecture) => lecture['Attendance']);
			mini_dataset['backgroundColor'] = 'rgba(' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) +', 0.5)';
			
			chart_dataset = [...chart_dataset, {"labels": chart_labels, "datasets":[mini_dataset]}];
		}

		keys = Object.keys(responseData['monthly_lectures']);
		let monthly_lectures = responseData['monthly_lectures'];
		for (let i=0; i<keys.length; i++)
		{
			let chart_labels = monthly_lectures[keys[i]].map((lecture) => lecture['Month']);
			let mini_dataset = {}
			mini_dataset['label'] = monthly_lectures[keys[i]][0]['Subject'] + ' - ' + monthly_lectures[keys[i]][0]['Batch'] + " : Monthly Lectures";
			mini_dataset['data'] = monthly_lectures[keys[i]].map((lecture) => lecture['Attendance']);
			mini_dataset['backgroundColor'] = 'rgba(' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) + ', ' + Math.floor(Math.random() * 255) +', 0.5)';
			chart_dataset = [...chart_dataset, {"labels": chart_labels, "datasets":[mini_dataset]}];
		}	
		setDataset(chart_dataset);
		console.log(chart_dataset);
  };

  useEffect(() => {
    const sendRequest = async () => {
      try {
        const response = await fetch( "http://localhost:5000/teach/181070029/attendance");
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
        text: 'Student Attendance Percentage',
      },
    },
  };
  
  return (
    <div style={{width:"1000px"}}>
	  	{ dataset && dataset.map((value, index)=>  
              ( 
                <Bar key={index} options={options} data={value} />
              )
            )
        }
    </div>
  );
}

export default Attendance_history