import Home from "./pages/Home";
import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import ProtectedRoute from "./components/ProtectedRoute";
import Register from "./pages/Register";
import Login from "./pages/Login";
import JobForm from "./components/JobForm";
import "./css/App.css";
import Favourites from "./pages/Favourites";

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <div className="main-div">
      <NavBar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
          <Route path="/favourites" element={<ProtectedRoute><Favourites /></ProtectedRoute>} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<RegisterAndLogout />} />
          <Route path="/post" element={<ProtectedRoute><JobForm /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  );
}

export default App
