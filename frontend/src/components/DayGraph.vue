<template>
  <div id="chart"></div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import c3, { ChartConfiguration } from "c3";
import _ from "lodash";
import { format } from "date-fns";

@Component
export default class DayGraph extends Vue {
  @Prop({ type: Array, required: true })
  private readonly visitorData!: { datetime: string; visitors: number }[];
  @Prop({ type: String, required: true })
  private readonly dateString!: string;
  @Prop({ type: Boolean, required: true })
  private readonly loading!: boolean;

  private get chartConfig(): ChartConfiguration {
    return {
      bindto: "#chart",
      data: {
        type: "line",
        x: "time",
        xFormat: "%Y-%m-%d %H:%M",
        rows: [["time", "visitors"], ...this.chartDataRows]
      },
      axis: {
        x: {
          type: "timeseries",
          tick: {
            rotate: 90,
            values: this.tickValues,
            format: "%H:%M"
          },
          min: this.tickValues[0],
          max: _.last(this.tickValues)!
        }
      },
      legend: {
        hide: true
      }
    };
  }

  private get tickValues() {
    const values = [];
    const minutes = _.range(0, 60, 30).map(value =>
      String(value).padStart(2, "0")
    );
    const hours = _.range(6, 22).map(value => String(value).padStart(2, "0"));
    for (const hour of hours) {
      for (const minute of minutes) {
        values.push(`${this.dateString} ${hour}:${minute}`);
      }
    }
    return values;
  }

  private get chartDataRows() {
    return this.visitorData?.map(item => {
      const date = new Date(item.datetime);
      return [format(date, "yyyy-MM-dd HH:mm"), item.visitors];
    });
  }

  @Watch("chartConfig", { immediate: true, deep: true })
  private redrawChart() {
    c3.generate(this.chartConfig);
  }
}
</script>
