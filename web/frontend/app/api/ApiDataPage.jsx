import React from "react";
import { useState, useEffect } from 'react';
import axios from "axios";

const api = axios.create({
  baseURL: "api/v1/",
});
api.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('accessToken')}`;

export const fetchIncidentsData = async (
  setData, setRawData, startDate, endDate) => {
  try {
    const response = await api.get('/report/meta_events', {
      params: {
        startDate: startDate,
        endDate: endDate
      }
    });
    const filteredResults = response.data.filter(item =>
      item.positive == true
    );
    setData(filteredResults);
    setRawData(response.data);
    setData(filteredResults);
  } catch (error) {
    console.error(error);
  }
};

export const fetchIncidentsRuleGet = (id) => {
  return new Promise((resolve, reject) => {
    api.get(`/report/meta_events/${id}`)
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        console.error(error);
        reject(error);
      });
  });
};

export const fetchIncidentsRuleEdit = (id, data) => {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await api.put(`/report/meta_events/${id}`, data);
      resolve(response.data);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchIncidentsPlaybook = (id, controller) => {
  return new Promise(async (resolve, reject) => {
    try {
      const accessToken = localStorage.getItem('accessToken');
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };      
      console.log(controller);
      const response = await fetch(`api/v1//ai/playbook/${id}`, {
        headers: headers,
        signal: controller.signal,
      });
      resolve(response);
    } catch (error) {
      console.error(error);
      reject(error);
    }
  });
};

export const fetchEventsData = (setData, setRawData) => {
    // fetch(`/api/v1/report/events?startDate=${startDate}&endDate=${endDate}`)
    api.get(`/report/events`)
      .then(response => {
        setData(response.data);
        setRawData(response.data);
      })
      .catch(error => console.error(error));
};

export const fetchEventsRuleGet = (id) => {
  return new Promise((resolve, reject) => {
    api.get(`/report/events/${id}`)
      .then(response => {
        resolve(response.data);
      })
      .catch(error => {
        console.error(error);
        reject(error);
      });
  });
};

export const fetchMessagesData = (setData, setRawData) => {
    api.get(`/report/messages`)
      .then(response => {
        setData(response.data);
        setRawData(response.data);
      })
      .catch(error => console.error(error));
};

export const fetchMessagesFilter = (filters, startDate, endDate, setData, setRawData) => {
    const { Tap, Source, Code } = filters;
    const queryParams = new URLSearchParams({
      startDate: startDate,
      endDate: endDate,
      node_tap: Tap,
      src: Source,
      code: Code,
    }).toString();
    api.get(`/report/messages?${queryParams}`)
      .then(response => {
        const data = response.data;
        setRawData(data);
        setData(data);
      })
      .catch(error => console.error(error));
  };


export const fetchPacketsData = (setData, setRawData) => {
    api.get(`/report/packets`)
      .then(response => {
        setData(response.data);
        setRawData(response.data);
      })
      .catch(error => console.error(error));
};

export const fetchPacketsFilter = (filters, startDate, endDate, setData, setRawData) => {
    const { Tap, Protocol, SourceIP, TargetIP } = filters;
    const queryParams = new URLSearchParams({
      startDate: startDate,
      endDate: endDate,
      src_addr: SourceIP,
      tgt_addr: TargetIP,
      proto: Protocol,
    }).toString();
    api.get(`/report/packets?${queryParams}`)
      .then(response => {
        const data = response.data;
        setRawData(data);
        setData(data);
      })
      .catch(error => console.error(error));
  };

export const fetchEventsFilter = (filters, startDate, endDate, setData, setRawData) => {
    const { Name, Tap, Source } = filters;
    const queryParams = new URLSearchParams({
      startDate: startDate,
      endDate: endDate,
      event_name: Name,
      node_tap: Tap,
      node_name: Source,
    }).toString();
    api.get(`/report/events?${queryParams}`)
      .then(response => {
        const data = response.data;
        setRawData(data);
        setData(data);
        setDataCount(data.length);
      })
      .catch(error => console.error(error));
  };

export const fetchIncidentsFilter = (filters, startDate, endDate, setData, setRawData) => {
    const { Severity, Name, Tactic } = filters;
    const queryParams = new URLSearchParams({
      startDate: startDate,
      endDate: endDate,
      severity: Severity,
      name: Name,
      tactic: Tactic
    }).toString();
    api.get(`/report/meta_events?${queryParams}`)
      .then(response => {
        const data = response.data;
        setRawData(data);
        setData(data);
        setDataCount(data.length);
      })
      .catch(error => console.error(error));
  };

export default api;
