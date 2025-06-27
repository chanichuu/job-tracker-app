import "../css/PopUp.css"

function PopUp({ title, text, job, onClick, currentAction, setShowPopUp, setCurrentAction, setCurrentJob }) {
    const jobExists = job !== null && job !== 'undefined';
    const hidePopUp = () => {
        setShowPopUp(false);
        setCurrentAction("");
        setCurrentJob(null);
    };

    const handleConfirmButton = (id) => {
        onClick(id);
        hidePopUp();
    };

    console.log(job)
    
    return (
    <div className="popup-div">
        <div className="inner-popup-div">
            <button className="popup-cancel-btn" onClick={hidePopUp}>
                X
            </button>
            <h1>{title}</h1>
            <h3>{text}</h3>
            { jobExists && <h3>{job.job_name} at {job.company_name} </h3>}
            { jobExists && currentAction === "details" && <div>
                <p>{job.description}</p>
                <p> Commute time (in minutes): {job.commute_time}</p>
                <p> Current state: {job.state}</p>
                <p> Yearly salary: {job.salary}</p>
                <p> Paid leave: {job.vacation_days}</p>
                <p> Current priority: {job.priority}</p>
                <h3>Address</h3>
                <p> Street: {job.address.street}</p>
                <p> City: {job.address.city}</p>
                <p> State: {job.address.state}</p>         
                <p> Zip Code: {job.address.zip_code}</p>
                <p> Country: {job.address.country}</p>           
                <h3>Contact</h3>
                <p> Name: {job.contact.name}</p>
                <p> E-Mail: {job.contact.email}</p>
                <p> Phone: {job.contact.phone}</p>   
            </div>}

            { currentAction === "delete" && <button className="popup-button" onClick={() => handleConfirmButton(job.id)}>
                Confirm
            </button>}
        </div>
    </div>
    )
}

export default PopUp