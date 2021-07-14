import React from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import Home from "./components/Landing/Home";
import StarDrawer from "./components/StarDrawer/StarDrawer";
import "./assets/css/styles.css";

export default function App() {
  return (
      <Router>
        <div>
          <nav className="navbar navbar-light bg-light">
            <ul className="nav">
              <li className="nav-item">
                <Link className="nav-link" to="/">صفحه‌ی اصلی</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/star/">ستاره‌ساز</Link>
              </li>
            </ul>
          </nav>
          <Switch>
            <Route exact path="/">
              <Home />
            </Route>
            <Route exact path="/star/">
              <StarDrawer/>
            </Route>
          </Switch>
        </div>
      </Router>
  );
}