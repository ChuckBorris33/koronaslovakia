<template>
  <ChartLayout :title="title">
    <div :id="graphId"></div>
  </ChartLayout>
</template>

<script lang="ts">
import c3, { ChartConfiguration } from "c3";
import { format } from "date-fns";
import { Component, Vue } from "vue-property-decorator";
import { fetchInfectedLog } from "@/api";
import { InfectedLog, InfectedLogDataKey } from "@/types";
import ChartLayout from "@/components/ChartLayout.vue";
import { getChartConfig, getTooltipWithIncreaseFormatter } from "@/utils";

@Component({
  components: {
    ChartLayout
  }
})
export default class OutcomeChart extends Vue {
  private title = "Výsledky ochorenia";
  private graphId = "outcomes-chart";

  private infectedLog: InfectedLog[] = [];

  private get chartConfig(): ChartConfiguration {
    const rows = [["Dátum", "Vyliečení", "Úmrtia"], ...this.chartDataRows];
    return getChartConfig({
      bindto: `#${this.graphId}`,
      data: {
        rows
      },
      tooltip: {
        format: {
          value: getTooltipWithIncreaseFormatter(rows)
        }
      }
    });
  }

  private get chartDataRows() {
    return this.infectedLog
      .filter(
        item =>
          item[InfectedLogDataKey.CURED] || item[InfectedLogDataKey.DEATHS]
      )
      .map(item => {
        const date = new Date(item.datetime);
        return [
          format(date, "yyyy-MM-dd"),
          item[InfectedLogDataKey.CURED],
          item[InfectedLogDataKey.DEATHS]
        ];
      });
  }

  async mounted() {
    const fetchResult = await fetchInfectedLog();
    this.infectedLog = fetchResult?.data?.results || [];
    c3.generate(this.chartConfig);
  }
}
</script>
