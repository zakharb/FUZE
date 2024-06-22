import React from "react";
import { useState, useEffect } from 'react';
import axios from "axios";

const api = axios.create({
  baseURL: "api/v1/",
});
api.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('accessToken')}`;

export const fetchTimelineData = (setData, tframe) => {
    const queryParams = {
      timeframe: tframe.toLowerCase(),
    };
    const queryString = new URLSearchParams(queryParams).toString();
    api.get(`/siem/timeline?${queryString}`)
      .then(response => {
        if (tframe == 0) {
          console.log(tframe)
          setData(prevData => {
            prevData.labels.push(response.data.labels);
            prevData.labels.shift()
            prevData.dataset1_data.push(response.data.dataset1_data);
            prevData.dataset1_data.shift()
            prevData.dataset2_data.push(response.data.dataset2_data);
            prevData.dataset2_data.shift()
            prevData.dataset3_data.push(response.data.dataset3_data);
            prevData.dataset3_data.shift()
            const newData = {
              ...prevData
            }
            return newData;
          });
        } else {
          setData(response.data); 
        }
      })
      .catch(error => console.error(error));
};

export const fetchSummaryData = (setData) => {
    api.get(`/siem/sum_chart`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchBarData = (setData, tframe) => {
    const queryParams = {
      timeframe: tframe.toLowerCase(),
    };
    const queryString = new URLSearchParams(queryParams).toString();
    api.get(`/siem/bar?${queryString}`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchRadarData = (setData, tframe) => {
    const queryParams = {
      timeframe: tframe.toLowerCase(),
    };
    const queryString = new URLSearchParams(queryParams).toString();
    api.get(`/siem/radar?${queryString}`)
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
    api.get(`/siem/polar?${queryString}`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchCard1Data = (setData) => {
    api.get(`/siem/total_messages`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchCard2Data = (setData) => {
    api.get(`/siem/total_events`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchCard3Data = (setData) => {
    api.get(`/siem/total_incidents`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export const fetchCategoriesData = (setData) => {
    api.get(`/siem/top_categories`)
      .then(response => {
        setData(response.data); 
      })
      .catch(error => console.error(error));
};

export default api;
