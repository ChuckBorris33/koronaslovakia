<template>
  <ChartLayout :title="title" :timespan.sync="timespan">
    <div :id="graphId"></div>
  </ChartLayout>
</template>

<script lang="ts">
import c3, { ChartConfiguration } from "c3";
import { format, subDays } from "date-fns";
import { Component, Vue, Watch } from "vue-property-decorator";
import { fetchInfectedIncreaseLog } from "@/api";
import { InfectedIncreaseLog } from "@/types";
import ChartLayout from "@/components/ChartLayout.vue";
import { getChartConfig } from "@/utils";

@Component({
  components: {
    ChartLayout
  }
})
export default class TestsPerDayChart extends Vue {
  private title = "Výsledky testov za deň";
  private graphId = "infected-increase-chart";

  private infectedLog: InfectedIncreaseLog[] = [];
  private timespan = 14;

  private get chartConfig(): ChartConfiguration {
    return getChartConfig(
      {
        bindto: `#${this.graphId}`,
        data: {
          type: "bar",
          rows: [["Dátum", "Pozitívne", "Negatívne"], ...this.chartDataRows],
          groups: [["Pozitívne", "Negatívne"]]
        },
        tooltip: {
          format: {
            value: this.tooltipValue
          }
        },
        axis: {
          y: {
            min: 0,
            padding: {
              bottom: 0
            }
          }
        }
      },
      this.timespan
    );
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
    return this.infectedLog
      .filter(item => {
        if (this.timespan < 0) {
          return true;
        }
        const date = new Date(item.datetime);
        const from = subDays(new Date(), this.timespan);
        return date > from;
      })
      .map(item => {
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

  @Watch("timespan")
  timespanChanged() {
    c3.generate(this.chartConfig);
  }
}
</script>
