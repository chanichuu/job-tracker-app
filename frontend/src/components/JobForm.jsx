import { useState } from "react";
import { useNavigate  } from "react-router-dom";
import JobDetails from "./JobDetails"
import AddressDetails from "./AddressDetails";
import ContactDetails from "./ContactDetails";
import "../css/JobForm.css"
import api from "../services/auth"
import { API_PATH } from "../services/constants";

function JobForm() {
    const [formStep, setFormStep] = useState(1);
    const [formData, setFormData] = useState({
        step1: { jobTitle: '', company: '', commuteTime: 0, description: '', jobState: 'NEW', salary: '', paidLeave: 0, jobPriority: 1},
        step2: { street: '', city: '', state: '',
            zipCode: '', country: ''
         },
        step3: { name: '', phoneNumber: '', email: '' }
      });
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        console.log("name, value: ", name, value)

        setFormData({
          ...formData,
          [`step${formStep}`]: {
            ...formData[`step${formStep}`],
            [name]: value
          }
        });
    };

    // todo test this!
    const handleSubmit = async (event) => {
        console.log("submitting data to backend...")

        event.preventDefault();

        const job = {
          job_name: formData.step1.jobTitle,
          company_name: formData.step1.company,
          commute_time: formData.step1.commuteTime,
          description: formData.step1.description,
          state: formData.step1.jobState,
          salary: formData.step1.salary,
          vacation_days: formData.step1.paidLeave,
          priority: formData.step1.jobPriority,
          address: {
              street: formData.step2.street,
              city: formData.step2.city,
              state: formData.step2.state,
              zip_code: formData.step2.zipCode,
              country: formData.step2.country,
          },
          contact: {
              name: formData.step3.name,
              phone: formData.step3.phoneNumber,
              email: formData.step3.email,
          }
        }

        console.log(job)
   
        try {
          const response = await api.post(API_PATH, job);   
          console.log('Response:', response.data);
          // handle successful response, go back to home?
          alert("Job created successfully!")
          navigate("/");
        } catch (error) {
          console.error('Error:', error);
          setError(error)
        }
    };

    const handleCancel = () => {
        console.log("Returning to Home...");
        navigate("/");
    };

    const nextStep = () => {
        if (formStep < 3) setFormStep(formStep + 1);
      };
    
    const prevStep = () => {
        if (formStep > 1) setFormStep(formStep - 1);
      };

    return (
        <div className="create-form-div">
            <h1>Create a new job:</h1>
            { formStep === 1 && <JobDetails formData={formData.step1} onChange={handleInputChange} onNext={nextStep}/>}
            { formStep === 2 && <AddressDetails formData={formData.step2} onChange={handleInputChange} onNext={nextStep} onPrev={prevStep}/>}
            { formStep === 3 && <ContactDetails formData={formData.step3} onChange={handleInputChange} onPrev={prevStep} handleSubmit={handleSubmit}/>}

            <button type="submit" className="cancel-button" onClick={handleCancel}>Cancel</button>
        </div>
    )
};

export default JobForm;