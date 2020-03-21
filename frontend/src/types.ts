export enum InfectedLogDataKey {
  INFECTED = "infected",
  TESTS = "tests",
  DATETIME = "datetime"
}

export type InfectedLog = {
  [TKey in InfectedLogDataKey]: number;
};

export type InfectedLogResult = { results: InfectedLog[] };
