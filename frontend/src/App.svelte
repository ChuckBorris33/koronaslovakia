<script lang="ts">
  import {
    Container,
    Navbar,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
  } from "sveltestrap";
  import Icon from "fa-svelte";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import ChartList from "./components/ChartList.svelte";
</script>

<svelte:head>
  <title>Korona</title>
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
</svelte:head>
<Navbar toggleable="lg" class="navbar-dark bg-primary">
  <Container>
    <NavbarBrand href="#">Koronavírus na slovensku</NavbarBrand>
    <Nav class="ml-auto" navbar>
      <NavItem>
        <NavLink href="https://github.com/ChuckBorris33/koronaslovakia">
          <Icon icon={faGithub} />
        </NavLink>
      </NavItem>
    </Nav>
  </Container>
</Navbar>
<Container class="main">
  <ChartList />
</Container>
