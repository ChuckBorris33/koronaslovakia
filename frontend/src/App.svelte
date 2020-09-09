<script lang="ts">
  import Icon from "fa-svelte";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import ChartList from "./components/ChartList.svelte";
</script>

<svelte:head>
  <title>Korona</title>
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
</svelte:head>
<div class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container">
    <a href="#" class="navbar-brand">Koronavírus na slovensku</a>
    <ul class="navbar-nav ml-auto">
      <li class="nav-item">
        <a
          class="nav-link"
          href="https://github.com/ChuckBorris33/koronaslovakia">
          <Icon icon={faGithub} />
          <span class="sr-only">Github</span>
        </a>
      </li>
    </ul>
  </div>
</div>
<div class="container main">
  <ChartList />
</div>
