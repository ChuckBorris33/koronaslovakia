import _ from "lodash";
import { format } from "date-fns";
import { ChartConfiguration, PrimitiveArray } from "c3";

export function formatNumber(value: number): string {
  const valueStr = value.toString();
  return valueStr.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

export function getChartConfig(
  config: ChartConfiguration,
  timespan = 14
): ChartConfiguration {
  const labels =
    timespan > 0
      ? {
          format: (value: number) => formatNumber(value)
        }
      : false;
  const basicConfig = {
    data: {
      type: "line",
      x: "Dátum",
      xFormat: "%Y-%m-%d",
      rows: [],
      labels
    },
    axis: {
      x: {
        type: "timeseries",
        tick: {
          format: "%d.%m",
          rotate: -60,
          culling: {
            max: 16
          }
        },
        padding: {
          left: 3600000 * 24, // 24 hours
          right: 3600000 * 24 // 24 hours
        }
      },
      y: {
        min: 0,
        padding: {
          bottom: 10
        }
      }
    },
    tooltip: {
      format: {
        title(x: Date): string {
          return format(x, "dd.MM.yyyy");
        }
      }
    },
    color: {
      pattern: ["#2D7DD2", "#EA7317", "#97CC04", "#F45D01"]
    }
  };
  return _.merge(basicConfig, config);
}

export function getTooltipWithDeltaFormatter(chartRows: PrimitiveArray[]) {
  return function(
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
