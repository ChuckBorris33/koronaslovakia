<template>
  <ChartLayout :title="title">
    <div :id="graphId"></div>
  </ChartLayout>
</template>

<script lang="ts">
import c3, { ChartConfiguration } from "c3";
import { format } from "date-fns";
import { Component, Vue } from "vue-property-decorator";
import { fetchInfectedIncreaseLog } from "@/api";
import { InfectedIncreaseLog } from "@/types";
import ChartLayout from "@/components/ChartLayout.vue";

@Component({
  components: {
    ChartLayout
  }
})
export default class TestsPerDayChart extends Vue {
  private title = "Výsledky testov za deň";
  private graphId = "infected-increase-chart";

  private infectedLog: InfectedIncreaseLog[] = [];

  private get chartConfig(): ChartConfiguration {
    return {
      bindto: `#${this.graphId}`,
      data: {
        type: "bar",
        x: "Dátum",
        xFormat: "%Y-%m-%d",
        rows: [["Dátum", "Pozitívne", "Negatívne"], ...this.chartDataRows],
        labels: true,
        groups: [["Pozitívne", "Negatívne"]],
        hide: ["Spolu"]
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
        }
      },
      tooltip: {
        format: {
          title(x: Date): string {
            return format(x, "dd.MM.yyyy");
          },
          value: this.tooltipValue
        }
      }
    };
  }

  private tooltipValue(
    value: number,
    ratio: number | undefined,
    id: string,
    index: number
  ): string {
    const testsTotal =
      (this.chartDataRows[index][1] as number) +
      (this.chartDataRows[index][2] as number);
    const percentage = Math.round((value / testsTotal) * 10000) / 100;
    return `${value} (${percentage}%)`;
  }

  private get chartDataRows() {
    return this.infectedLog.map(item => {
      const date = new Date(item.datetime);
      return [
        format(date, "yyyy-MM-dd"),
        item.infected_increase,
        item.tests_increase - item.infected_increase
      ];
    });
  }

  async mounted() {
    const fetchResult = await fetchInfectedIncreaseLog();
    this.infectedLog = fetchResult?.data?.results || [];
    c3.generate(this.chartConfig);
  }
}
</script>
