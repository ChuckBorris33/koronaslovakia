import _ from "lodash";
import { format } from "date-fns";
import { ChartConfiguration } from "c3";

export function getChartConfig(config: ChartConfiguration): ChartConfiguration {
  const basicConfig = {
    data: {
      type: "line",
      x: "Dátum",
      xFormat: "%Y-%m-%d",
      rows: [],
      labels: true
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
          left: 3600000 * 12, // 12 hours
          right: 3600000 * 12 // 12 hours
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
    }
  };
  return _.merge(basicConfig, config);
}
