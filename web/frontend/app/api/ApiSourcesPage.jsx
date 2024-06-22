import axios from "axios";

const api = axios.create({
  baseURL: "api/v1/",
});
api.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('accessToken')}`;

export const fetchSourceData = (setData, setRawData) => {
    api.get(`/source/sources`)
      .then(response => {
        setData(response.data);
        setRawData(response.data);
      })
      .catch(error => console.error(error));
};

export const fetchData = (setData, setRawData) => {
    api.get(`/sources/rule`)
      .then(response => {
        setData(response.data);
        setRawData(response.data);
      })
      .catch(error => console.error(error));
};

export const fetchRuleGet = (id) => {
  return new Promise((resolve, reject) => {
    api.get(`/sources/rule/${id}`)
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        console.error(error);
        reject(error);
      });
  });
};

export const fetchRuleAdd = (data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.post('/sources/rule', data);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchRuleDel = (id) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.delete(`/sources/rule/${id}`);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchRuleCopy = (id) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.post(`/sources/copy/${id}`);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchRuleEdit = (id, data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.put(`/sources/rule/${id}`, data);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchRuleImport = (setData, data) => {
  return new Promise(async (resolve, reject) => {
    try {
      api.put('/sources/import', data)
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

export const fetchRuleImportCSV = (setData, data) => {
  return new Promise(async (resolve, reject) => {
    try {
      api.put('/sources/import_csv', data)
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
      const response = await api.delete(`/sources/delete_all`);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};
export default api;
