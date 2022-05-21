import './App.css';
import Attendance from './pages/attendance.js';
import Navbar from './components/Navbar.js';
import {BrowserRouter,Route,Routes,Switch} from 'react-router-dom';
import Auth from './pages/auth.js';
import Login from './pages/login.js';
import T_lects from './pages/teachers/t_lects.js';
import T_attend from './pages/teachers/t_attend.js';

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
	    </Routes>
	    </div>
    </BrowserRouter>
  );
}

export default App;