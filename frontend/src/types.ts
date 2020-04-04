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

export type InfectedLogResult = { results: InfectedLog[] };
export type InfectedIncreaseLogResult = { results: InfectedIncreaseLog[] };
