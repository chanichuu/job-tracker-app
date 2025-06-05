import { Link, useNavigate, useLocation  } from "react-router-dom";
import "../css/Navbar.css"
import api from "../services/auth"

function NavBar() {
    const navigate = useNavigate();
    const location = useLocation();
    const handleLogout = () => {
        localStorage.clear()
        navigate('/login');
      };

    return (
        <nav className="navbar fixed-top">
            <div className="navbar-brand">
                <Link to="/" className="nav-brand">Job Tracker App</Link>
            </div>
            <div className="navbar-links">
              {api.isAuthenticated() ? (
              <>
                  <Link to="/" className="nav-link">Home</Link>
                  <Link to="/favourites" className="nav-link">Favourites</Link>
                  <button className="auth-button logout-button" onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <>
                  {location.pathname !== '/login' && (
                    <Link to="/login" className="nav-link">Login</Link>
                  )}
                  {/* Conditionally render Sign up link */}
                  {location.pathname !== '/register' && (
                    <Link to="/register" className="nav-link">Sign up</Link>
                  )}
              </>
            )}
            </div>
        </nav>
    )
}

export default NavBar