import React from "react";
import { useState, useEffect } from 'react';
import axios from "axios";

const api = axios.create({
  baseURL: "api/v1/",
});
api.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('accessToken')}`;

export const fetchSummaryData = (setData) => {
    api.get(`/netmap/sum_chart`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchPolarData = (setData, tframe) => {
    const queryParams = {
      timeframe: tframe.toLowerCase(),
    };
    const queryString = new URLSearchParams(queryParams).toString();
    api.get(`/netmap/polar?${queryString}`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchCategoriesData = (setData) => {
    api.get(`/netmap/top_categories`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchMapData = (setData) => {
    api.get(`/netmap/map_data`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchTreeData = (setData) => {
  api.get(`/netmap/tree_data`)
    .then(response => {
      setData(response.data); 
    })
    .catch(error => console.error(error));
};

export const fetchTreeSourcesData = (setData) => {
  api.get(`/netmap/tree_sources`)
    .then(response => {
      setData(response.data); 
    })
    .catch(error => console.error(error));
};

export const fetchTreeDestinationsData = (setData) => {
  api.get(`/netmap/tree_destinations`)
    .then(response => {
      setData(response.data); 
    })
    .catch(error => console.error(error));
};

export default api;
