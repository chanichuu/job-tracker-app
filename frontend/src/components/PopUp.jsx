import "../css/PopUp.css"

function PopUp({ title, text, job, onClick, setShowPopUp, setCurrentAction, setCurrentJob }) {
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
            { job !== null && job !== 'undefined' && <h3>{job.job_name} at {job.company_name} </h3>}
            <button className="popup-button" onClick={() => handleConfirmButton(job.id)}>
                Confirm
            </button>
        </div>
    </div>
    )
}

export default PopUp