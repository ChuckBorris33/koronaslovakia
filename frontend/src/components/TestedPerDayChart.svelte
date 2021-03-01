<script lang="ts">
  import c3, { ChartConfiguration, ChartAPI, PrimitiveArray } from "c3";

  import {
    formatNumber,
    getChartConfig,
    getTestedPerDayChartRows,
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
    if (id == "Percento pozitívnych") {
      const percentage = Math.round(value * 10000) / 100;
      return `${percentage}%`;
    }
    return String(value);
  }

  function formatPercent(value: number): string {
    return `${Math.round(value * 10000) / 100}%`;
  }

  function labelsFormatter(value: number, id: string): string {
    if (id == "Percento pozitívnych") {
      if (timespan != 14) {
        return "";
      }
      return formatPercent(value);
    }
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
      bindto: `#${id}_graph`,
      data: {
        type: "bar",
        types: {
          "Percento pozitívnych": "line",
        },
        axes: {
          "Percento pozitívnych": "y2",
          Pozitívne: "y",
          Negatívne: "y",
        },
        colors: {
          "Percento pozitívnych": "#5f8103",
          Pozitívne: "#2D7DD2",
          Negatívne: "#EA7317",
        },
        rows,
        labels: { format: labelsFormatter },
        groups: [["Pozitívne", "Negatívne"], ["Percento pozitívnych"]],
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
        y2: {
          show: true,
          min: 0,
          padding: {
            bottom: 0,
          },
          tick: {
            format: formatPercent,
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
  <div id={`${id}_graph`} class:hideGraphPoints={timespan == -1} />
</ChartLayout>
