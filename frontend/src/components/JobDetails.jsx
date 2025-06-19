function JobDetails({ formData, onChange, onNext }) {
    console.log("current step: job details...")
    return (
        <form onSubmit={onNext} className="create-form">
            <h3>Job details:</h3>
            <div className="input-div">
                <label className="form-label">Job Title 
                    <input type="text" className="form-input" name="jobTitle" value={formData.jobTitle} onChange={onChange} required maxLength="128"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Company 
                    <input type="text" className="form-input" name="company" value={formData.company} onChange={onChange} required maxLength="128"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Commute time (Minutes)
                    <input type="number" className="form-input" name="commuteTime" value={formData.commuteTime} onChange={onChange}/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Description 
                    <input type="text" className="form-input" name="description" value={formData.description} onChange={onChange} maxLength="256"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Job State
                    <select id="jobState" className="form-input" name="jobState" value={formData.jobState} onChange={onChange}>
                        <option value="NEW" selected="selected">NEW</option>
                        <option value="APPLIED">APPLIED</option>
                        <option value="INTERVIEW">INTERVIEW</option>
                        <option value="OFFER">OFFER</option>
                        <option value="REJECTED">REJECTED</option>
                    </select>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Yearly Income 
                    <input type="number" className="form-input" name="salary" value={formData.salary} onChange={onChange} min="0"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Paid leave
                    <input type="number" className="form-input" name="paidLeave" value={formData.paidLeave} onChange={onChange} min="0"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Priority
                    <select id="jobState" className="form-input" name="jobPriority" value={formData.jobPriority} onChange={onChange}>
                        <option value="1" selected="selected">LOW</option>
                        <option value="2">MEDIUM</option>
                        <option value="3" selected="selected">HIGH</option>
                    </select>
                </label>
            </div>
            <button type="submit" className="form-button">Next</button>
        </form>
    );
};

export default JobDetails;