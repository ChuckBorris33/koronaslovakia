import axios, { AxiosResponse } from "axios";
import cachios from "cachios";
import {
  InfectedIncreaseLogResult,
  InfectedLogResult,
  LastLogByLocationResult,
} from "@/types";

const api = cachios.create(
  axios.create({
    baseURL: process.env.VUE_APP_API_BASE,
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

export async function fetchLastLogByLocation(): Promise<
  AxiosResponse<LastLogByLocationResult>
> {
  return api.get(`/get_last_log_by_location/`);
}

export default api;
