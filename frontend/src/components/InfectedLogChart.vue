<template>
  <ChartLayout :title="title">
    <div :id="graphId"></div>
  </ChartLayout>
</template>

<script lang="ts">
import c3, { ChartConfiguration } from "c3";
import { format } from "date-fns";
import { Component, Vue, Prop } from "vue-property-decorator";
import { fetchInfectedLog } from "@/api";
import { InfectedLog, InfectedLogDataKey } from "@/types";
import ChartLayout from "@/components/ChartLayout.vue";
import { getChartConfig } from "@/utils";

@Component({
  components: {
    ChartLayout
  }
})
export default class InfectedLogChart extends Vue {
  @Prop({ type: String, required: true })
  private title!: string;
  @Prop({ type: String, required: true })
  private graphId!: string;
  @Prop({ type: String, required: true })
  private dataKey!: InfectedLogDataKey;

  private infectedLog: InfectedLog[] = [];

  private get chartConfig(): ChartConfiguration {
    return getChartConfig({
      bindto: `#${this.graphId}`,
      data: {
        rows: [["Dátum", this.title], ...this.chartDataRows]
      },
      tooltip: {
        format: {
          value: this.tooltipValue
        }
      }
    });
  }

  private tooltipValue(
    value: number,
    ratio: number | undefined,
    id: string,
    index: number
  ): string {
    const lastValue: number = index
      ? (this.chartDataRows[index - 1][1] as number)
      : 0;
    return `${value} (+${value - lastValue})`;
  }

  private get chartDataRows() {
    return this.infectedLog.map(item => {
      const date = new Date(item.datetime);
      return [format(date, "yyyy-MM-dd"), item[this.dataKey] as number];
    });
  }

  async mounted() {
    const fetchResult = await fetchInfectedLog();
    this.infectedLog = fetchResult?.data?.results || [];
    c3.generate(this.chartConfig);
  }
}
</script>
