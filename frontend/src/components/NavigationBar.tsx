import { Link } from "react-router";

function NavigationBar() {
    return (
        <nav className="nav-bar">
            <div className="nav-bar-app">
                <Link to='/'>Play suggest</Link>
            </div>
            <div className="nav-bar-links">
                <Link to='/' className="nav-link">Home</Link>
                <Link to='/favorites' className="nav-link">Favorites</Link>
            </div>
        </nav>
    );
}

export default NavigationBar;