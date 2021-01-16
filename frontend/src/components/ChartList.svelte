<script lang="ts">
  import {
    getInfectedChartRows,
    getOutcomeChartRows,
    getTestedChartRows,
  } from "../utils";
  import Summary from "./Summary.svelte";
  import LineChart from "./LineChart.svelte";
  import TestedPerDayChart from "./TestedPerDayChart.svelte";
  import TestedPercentageChart from "./TestedPercentageChart.svelte";
  import InfectedByLocationTable from "./InfectedByLocationTable.svelte";
  import { SectionHeader } from "@beyonk/svelte-scrollspy";

  const charts: {
    id: string;
    title: string;
  }[] = [
    {
      id: "summary",
      title: "Súhrn",
    },
    {
      id: "infected-count",
      title: "Počet nakazených",
    },
    {
      id: "outcome-count",
      title: "Výsledky ochorenia",
    },
    {
      id: "infected-increase-chart",
      title: "Výsledky testov za deň",
    },
    {
      id: "by-location-table",
      title: "Prehľad podľa okresov",
    },
  ];
</script>

<div class="columns">
  <div class="hide-md column col-3">
    <ul class="nav" id="main-navigation">
      {#each charts as chart}
        <li class="nav-item">
          <SectionHeader id={chart.id}>
            <a class="text-primary" href={`#${chart.id}`}> {chart.title} </a>
          </SectionHeader>
        </li>
      {/each}
    </ul>
  </div>
  <div class="column col-9 col-md-12">
    <Summary {...charts[0]} />
    <LineChart {...charts[1]} chartDataGetter={getInfectedChartRows} />
    <LineChart {...charts[2]} chartDataGetter={getOutcomeChartRows} />
    <LineChart {...charts[3]} chartDataGetter={getTestedChartRows} />
    <TestedPerDayChart {...charts[4]} />
    <TestedPercentageChart {...charts[5]} />
    <InfectedByLocationTable {...charts[6]} />
  </div>
</div>
