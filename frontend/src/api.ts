import axios, { AxiosResponse } from "axios";

import type { InfectedLogResult, InfectedIncreaseLogResult } from "./types";

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

export default api;
