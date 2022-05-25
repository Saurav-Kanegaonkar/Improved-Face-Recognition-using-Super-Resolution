import './App.css';
import Attendance from './pages/attendance.js';
import Navbar from './components/Navbar.js';
import {BrowserRouter,Route,Routes,Switch} from 'react-router-dom';
import Auth from './pages/auth.js';
import Login from './pages/login.js';
import T_lects from './pages/teachers/t_lects.js';
import T_attend from './pages/teachers/t_attend.js';
import Attendance_history from './pages/teachers/Attendance_history.js';
import Student_Dashboard from './pages/students/Student_Dashboard.js';

function App() {
  return (
  	<BrowserRouter>

	    <div className="App">
	      <header>
	        <Navbar/>
	      </header>
	    <Routes>
		    <Route path="/auth" element={<Auth/>}/>
		    <Route path="/login" element={<Login/>}/>
		    <Route path="/attendance" element={<Attendance/>}/>
		    <Route path="/lectures" element={<T_lects/>}/>
		    <Route path="/t_attendance" element={<T_attend/>}/>
		    <Route path="/attendance_history" element={<Attendance_history/>}/>
		    <Route path="/student_dashboard" element={<Student_Dashboard/>}/>
	    </Routes>
	    </div>
    </BrowserRouter>
  );
}

export default App;