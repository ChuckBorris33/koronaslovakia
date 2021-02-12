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
  VACCINATED = "vaccinated",
  VACCINATED_2ND_DOSE = "vaccinated_2nd_dose",
  AG_TESTS = "ag_tests",
  AG_POSITIVE = "ag_positive",
}

export enum InfectedIncreaseLogDataKey {
  INFECTED = "infected_increase",
  TESTS = "tests_increase",
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
  [InfectedLogDataKey.VACCINATED]: number;
  [InfectedLogDataKey.VACCINATED_2ND_DOSE]: number;
  [InfectedLogDataKey.AG_TESTS]: number;
  [InfectedLogDataKey.AG_POSITIVE]: number;
};

export type InfectedIncreaseLog = {
  date: string;
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

export type SummaryValue = {
  title: string;
  value: string;
  delta: string;
};

export type TableColumn = {
  title: string;
  sort: null | "asc" | "desc";
};

export type SortValue = {
  sortColumnKey: string;
  sortType: string;
};


export type SubValueSummaryCard = {
  main: SummaryValue
  subValues: SummaryValue[]
}