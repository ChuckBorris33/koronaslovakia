<script lang="ts">
  import {
    getInfectedChartRows,
    getOutcomeChartRows,
    getTestedChartRows,
  } from "../utils";
  import Summary from "./Summary.svelte";
  import LineChart from "./LineChart.svelte";
  import TestedPerDayChart from "./TestedPerDayChart.svelte";
  import TestedPerDayPositivePercentLineChart from "./TestedPerDayPositivePercentLineChart.svelte";
  import InfectedByLocationTable from "./InfectedByLocationTable.svelte";

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
      id: "tested-count",
      title: "Počet testov",
    },
    {
      id: "infected-increase-chart",
      title: "Výsledky testov za deň",
    },
    {
      id: "infected-percent-increase-chart",
      title: "Počty pozitívnych k testovaným"
    },
    {
      id: "by-location-table",
      title: "Prehľad podľa okresov",
    },
  ];
</script>

<div class="row">
  <div class="col com-md-3 d-none d-md-block">
    <ul class="nav flex-column" id="main-navigation">
      {#each charts as chart, index}
        <li class="nav-item">
          <a class="nav-link" class:active={index === 0} href={`#${chart.id}`}>
            {chart.title}
          </a>
        </li>
      {/each}
    </ul>
  </div>
  <div class="col col-md-9 col-sm-12">
    <Summary {...charts[0]} />
    <LineChart {...charts[1]} chartDataGetter={getInfectedChartRows} />
    <LineChart {...charts[2]} chartDataGetter={getOutcomeChartRows} />
    <LineChart {...charts[3]} chartDataGetter={getTestedChartRows} />
    <TestedPerDayChart {...charts[4]} />
    <TestedPerDayPositivePercentLineChart {...charts[5]} />
    <InfectedByLocationTable />
  </div>
</div>
