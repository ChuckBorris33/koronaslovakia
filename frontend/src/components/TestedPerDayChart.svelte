<script lang="ts">
  import c3, { ChartConfiguration, ChartAPI, PrimitiveArray } from "c3";

  import {
    formatNumber,
    getChartConfig,
    getTestedPerDayChartRows,
  } from "../utils";
  import { infectedIncreaseLog } from "../store";
  import ChartLayout from "./ChartLayout.svelte";

  export let title;
  export let id;

  let timespan = 14;
  let rows: PrimitiveArray[] = [];
  let chart: ChartAPI | undefined;

  function tooltipValue(
    value: number,
    ratio: number | undefined,
    id: string,
    index: number
  ): string {
    const testsTotal =
      (rows[index + 1][1] as number) + (rows[index + 1][2] as number);
    const percentage = Math.round((value / testsTotal) * 10000) / 100;
    return `${value} (${percentage}%)`;
  }

  function labelsFormatter(value: number): string {
    if (timespan === -1) {
      return "";
    }
    return formatNumber(value);
  }

  function getTPDChartConfig(timespan: number): ChartConfiguration {
    const newRows = getTestedPerDayChartRows($infectedIncreaseLog, timespan);
    // Replacing rows contens so tooltip formatter works correctly
    rows.splice(0, Infinity, ...newRows);
    return getChartConfig({
      bindto: `#${id}`,
      data: {
        type: "bar",
        rows,
        labels: { format: labelsFormatter },
        groups: [["Pozitívne", "Negatívne"]],
      },
      tooltip: {
        format: {
          value: tooltipValue,
        },
      },
      axis: {
        y: {
          min: 0,
          padding: {
            bottom: 0,
          },
        },
      },
    });
  }

  $: if ($infectedIncreaseLog.length) {
    if (!chart) {
      chart = c3.generate(getTPDChartConfig(timespan));
    } else {
      const newRows = getTestedPerDayChartRows($infectedIncreaseLog, timespan);
      // Replacing rows contens so tooltip formatter works correctly
      rows.splice(0, Infinity, ...newRows);
      chart.load({
        rows,
      });
    }
  }
</script>

<ChartLayout {id} {title} bind:timespan>
  <div {id} />
</ChartLayout>
