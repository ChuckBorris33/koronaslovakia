<script lang="ts">
  import Icon from "fa-svelte";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import ChartList from "./components/ChartList.svelte";
  import { ScrollSpy } from "@beyonk/svelte-scrollspy";
</script>

<svelte:head>
  <title>Korona</title>
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
</svelte:head>
<div class="navbar bg-primary">
  <div class="container grid-lg">
    <div class="columns px-2">
      <section class="navbar-section my-1">
        <a href="/" class="navbar-brand text-light">Koronavírus na slovensku</a>
      </section>
      <section class="navbar-section my-1">
        <a
          class="btn btn-link centered-icon text-light"
          href="https://github.com/ChuckBorris33/koronaslovakia">
          <Icon icon={faGithub} />
          <i class="fab fa-git" />
          <span class="text-assistive">Github</span>
        </a>
      </section>
    </div>
  </div>
</div>

<div class="container grid-lg main">
  <div class="px-2">
    <ScrollSpy>
      <ChartList />
    </ScrollSpy>
  </div>
</div>
