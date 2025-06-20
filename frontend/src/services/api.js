import { API_PATH } from "../services/constants";
import api from "../services/auth";


const handleDelete = async (query = "") => {
    console.log("query: ", query)
    try {
      if (query === null || query === 'undefined') {
        console.error("no id found")
        alert("Failed to delete job. Please try again later."); // todo: handle error properly
      } else {
        const apiUrl = `${API_PATH}/${encodeURIComponent(query)}`

        const res = await api.delete(apiUrl);
        alert("Job deleted successfully!")
        console.log("Deleted Job with response:", res.data);
      }
    } catch (err) {
      console.error("Failed to delete job:", err);
      alert("Failed to delete job. Please try again later."); // todo: handle error properly
    }
  };


  export default handleDelete;