import axiosPackage from "axios";

const axios = axiosPackage.create({
  baseURL: process.env.VUE_APP_API_BASE
});

export default axios;
