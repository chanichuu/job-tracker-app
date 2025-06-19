import JobCard from "../components/JobCard"
import SearchBar from "../components/SearchBar"
import CreateButton from "../components/CreateButton";
import PopUp from "../components/PopUp";
import { useState, useEffect, useCallback } from "react";
import { API_PATH } from "../services/constants";
import "../css/Home.css"
import api from "../services/auth";

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

    const handleDelete = useCallback(async (query = "") => {
      setError(null);
      console.log("query: ", query)
      try {
        if (query === null || query === 'undefined') {
          console.error("no id found")
          setError("Failed to delete job. Please try again later.")
        } else {
          const apiUrl = `${API_PATH}/${encodeURIComponent(query)}`
  
          const res = await api.delete(apiUrl);
          alert("Job deleted successfully!")
          console.log("Deleted Job with response:", res.data);
        }
      } catch (err) {
        console.error("Failed to delete job:", err);
        setError("Failed to delete job. Please try again later.");
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