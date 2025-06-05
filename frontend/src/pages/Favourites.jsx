import JobCard from "../components/JobCard"
import { useState, useEffect } from "react";
import api from "../services/auth"
import { API_PATH } from "../services/constants";
import "../css/Favourites.css"

function Favourites () {
    const [favourites, setFavourites] = useState([]);
    const [error, setError] = useState(null);

    // load all favourites from the backend
    useEffect(() => {
        const loadJobFavourites = () => {
          api.get(API_PATH+"?isFavourite=True")
          .then((res) => res.data)
          .then((data) => {
            setFavourites(data);
            console.log(data);
          })
          .catch((err) => setError(err));
        };
    
        loadJobFavourites();
        }, []);

    return <div className="favourites">
        <h1>Your job favourites</h1>
        <div className="job-grid">
          {favourites?.map((job) => (
            <JobCard job={job} key={job.id} />
          ))}
        </div>
    </div>
}

export default Favourites