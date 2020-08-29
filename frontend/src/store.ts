import { readable } from "svelte/store";

import {
  fetchInfectedLog,
  fetchInfectedIncreaseLog,
  fetchLastLogByLocation,
} from "./api";

import type { Readable } from "svelte/store";
import type {
  InfectedLog,
  InfectedIncreaseLog,
  LastLogByLocation,
} from "./types";

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

async function setLastLogByLocation(set: (value: LastLogByLocation[]) => void) {
  const fetchResult = await fetchLastLogByLocation();
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

export const lastLogByLocation: Readable<LastLogByLocation[]> = readable(
  [],
  (set) => {
    setLastLogByLocation(set);
    return () => {};
  }
);
