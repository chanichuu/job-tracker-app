import JobCard from "../components/JobCard"
import SearchBar from "../components/SearchBar"
import CreateButton from "../components/CreateButton";
import PopUp from "../components/PopUp";
import { useState, useEffect, useCallback } from "react";
import { API_PATH } from "../services/constants";
import "../css/Home.css"
import api from "../services/auth";
import handleDelete from "../services/api";

function Home() {
    const [jobs, setJobs] = useState([]);
    const [showPopUp, setShowPopUp] = useState(false);
    const [currentJob, setCurrentJob] = useState(null);
    const [currentAction, setCurrentAction] = useState("");
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
    }, [fetchJobs, showPopUp]);

    return (
      <div className="home">
        <h1>Jobs</h1>
        <CreateButton/>
        <h3>Showing all your current jobs. Filter by job name.</h3>
        <SearchBar onSearch={fetchJobs}/>
        {error && <div className="error-message">{error}</div>}
        { showPopUp && currentAction === "delete" && <PopUp title="Delete job?" text="Do you want to delete this job:" job={currentJob} onClick={handleDelete} setShowPopUp={setShowPopUp} setCurrentAction={setCurrentAction} setCurrentJob={setCurrentJob}></PopUp>}
        <div className="job-grid">
          {jobs?.map((job) => (
            <JobCard job={job} key={job.id} setCurrentJob={setCurrentJob} setShowPopUp={setShowPopUp} setCurrentAction={setCurrentAction}/>
          ))}
        </div>
      </div>
    )
}

export default Home