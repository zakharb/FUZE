import axios from "axios";

const api = axios.create({
  baseURL: "api/v1/",
});
api.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('accessToken')}`;

export const fetchData = (setData, setRawData) => {
    api.get(`/taxanomy/taxanomy`)
      .then(response => {
        setData(response.data);
        setRawData(response.data);
      })
      .catch(error => console.error(error));
};

export const fetchTaxanomyGet = (id) => {
  return new Promise((resolve, reject) => {
    api.get(`/taxanomy/taxanomy/${id}`)
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        console.error(error);
        reject(error);
      });
  });
};

export const fetchTaxanomyAdd = (data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.post('/taxanomy/taxanomy', data);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchTaxanomyDel = (id) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.delete(`/taxanomy/taxanomy/${id}`);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchTaxanomyCopy = (id) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.post(`/taxanomy/copy/${id}`);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchTaxanomyEdit = (id, data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.put(`/taxanomy/taxanomy/${id}`, data);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchTaxanomyImport = (setData, data) => {
  return new Promise(async (resolve, reject) => {
    try {
      api.put('/taxanomy/import', data)
        .then(response => {
          setData(response.data)
          resolve(response.data);
        });
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchDeleteAll = (id) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.delete(`/taxanomy/delete_all`);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};
export default api;
