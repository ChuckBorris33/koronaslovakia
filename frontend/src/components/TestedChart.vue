<template>
  <ChartLayout :title="title" :timespan.sync="timespan">
    <div :id="graphId"></div>
  </ChartLayout>
</template>

<script lang="ts">
import c3, { ChartConfiguration } from "c3";
import { format, subDays } from "date-fns";
import { Component, Vue, Watch } from "vue-property-decorator";
import { fetchInfectedLog } from "@/api";
import { InfectedLog, InfectedLogDataKey } from "@/types";
import ChartLayout from "@/components/ChartLayout.vue";
import { getChartConfig, getTooltipWithDeltaFormatter } from "@/utils";

@Component({
  components: {
    ChartLayout
  }
})
export default class TestedChart extends Vue {
  private title = "Počet testov";
  private graphId = "tests-chart";

  private infectedLog: InfectedLog[] = [];
  private timespan = 14;

  private get chartConfig(): ChartConfiguration {
    const rows = [["Dátum", this.title], ...this.chartDataRows];
    return getChartConfig(
      {
        bindto: `#${this.graphId}`,
        data: {
          rows
        },
        tooltip: {
          format: {
            value: getTooltipWithDeltaFormatter(rows)
          }
        }
      },
      this.timespan
    );
  }

  private get chartDataRows() {
    return this.infectedLog
      .filter(item => {
        if (this.timespan < 0) {
          return true;
        }
        const date = new Date(item.date);
        const from = subDays(new Date(), this.timespan);
        return date > from;
      })
      .map(item => {
        const date = new Date(item.date);
        return [format(date, "yyyy-MM-dd"), item[InfectedLogDataKey.TESTS]];
      });
  }

  async mounted() {
    const fetchResult = await fetchInfectedLog();
    this.infectedLog = fetchResult?.data?.results || [];
    c3.generate(this.chartConfig);
  }

  @Watch("timespan")
  timespanChanged() {
    c3.generate(this.chartConfig);
  }
}
</script>
