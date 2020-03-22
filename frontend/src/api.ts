import axiosPackage, { AxiosResponse } from "axios";
import { setupCache } from "axios-cache-adapter";
import { InfectedIncreaseLogResult, InfectedLogResult } from "@/types";

const cache = setupCache({
  maxAge: 15 * 60 * 1000
});

const axios = axiosPackage.create({
  adapter: cache.adapter,
  baseURL: process.env.VUE_APP_API_BASE
});

export async function fetchInfectedLog(): Promise<
  AxiosResponse<InfectedLogResult>
> {
  return await axios.get(`/infected_log/`);
}

export async function fetchInfectedIncreaseLog(): Promise<
  AxiosResponse<InfectedIncreaseLogResult>
> {
  return await axios.get(`/infected_increase_log/`);
}

export default axios;
