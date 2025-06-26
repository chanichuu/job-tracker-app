function ContactDetails({ formData, onChange, onPrev, handleSubmit }) {
    console.log("current step: contact details...")
    return (
        <form onSubmit={handleSubmit} className="create-form">
            <h3>Contact details:</h3>
            <div className="input-div">
                <label className="form-label">Name
                    <input type="text" className="form-input" name="name" value={formData.name} onChange={onChange} maxLength="64"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Phone number  
                    <input type="text" className="form-input" name="phoneNumber" value={formData.phoneNumber} onChange={onChange}/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">E-Mail
                    <input type="text" className="form-input" name="email" value={formData.email} onChange={onChange}/>
                </label>
            </div>
            <button type="submit" className="sub-button">Submit</button>
            <button className="form-button" onClick={onPrev}>Previous</button>
        </form>
    );
}

export default ContactDetails;