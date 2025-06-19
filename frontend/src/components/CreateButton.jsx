import { useNavigate  } from "react-router-dom";
import "../css/CreateButton.css"

function CreateButton() {
  const navigate = useNavigate();
  const handleCreate = (event) => {
    event.preventDefault();
    console.log("Create button clicked.")
    navigate("/post")
  }  

  return (
      <button type="submit" className="create-button" onClick={handleCreate}>Add Job</button>
  )
};

export default CreateButton;
