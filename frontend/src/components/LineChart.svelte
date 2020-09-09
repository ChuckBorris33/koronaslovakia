<script lang="ts">
  import c3, { ChartConfiguration, PrimitiveArray, ChartAPI } from "c3";

  import { infectedLog } from "../store";
  import {
    formatNumber,
    getChartConfig,
    getTooltipWithDeltaFormatter,
  } from "../utils";
  import ChartLayout from "./ChartLayout.svelte";

  import type { InfectedLog } from "../types";

  export let id: string;
  export let title: string;
  export let chartDataGetter: (
    log: InfectedLog[],
    timespan: number
  ) => PrimitiveArray[];

  let timespan = 14;
  let rows: PrimitiveArray[] = [];
  let chart: ChartAPI | undefined;

  function labelsFormatter(value: number): string {
    if (timespan != 14) {
      return "";
    }
    return formatNumber(value);
  }

  function getLineChartConfig(timespan: number): ChartConfiguration {
    const newRows = chartDataGetter($infectedLog, timespan);
    // Replacing rows contens so tooltip formatter works correctly
    rows.splice(0, Infinity, ...newRows);
    return getChartConfig({
      bindto: `#${id}_graph`,
      data: {
        rows,
        labels: { format: labelsFormatter },
      },
      tooltip: {
        format: {
          value: getTooltipWithDeltaFormatter(rows),
        },
      },
    });
  }

  $: if ($infectedLog.length) {
    if (!chart) {
      chart = c3.generate(getLineChartConfig(timespan));
    } else {
      const newRows = chartDataGetter($infectedLog, timespan);
      // Replacing rows contens so tooltip formatter works correctly
      rows.splice(0, Infinity, ...newRows);
      chart.load({
        rows,
      });
    }
  }
</script>

<ChartLayout {id} {title} bind:timespan>
  <div id={`${id}_graph`} class:hideGraphPoints={timespan == -1} />
</ChartLayout>
