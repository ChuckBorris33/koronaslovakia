<script lang="ts">
  import { Col, Nav, NavItem, NavLink, Row } from "sveltestrap";

  import { getInfectedChartRows, getOutcomeChartRows } from "../utils";
  import Summary from "./Summary.svelte";
  import BasicLineChart from "./BasicLineChart.svelte";
  import type { SvelteComponent } from "svelte";

  const charts: {
    id: string;
    title: string;
    component: SvelteComponent;
    otherProps?: Record<string, any>;
  }[] = [
    {
      id: "summary",
      title: "Súhrn",
      component: Summary,
    },
    {
      id: "infected-count",
      title: "Počet nakazených",
      component: BasicLineChart,
      otherProps: {
        chartDataGetter: getInfectedChartRows,
      },
    },
    {
      id: "outcome-count",
      title: "Výsledky ochorenia",
      component: BasicLineChart,
      otherProps: {
        chartDataGetter: getOutcomeChartRows,
      },
    },
  ];
</script>

<Row class="w-100">
  <Col xs="3" class="d-none d-md-block">
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
  <Col md="9" xs="12">
    {#each charts as chart}
      {#if chart.component}
        <svelte:component
          this={chart.component}
          id={chart.id}
          title={chart.title}
          {...chart.otherProps || {}} />
      {/if}
    {/each}
  </Col>
</Row>
