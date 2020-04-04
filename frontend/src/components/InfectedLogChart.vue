<template>
  <ChartLayout :title="title">
    <div :id="graphId"></div>
  </ChartLayout>
</template>

<script lang="ts">
import c3, { ChartConfiguration, PrimitiveArray } from "c3";
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
export default class InfectedLogChart extends Vue {
  private graphId = "cases-over-time-chart";
  private title = "Počet nakazených";

  private infectedLog: InfectedLog[] = [];

  private get chartConfig(): ChartConfiguration {
    const rows = [["Dátum", "Nakazených", "Aktívnych"], ...this.chartDataRows];
    return getChartConfig({
      bindto: `#${this.graphId}`,
      data: {
        rows,
        hide: ["Aktívnych"]
      },
      tooltip: {
        format: {
          value: getTooltipWithIncreaseFormatter(rows)
        }
      }
    });
  }

  private get chartDataRows(): PrimitiveArray[] {
    return this.infectedLog.map(item => {
      const date = new Date(item.datetime);
      const dateString: string = format(date, "yyyy-MM-dd");
      return [
        dateString,
        item[InfectedLogDataKey.INFECTED],
        item[InfectedLogDataKey.INFECTED] -
          item[InfectedLogDataKey.CURED] -
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
