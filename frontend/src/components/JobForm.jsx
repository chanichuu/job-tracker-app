import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
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
    const location = useLocation();
    const navigate = useNavigate();
    const currentAction = location.state?.currentAction || "";
    const [error, setError] = useState(null);

    useEffect(() => {
      if (currentAction === "edit") {
        let jobToEdit = retrieveJobToEdit();

        console.log("Editing current job...")
        setFormData({
          step1: { jobTitle: jobToEdit.job_name, company: jobToEdit.company_name, commuteTime: jobToEdit.commute_time, description: jobToEdit.description,
             jobState: jobToEdit.state, salary: jobToEdit.salary, paidLeave: jobToEdit.vacation_days, jobPriority: jobToEdit.priority},
          step2: { street: jobToEdit.address.street, city: jobToEdit.address.city, state: jobToEdit.address.state,
              zipCode: jobToEdit.address.zip_code, country: jobToEdit.address.country
           },
          step3: { name: jobToEdit.contact.name, phoneNumber: jobToEdit.contact.phone, email: jobToEdit.contact.email }
        });
      }
    }, [location.state, currentAction, navigate]);

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
          if (currentAction === "edit") {
            let jobId = getCurrentJobId()
            if (jobId === null || jobId === undefined) {
              console.error('Error: No job id found. Cannot update job.')
              setError("Error updating job."); // todo show proper error message to user
              navigate("/")
            } else {
              job.id = jobId;
              const response = await api.put(API_PATH+"/"+jobId, job)
              console.log('PUT Response:', response.data)
              alert("Job updated successfully!")
            }
          } else {
            const response = await api.post(API_PATH, job);
            console.log('POST Response:', response.data);
            // handle successful response, go back to home?
            alert("Job created successfully!")
          }
          // clear local storage
          localStorage.removeItem("editingJob")
          navigate("/")
        } catch (error) {
          console.error('Error:', error)
          setError(error)
        }
    };

    const getCurrentJobId = () => {
      let jobToEdit = retrieveJobToEdit();

      return jobToEdit.id;
    }

    const retrieveJobToEdit = () => {
        const jobFromNav = location.state?.currentJob;
        const jobFromStorage = localStorage.getItem("editingJob");
        let jobToEdit = null;

        if (jobFromNav) {
          jobToEdit = jobFromNav;
          localStorage.setItem("editingJob", JSON.stringify(jobFromNav));
        } else if (jobFromStorage) {
          jobToEdit = JSON.parse(jobFromStorage);
        }
        if (!jobToEdit) {
          // If trying to edit without a job, redirect or show error
          console.error("No job provided for editing");
          setError("No job data found. Redirecting to job list...");
          setTimeout(() => navigate("/jobs"), 2000);
          return;
        }

        return jobToEdit;
    }

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
            { currentAction === "edit" && <h1>Edit job:</h1> || <h1>Create a new job:</h1>}
            { formStep === 1 && <JobDetails formData={formData.step1} onChange={handleInputChange} onNext={nextStep}/>}
            { formStep === 2 && <AddressDetails formData={formData.step2} onChange={handleInputChange} onNext={nextStep} onPrev={prevStep}/>}
            { formStep === 3 && <ContactDetails formData={formData.step3} onChange={handleInputChange} onPrev={prevStep} handleSubmit={handleSubmit}/>}

            <button type="submit" className="cancel-button" onClick={handleCancel}>Cancel</button>
        </div>
    )
};

export default JobForm;