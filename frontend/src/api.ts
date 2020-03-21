import axiosPackage, { AxiosResponse } from "axios";
import { InfectedLogResult } from "@/types";

const axios = axiosPackage.create({
  baseURL: process.env.VUE_APP_API_BASE
});

export async function fetchInfectedLog(): Promise<
  AxiosResponse<InfectedLogResult>
> {
  return await axios.get(`/infected_log/`);
}

export default axios;
