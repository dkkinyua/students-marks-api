import 'bootstrap/dist/css/bootstrap.min.css';
import React from 'react'
import ReactDOM from 'react-dom'
import {
    BrowserRouter as Router,
    Routes,
    Route
} from 'react-router-dom'

import NavBar from './components/navbar'
import Home from './components/home';
import Login from './components/login';
import SignUp from './components/signup';
import CreateMarks from './components/marks';


const App = () => {

    return (
        <Router>
            <div>
                <NavBar />
                <Routes>
                    <Route path='/' element={<Home/>}/>
                    <Route path='/signup' element={<SignUp/>}/>
                    <Route path='/login' element={<Login/>}/>
                    <Route path='/create-marks' element={<CreateMarks/>}/>
                </Routes>
            </div>
        </Router>
    )
}

ReactDOM.render(<App />, document.getElementById("root"))
