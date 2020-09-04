<script lang="ts">
  import { Col, Nav, NavItem, NavLink, Row } from "sveltestrap";

  import {
    getInfectedChartRows,
    getOutcomeChartRows,
    getTestedChartRows,
  } from "../utils";
  import Summary from "./Summary.svelte";
  import LineChart from "./LineChart.svelte";
  import TestedPerDayChart from "./TestedPerDayChart.svelte";
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
      id: "by-location-table",
      title: "Prehľad podľa okresov",
    },
  ];
</script>

<div class="row chartsContainer">
  <Col sm="3" class="d-none d-md-block">
    <Nav id="main-navigation" vertical>
      {#each charts as chart, index}
        <NavItem>
          <NavLink class="nav-link" active={index === 0} href={`#${chart.id}`}>
            {chart.title}
          </NavLink>
        </NavItem>
      {/each}
    </Nav>
  </Col>
  <div class="col col-md-9 col-sm-12">
    <Summary {...charts[0]} />
    <LineChart {...charts[1]} chartDataGetter={getInfectedChartRows} />
    <LineChart {...charts[2]} chartDataGetter={getOutcomeChartRows} />
    <LineChart {...charts[3]} chartDataGetter={getTestedChartRows} />
    <TestedPerDayChart {...charts[4]} />
    <InfectedByLocationTable />
  </div>
</div>
