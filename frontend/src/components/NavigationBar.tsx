import { Link } from "react-router";
import '../css/NavigationBar.css';

function NavigationBar() {
    return (
        <nav className="nav-bar">
            <div className="nav-bar-app">
                <Link to='/'><img src="./app_logo.svg" className="app-logo" />Play suggest</Link>
            </div>
            <div className="nav-bar-links">
                <Link to='/' className="nav-link">Home</Link>
                <Link to='/favorites' className="nav-link">Favorites</Link>
                <Link to='/ask_ai' className="nav-link">🫧 Ask AI 🤖</Link>
            </div>
        </nav>
    );
}

export default NavigationBar;