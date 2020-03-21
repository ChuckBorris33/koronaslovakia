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
    return {
      bindto: `#${this.graphId}`,
      data: {
        type: "line",
        x: "Dátum",
        xFormat: "%Y-%m-%d",
        rows: [["Dátum", this.title], ...this.chartDataRows],
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
        }
      },
      tooltip: {
        format: {
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
    const lastValue: number = index
      ? (this.chartDataRows[index - 1][1] as number)
      : 0;
    return `${value} (+${value - lastValue})`;
  }

  private get chartDataRows() {
    return this.infectedLog.map(item => {
      const date = new Date(item[InfectedLogDataKey.DATETIME]);
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
