import "./App.css";

import {
    BrowserRouter as Router,
    Routes,
    Route,
} from "react-router-dom";

import Home from "./Home";
import Login from "./Login";
import Benchmark from "./Benchmark";
import ResetPassword from "./ResetPassword";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route 
            exact 
            path="/" 
            element={<Home />}
          />
          <Route 
            path="/Benchmark" 
            element={<Benchmark />}
          />
          <Route 
            path="/Login" 
            element={<Login />}
          />
          <Route 
            path="/ResetPassword" 
            element={<ResetPassword />}
          />
        </Routes>
      </Router>  
    </>
  );
}

export default App;
