import _ from "lodash";
import { format, subDays } from "date-fns";

import { InfectedLogDataKey } from "./types";

import type { ChartConfiguration, PrimitiveArray } from "c3";
import type {
  InfectedLog,
  InfectedIncreaseLog,
  LastLogByLocation,
  SummaryValue,
  TableColumn,
  SortValue,
} from "./types";

export function formatNumber(value: number): string {
  const valueStr = value.toString();
  return valueStr.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

export function getChartConfig(config: ChartConfiguration): ChartConfiguration {
  const basicConfig = {
    data: {
      type: "line",
      x: "Dátum",
      xFormat: "%Y-%m-%d",
      rows: [],
    },
    axis: {
      x: {
        type: "timeseries",
        tick: {
          format: "%d.%m",
          rotate: -60,
          culling: {
            max: 16,
          },
        },
        padding: {
          left: 3600000 * 24, // 24 hours
          right: 3600000 * 24, // 24 hours
        },
      },
      y: {
        min: 0,
        padding: {
          bottom: 10,
        },
      },
    },
    tooltip: {
      format: {
        title(x: Date): string {
          return format(x, "dd.MM.yyyy");
        },
      },
    },
    color: {
      pattern: ["#2D7DD2", "#EA7317", "#5f8103", "#F45D01"],
    },
  };
  return _.merge(basicConfig, config);
}

export function getTooltipWithDeltaFormatter(chartRows: PrimitiveArray[]) {
  return function (
    value: number,
    ratio: number | undefined,
    id: string,
    index: number
  ): string {
    const columnId = chartRows[0].indexOf(id);
    const lastValue: number =
      index > 0 ? (chartRows[index][columnId] as number) : 0;
    const delta = value - lastValue;
    const sign = delta > 0 ? "+" : "";
    return `${formatNumber(value)} (${sign}${formatNumber(delta)})`;
  };
}

export function normalizeString(str: string): string {
  return str
    .toLowerCase()
    .trim()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function formatSummaryDelta(value: number): string {
  if (value == 0) {
    return "";
  }
  const formattedValue = formatNumber(value);
  return value > 0 ? `(+${formattedValue})` : `(${formattedValue})`;
}

export function getSummaryValue(
  lastLogs: InfectedLog[],
  key: InfectedLogDataKey,
  title: string
): SummaryValue {
  return {
    title,
    value: formatNumber(lastLogs[0][key]),
    delta: formatSummaryDelta(lastLogs[0][key] - lastLogs[1][key]),
  };
}

export function getInfectedChartRows(
  logs: InfectedLog[],
  timespan: number
): PrimitiveArray[] {
  const data = logs
    .filter((item) => {
      if (timespan < 0) {
        return true;
      }
      const date = new Date(item.date);
      const from = subDays(new Date(), timespan);
      return date > from;
    })
    .map((item) => {
      const date = new Date(item.date);
      const dateString: string = format(date, "yyyy-MM-dd");
      return [dateString, item[InfectedLogDataKey.INFECTED]];
    });
  return [["Dátum", "Nakazených"], ...data];
}

export function getOutcomeChartRows(
  logs: InfectedLog[],
  timespan: number
): PrimitiveArray[] {
  const data = logs
    .filter((item) => item[InfectedLogDataKey.DEATHS])
    .filter((item) => {
      if (timespan < 0) {
        return true;
      }
      const date = new Date(item.date);
      const from = subDays(new Date(), timespan);
      return date > from;
    })
    .map((item) => {
      const date = new Date(item.date);
      return [format(date, "yyyy-MM-dd"), item[InfectedLogDataKey.DEATHS]];
    });
  return [["Dátum", "Úmrtia"], ...data];
}

export function getHospitalizedChartRows(
  logs: InfectedLog[],
  timespan: number
): PrimitiveArray[] {
  const firstNonEmptyId = logs.findIndex((item) => {
    return (
      item[InfectedLogDataKey.HOSPITALIZED] ||
      item[InfectedLogDataKey.CONFIRMED_HOSPITALIZED] ||
      item[InfectedLogDataKey.CONFIRMED_HOSPITALIZED_ICU] ||
      item[InfectedLogDataKey.CONFIRMED_HOSPITALIZED_VENTILATION]
    );
  });
  const nonEmptyLogs = logs.slice(firstNonEmptyId);
  const data = nonEmptyLogs
    .filter((item) => {
      if (timespan < 0) {
        return true;
      }
      const date = new Date(item.date);
      const from = subDays(new Date(), timespan);
      return date > from;
    })
    .map((item) => {
      const date = new Date(item.date);
      return [
        format(date, "yyyy-MM-dd"),
        item[InfectedLogDataKey.HOSPITALIZED],
        item[InfectedLogDataKey.CONFIRMED_HOSPITALIZED],
        item[InfectedLogDataKey.CONFIRMED_HOSPITALIZED_ICU],
        item[InfectedLogDataKey.CONFIRMED_HOSPITALIZED_VENTILATION],
      ];
    });
  return [
    [
      "Dátum",
      "Hospitalizovaných",
      "Potvrdený covid19",
      "Na JIS",
      "Na ventilácií",
    ],
    ...data,
  ];
}

export function getVaccinatedChartRows(
  logs: InfectedLog[],
  timespan: number
): PrimitiveArray[] {
  const firstNonEmptyId = logs.findIndex(
    (item) => item[InfectedLogDataKey.VACCINATED]
  );
  const nonEmptyLogs = logs.slice(firstNonEmptyId);
  const data = nonEmptyLogs
    .filter((item) => {
      if (timespan < 0) {
        return true;
      }
      const date = new Date(item.date);
      const from = subDays(new Date(), timespan);
      return date > from;
    })
    .map((item) => {
      const date = new Date(item.date);
      return [
        format(date, "yyyy-MM-dd"),
        item[InfectedLogDataKey.VACCINATED],
        item[InfectedLogDataKey.VACCINATED_2ND_DOSE],
      ];
    });
  return [
    ["Dátum", "Počet zaočkovaných", "Počet zaočkovaných 2. dávkou"],
    ...data,
  ];
}

export function getTestedPerDayChartRows(
  logs: InfectedIncreaseLog[],
  timespan: number
) {
  const data = logs
    .filter((item) => {
      if (timespan < 0) {
        return true;
      }
      const date = new Date(item.date);
      const from = subDays(new Date(), timespan);
      return date > from;
    })
    .map((item) => {
      const date = new Date(item.date);
      return [
        format(date, "yyyy-MM-dd"),
        item.tests_increase != 0
          ? item.infected_increase / item.tests_increase
          : 0,
        item.infected_increase,
        item.tests_increase - item.infected_increase,
      ];
    });
  return [["Dátum", "Percento pozitívnych", "Pozitívne", "Negatívne"], ...data];
}

export function getCurrentSort(
  columns: Record<string, TableColumn>
): SortValue {
  const sortColumnKey: string = _.findKey(
    columns,
    (column) => column.sort !== null
  );
  const sortType = columns[sortColumnKey].sort;
  return {
    sortColumnKey,
    sortType,
  };
}

export function getInfectedByLocationTableRows(
  data: LastLogByLocation[],
  columns: Record<string, TableColumn>,
  filter: string
): LastLogByLocation[] {
  const allRows = data.map((item) => {
    return {
      ...item,
      last_updated: new Date(item.last_updated),
    };
  });

  const filteredRows = allRows.filter((item) => {
    const filterValue = normalizeString(filter);
    return normalizeString(item.location).startsWith(filterValue);
  });

  const { sortColumnKey, sortType } = getCurrentSort(columns);
  let sortedRows = _.sortBy(filteredRows, [sortColumnKey]);
  if (sortType == "desc") {
    sortedRows = _.reverse(sortedRows);
  }

  return sortedRows.map((item) => {
    return {
      ...item,
      last_updated: format(item.last_updated, "d.M.yyyy"),
    };
  });
}
