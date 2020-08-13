export enum InfectedLogDataKey {
  INFECTED = "infected",
  TESTS = "tests",
  CURED = "cured",
  DEATHS = "deaths",
  MEDIAN = "median",
  HOSPITALIZED = "hospitalized",
  CONFIRMED_HOSPITALIZED = "confirmed_hospitalized",
  CONFIRMED_HOSPITALIZED_ICU = "confirmed_hospitalized_icu",
  CONFIRMED_HOSPITALIZED_VENTILATION = "confirmed_hospitalized_ventilation",
}

export type InfectedLog = {
  date: string;
  [InfectedLogDataKey.INFECTED]: number;
  [InfectedLogDataKey.TESTS]: number;
  [InfectedLogDataKey.CURED]: number;
  [InfectedLogDataKey.DEATHS]: number;
  [InfectedLogDataKey.MEDIAN]: number;
  [InfectedLogDataKey.HOSPITALIZED]: number;
  [InfectedLogDataKey.CONFIRMED_HOSPITALIZED]: number;
  [InfectedLogDataKey.CONFIRMED_HOSPITALIZED_ICU]: number;
  [InfectedLogDataKey.CONFIRMED_HOSPITALIZED_VENTILATION]: number;
};

export type InfectedLogResult = { results: InfectedLog[] };

export type SummaryValue = {
  title: string;
  value: string;
  delta: string;
};
