import { readable } from "svelte/store";

import { fetchInfectedLog, fetchInfectedIncreaseLog } from "./api";

import type { Readable } from "svelte/store";
import type { InfectedLog, InfectedIncreaseLog } from "./types";

async function setInfectedLog(set: (value: InfectedLog[]) => void) {
  const fetchResult = await fetchInfectedLog();
  set(fetchResult?.data?.results || []);
}

async function setInfectedIncreaseLog(
  set: (value: InfectedIncreaseLog[]) => void
) {
  const fetchResult = await fetchInfectedIncreaseLog();
  set(fetchResult?.data?.results || []);
}

export const infectedLog: Readable<InfectedLog[]> = readable([], (set) => {
  setInfectedLog(set);
  return () => {};
});

export const infectedIncreaseLog: Readable<InfectedIncreaseLog[]> = readable(
  [],
  (set) => {
    setInfectedIncreaseLog(set);
    return () => {};
  }
);
