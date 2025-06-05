import { ACCESS_TOKEN, BASE_URL, API_PATH } from "./constants";
import api from "./auth"

export const getJobs = () => {
  api
      .get(`${API_PATH}`)
      .then((res) => res.data)
      .then((data) => {
          setNotes(data);
          console.log(data);
      })
      .catch((err) => alert(err));
};

export const getJobs2 = async () => {
  const response = (await fetch(`${BASE_URL}${API_PATH}`, {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
}))
  const data = await response.json();
  console.log(data)
  return data;
};

export const getFavourites = async (query) => {
  const response = (await fetch(
    `${BASE_URL}${API_PATH}?isFavourite=${encodeURIComponent(
      query
    )}`, {
      method: 'GET',
      headers: {
          'Authorization': 'Bearer ' + ACCESS_TOKEN
      }
  }))
  const data = await response.json();
  return data;
}

export const getJob = async (query) => {
  const response = (await fetch(
    `${BASE_URL}${API_PATH}/${encodeURIComponent(
      query
    )}`, {
      method: 'GET',
      headers: {
          'Authorization': 'Bearer ' + ACCESS_TOKEN
      }
  }))
  const data = await response.json();
  return data;
};
