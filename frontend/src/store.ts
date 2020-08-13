import { readable } from "svelte/store";
import type { Readable } from "svelte/store";
import type { InfectedLog } from "./types";
import { fetchInfectedLog } from "./api";

async function setInfectedLog(set: (value: InfectedLog[]) => void) {
  const fetchResult = await fetchInfectedLog();
  set(fetchResult?.data?.results || []);
}

export const infectedLog: Readable<InfectedLog[]> = readable([], (set) => {
  setInfectedLog(set);
  return () => {};
});
