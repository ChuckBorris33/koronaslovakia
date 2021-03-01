<script lang="ts">
  import {
    getInfectedChartRows,
    getVaccinatedChartRows,
    getOutcomeChartRows,
    getHospitalizedChartRows,
  } from "../utils";
  import Summary from "./Summary.svelte";
  import LineChart from "./LineChart.svelte";
  import TestedPerDayChart from "./TestedPerDayChart.svelte";
  import InfectedByLocationTable from "./InfectedByLocationTable.svelte";
  import { SectionHeader } from "@beyonk/svelte-scrollspy";
  import type { PrimitiveArray } from "c3";
  import type { InfectedLog } from "../types";

  const charts: {
    component: any;
    attributes: {
      id: string;
      title: string;
      chartDataGetter?: (
        logs: InfectedLog[],
        timespan: number
      ) => PrimitiveArray[];
    };
  }[] = [
    {
      component: Summary,
      attributes: {
        id: "summary",
        title: "Súhrn",
      },
    },
    {
      component: LineChart,
      attributes: {
        id: "infected-count",
        title: "Počet nakazených",
        chartDataGetter: getInfectedChartRows,
      },
    },
    {
      component: LineChart,
      attributes: {
        id: "vaccination-chart",
        title: "Počet zaočkovaných",
        chartDataGetter: getVaccinatedChartRows,
      },
    },
    {
      component: LineChart,
      attributes: {
        id: "hospitalization-chart",
        title: "Počet hospitalizovaných",
        chartDataGetter: getHospitalizedChartRows,
      },
    },
    {
      component: LineChart,
      attributes: {
        id: "outcome-count",
        title: "Úmrtia",
        chartDataGetter: getOutcomeChartRows,
      },
    },
    {
      component: TestedPerDayChart,
      attributes: {
        id: "infected-increase-chart",
        title: "Výsledky testov za deň",
      },
    },
    {
      component: InfectedByLocationTable,
      attributes: {
        id: "by-location-table",
        title: "Prehľad podľa okresov",
      },
    },
  ];
</script>

<div class="columns">
  <div class="hide-md column col-3">
    <ul class="nav" id="main-navigation">
      {#each charts as chart}
        <li class="nav-item">
          <SectionHeader id={chart.attributes.id}>
            <a class="text-primary" href={`#${chart.attributes.id}`}>
              {chart.attributes.title}
            </a>
          </SectionHeader>
        </li>
      {/each}
    </ul>
  </div>
  <div class="column col-9 col-md-12">
    {#each charts as chart}
      <svelte:component this={chart.component} {...chart.attributes} />
    {/each}
  </div>
</div>
