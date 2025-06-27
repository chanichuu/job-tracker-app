import JobCard from "../components/JobCard"
import PopUp from "../components/PopUp";
import { useState, useEffect, useCallback } from "react";
import api from "../services/auth"
import { API_PATH } from "../services/constants";
import handleDelete from "../services/api";
import "../css/Favourites.css"

function Favourites () {
    const [favourites, setFavourites] = useState([]);
    const [showPopUp, setShowPopUp] = useState(false);
    const [currentJob, setCurrentJob] = useState(null);
    const [currentAction, setCurrentAction] = useState("");
    const [error, setError] = useState(null);

    // load all favourites from the backend
    const loadJobFavourites = useCallback( async () => {
      setError(null);
      try {
        const apiUrl = `${API_PATH}?isFavourite=True`
        const res = await api.get(apiUrl)
        setFavourites(res.data);
        console.log("Fetched favourites: ", res.data);
      } catch (err) {
        console.error("Failed to fetch favourites:", err);
        setError("Failed to load favourites. Please try again.");
      }
    }, [API_PATH]);

    useEffect(() => {
      loadJobFavourites();
    }, [loadJobFavourites, showPopUp]);
  

    return <div className="favourites">
        <h1>Your favourite jobs:</h1>
        { showPopUp && currentAction === "delete" && <PopUp title="Delete job?" text="Do you want to delete this job:" job={currentJob} onClick={handleDelete} setShowPopUp={setShowPopUp} setCurrentAction={setCurrentAction} setCurrentJob={setCurrentJob}></PopUp>}
        { showPopUp && currentAction === "details" && <PopUp title="Details" text="" job={currentJob} currentAction={currentAction} setShowPopUp={setShowPopUp} setCurrentAction={setCurrentAction} setCurrentJob={setCurrentJob}></PopUp>}
        <div className="job-grid">
          {favourites?.map((job) => (
            <JobCard job={job} key={job.id} setCurrentJob={setCurrentJob} setShowPopUp={setShowPopUp} setCurrentAction={setCurrentAction}/>
          ))}
        </div>
    </div>
}

export default Favourites