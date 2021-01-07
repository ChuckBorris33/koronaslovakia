<script lang="ts">
  import c3, { ChartConfiguration, ChartAPI, PrimitiveArray } from "c3";

  import {
    getChartConfig,
    getTestedPerDayPercentChartRows,
  } from "../utils";
  import { infectedIncreaseLog } from "../store";
  import ChartLayout from "./ChartLayout.svelte";

  export let title: string;
  export let id: string;

  let timespan = 14;
  let rows: PrimitiveArray[] = [];
  let chart: ChartAPI | undefined;

  function tooltipValue(
    value: number,
    ratio: number | undefined,
    id: string,
    index: number
  ): string {
    const percentage = Math.round(value * 10000) / 100;
    return `${percentage}%`;
  }

  function labelsFormatter(value: number): string {
    if (timespan != 14) {
      return "";
    }
    return `${Math.round(value * 10000) / 100}%`;
  }

  function getTPDLineChartConfig(timespan: number): ChartConfiguration {
    const newRows = getTestedPerDayPercentChartRows($infectedIncreaseLog, timespan);
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
          value: tooltipValue,
        },
      },
      axis: {
        y: {
        tick: {
          format: labelsFormatter
        },
      },
      }
    });
  }

  $: if ($infectedIncreaseLog.length) {
    if (!chart) {
      chart = c3.generate(getTPDLineChartConfig(timespan));
    } else {
      const newRows = getTestedPerDayPercentChartRows($infectedIncreaseLog, timespan);
      // Replacing rows contens so tooltip formatter works correctly
      rows.splice(0, Infinity, ...newRows);
      chart.load({
        rows,
      });
    }
  }
</script>

<ChartLayout {id} {title} bind:timespan>
  <div id={`${id}_graph`} class:hideGraphPoints={timespan == -1}/>
</ChartLayout>
