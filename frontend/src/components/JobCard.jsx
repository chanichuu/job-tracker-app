import "../css/JobCard.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/auth";
import { API_PATH } from "../services/constants";

function JobCard ({job, setCurrentJob, setShowPopUp, setCurrentAction }) {
    const [isFavorite, setIsFavorite] = useState(job.is_favourite);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);  
    const navigate = useNavigate();

    const handleToggleFavorite = async () => {
      setLoading(true);
      setError(null);
      try {
        const updatedJobData = {
          ...job,
          is_favourite: !isFavorite,
        };
  
        const response = await api.put(`${API_PATH}/${job.id}`, updatedJobData);
  
        setIsFavorite(response.data.is_favourite);
        console.log("Job favorite status updated:", response.data);
      } catch (err) {
        console.error("Failed to toggle favorite status:", err);
        setError("Failed to update favorite status.");
      } finally {
        setLoading(false);
      }
    };

    const handleEditButtonClick = () => {
      setCurrentJob(job)
      setCurrentAction("edit")
      navigate("/post", {
        state: {
          currentJob: job,
          currentAction: "edit"
        }
      })
    };

    const handleDeleteButtonClick = () => {
      console.log("delete button clicked!")
      setCurrentJob(job);
      setCurrentAction("delete")
      setShowPopUp(true);
    };

    const handleDetailsButtonClick = () => {
      console.log("details button clicked!")
      setCurrentJob(job);
      setCurrentAction("details")
      setShowPopUp(true);
    };

    return (
      <div className="job-card">
        <div className="job-name">
            <h1>{job.job_name}</h1>
            <div className="job-info">
                <h2>Company: {job.company_name}</h2>
                <h3>Status: {job.state}</h3>
            </div>
            <div className="job-overlay">
              <button
                  id={`fav-btn-${job.id}`}
                  className={`fav-btn ${isFavorite ? "favorited" : ""}`}
                  onClick={handleToggleFavorite}
                  disabled={loading}
                  >
                  {loading ? "..." : "♥"}
              </button>
              <button className="edit-btn" onClick={handleEditButtonClick}>
                  ✏️ 
              </button>
              <button className="dtl-btn" onClick={handleDetailsButtonClick}>
                  ...
              </button>
              <button className="rmv-btn" onClick={handleDeleteButtonClick}>
                  X
              </button>
            </div>
        </div>
      </div>
    )
}

export default JobCard