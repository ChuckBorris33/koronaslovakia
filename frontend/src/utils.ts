import _ from "lodash";
import { format } from "date-fns";
import type { ChartConfiguration, PrimitiveArray } from "c3";
import type { InfectedLog, SummaryValue } from "./types";
import { InfectedLogDataKey } from "./types";

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
      pattern: ["#2D7DD2", "#EA7317", "#97CC04", "#F45D01"],
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

export function getActiveSummaryValue(lastLogs: InfectedLog[]): SummaryValue {
  const lastActive: number =
    lastLogs[0][InfectedLogDataKey.INFECTED] -
    lastLogs[0][InfectedLogDataKey.DEATHS] -
    lastLogs[0][InfectedLogDataKey.CURED];
  const beforeActive: number =
    lastLogs[1][InfectedLogDataKey.INFECTED] -
    lastLogs[1][InfectedLogDataKey.DEATHS] -
    lastLogs[1][InfectedLogDataKey.CURED];
  return {
    title: "Aktívnych",
    value: formatNumber(lastActive),
    delta: formatSummaryDelta(lastActive - beforeActive),
  };
}
