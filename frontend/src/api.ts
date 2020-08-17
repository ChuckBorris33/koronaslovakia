import axios, { AxiosResponse } from "axios";
import type { InfectedLogResult } from "./types";

const api = axios.create({
  baseURL: process.env.API_BASE,
});

export async function fetchInfectedLog(): Promise<
  AxiosResponse<InfectedLogResult>
> {
  return api.get(`/infected_log/`);
}

export default api;
