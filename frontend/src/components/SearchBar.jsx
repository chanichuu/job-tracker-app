import { useState } from "react";
import "../css/SearchBar.css"

function SearchBar ({ onSearch }) {
    const [searchQuery, setSearchQuery] = useState("");

    const handleSearch = async (e) => {
      e.preventDefault(); 
      console.log("Search initiated for:", searchQuery);
      if (onSearch) {
        await onSearch(searchQuery);
      }
    };

    return (
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search for jobs..."
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>
   )
}

export default SearchBar