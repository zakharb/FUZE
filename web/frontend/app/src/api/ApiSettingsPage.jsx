import React from "react";
import { useState, useEffect } from 'react';
import axios from "axios";

const api = axios.create({
  baseURL: "api/v1/",
});
api.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem('accessToken')}`;

export const fetchInstallConfig = () => {
    api.get(`/settings/install_config`)
      .then(response => {
        console.log(response);
      })
      .catch(error => console.error(error));
};

export const fetchCheckRules = () => {
    api.get(`/settings/check_rules`)
      .then(response => {
        console.log(response);
      })
      .catch(error => console.error(error));
};

export default api;
