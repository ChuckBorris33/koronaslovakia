export enum InfectedLogDataKey {
  INFECTED = "infected",
  TESTS = "tests",
  CURED = "cured",
  DEATHS = "deaths"
}

export enum InfectedIncreaseLogDataKey {
  INFECTED = "infected_increase",
  TESTS = "tests_increase"
}

export type InfectedLog = {
  datetime: string;
  [InfectedLogDataKey.INFECTED]: number;
  [InfectedLogDataKey.TESTS]: number;
  [InfectedLogDataKey.CURED]: number;
  [InfectedLogDataKey.DEATHS]: number;
};

export type InfectedIncreaseLog = {
  datetime: string;
  [InfectedIncreaseLogDataKey.INFECTED]: number;
  [InfectedIncreaseLogDataKey.TESTS]: number;
};

export type LastLogByLocation = {
  location: string;
  last_updated: string;
  infected: number;
  cured: number;
  deaths: number;
  infected_delta: number;
  cured_delta: number;
  deaths_delta: number;
  infected_females: number;
  infected_males: number;
};

export type InfectedLogResult = { results: InfectedLog[] };
export type InfectedIncreaseLogResult = { results: InfectedIncreaseLog[] };
export type LastLogByLocationResult = { results: LastLogByLocation[] };
