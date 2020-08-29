import axios, { AxiosResponse } from "axios";

import type {
  InfectedLogResult,
  InfectedIncreaseLogResult,
  LastLogByLocationResult,
} from "./types";

const api = axios.create({
  baseURL: process.env.API_BASE,
});

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
