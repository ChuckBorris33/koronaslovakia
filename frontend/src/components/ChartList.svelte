<script lang="ts">
  import { Col, Nav, NavItem, NavLink, Row } from "sveltestrap";

  const charts: {
    title: string;
    component?: any;
    id: string;
  }[] = [
    {
      title: "Súhrn",
      id: "summary",
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
        <svelte:component this={chart.component} id={chart.id} />
      {/if}
    {/each}
  </Col>
</Row>
