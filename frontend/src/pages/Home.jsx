import JobCard from "../components/JobCard"
import SearchBar from "../components/SearchBar"
import { useState, useEffect, useCallback } from "react";
import { API_PATH } from "../services/constants";
import "../css/Home.css"
import api from "../services/auth";

function Home() {
    const [jobs, setJobs] = useState([]);
    const [error, setError] = useState(null);

    // load all jobs from the backend
    const fetchJobs = useCallback(async (query = "") => {
      setError(null);
      try {
        const apiUrl = query
          ? `${API_PATH}?beginsWith=${encodeURIComponent(query)}`
          : API_PATH; // if no query, fetch all jobs
  
        const res = await api.get(apiUrl);
        setJobs(res.data);
        console.log("Fetched Jobs:", res.data);
      } catch (err) {
        console.error("Failed to fetch jobs:", err);
        setError("Failed to load jobs. Please try again.");
      }
    }, [API_PATH]);
  
    useEffect(() => {
      fetchJobs();
    }, [fetchJobs]);

    return (
      <div>
        <h1>Jobs</h1>
        <h3>Showing all your current jobs. Filter by job name.</h3>
        <SearchBar onSearch={fetchJobs}/>

        {error && <div className="error-message">{error}</div>}

        <div className="job-grid">
          {jobs?.map((job) => (
            <JobCard job={job} key={job.id} />
          ))}
        </div>
      </div>
    )
}

export default Home