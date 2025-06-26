function AddressDetails({ formData, onChange, onNext, onPrev }) { 
    console.log("current step: address details...")
    return (
        <form onSubmit={onNext} className="create-form">
            <h3>Address details:</h3>
            <div className="input-div">
                <label className="form-label">Street
                    <input type="text" className="form-input" name="street" value={formData.street} onChange={onChange} required maxLength="128"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">City  
                    <input type="text" className="form-input" name="city" value={formData.city} onChange={onChange} required maxLength="64"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">State/Prefecture
                    <input type="text" className="form-input" name="state" value={formData.state} onChange={onChange} maxLength="64"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Zip code 
                    <input type="text" className="form-input" name="zipCode" value={formData.zipCode} onChange={onChange} maxLength="10"/>
                </label>
            </div>
            <div className="input-div">
                <label className="form-label">Country 
                    <input type="text" className="form-input" name="country" value={formData.country} onChange={onChange} maxLength="64"/>
                </label>
            </div>
            <button type="submit" className="form-button">Next</button>
            <button className="form-button" onClick={onPrev}>Previous</button>
        </form>
    );
}

export default AddressDetails;