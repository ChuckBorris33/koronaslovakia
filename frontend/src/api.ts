import axios, { AxiosResponse } from "axios";
import cachios from "cachios";
import { InfectedIncreaseLogResult, InfectedLogResult } from "@/types";

const api = cachios.create(
  axios.create({
    baseURL: process.env.VUE_APP_API_BASE
  })
);

export async function fetchInfectedLog(): Promise<
  AxiosResponse<InfectedLogResult>
> {
  return api.get(`/infected_log/`);
}

export async function fetchInfectedIncreaseLog(): Promise<
  AxiosResponse<InfectedIncreaseLogResult>
> {
  return api.get(`/infected_increase_log/`);
}

export default api;
