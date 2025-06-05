import "../css/JobCard.css";
import { useState } from "react";
import api from "../services/auth";
import { API_PATH } from "../services/constants";

function JobCard ({job}) {
    const [isFavorite, setIsFavorite] = useState(job.is_favourite);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);  

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
              <button className="edit-btn">
                  ✏️ {/* todo: add edit functionality */}
              </button>
              <button className="rmv-btn">
                  X {/* todo: add remove functionality */}
              </button>
            </div>
        </div>
      </div>
    )
}

export default JobCard