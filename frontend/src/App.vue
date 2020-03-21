<template>
  <div id="app">
    <div class="container">
      <div class="text-center title">
        <h1 class="text-uppercase">Koronavírus na slovensku</h1>
      </div>
      <div class="w-100 row">
        <div class="col-3 d-none d-md-block">
          <ul id="main-navigation" class="nav flex-column">
            <li class="nav-item">
              <a class="nav-link active" href="#infected-count">
                Počet nakazených
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#tested-count">
                Počet testov
              </a>
            </li>
          </ul>
        </div>
        <div class="col-md-9 col-12">
          <div>
            <InfectedLogChart
              id="infected-count"
              graph-id="cases-over-time-chart"
              title="Počet nakazených"
              data-key="infected"
            />
            <InfectedLogChart
              id="tested-count"
              graph-id="tested-over-time-chart"
              title="Počet testov"
              data-key="tests"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import InfectedLogChart from "@/components/InfectedLogChart.vue";

@Component({
  components: {
    InfectedLogChart
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
@import "~c3/c3.css";
@import "~bootstrap/scss/bootstrap";

.title {
  padding-top: 4em;
  padding-bottom: 4em;
}

#main-navigation {
  position: fixed;

  .active {
    font-weight: bold;
  }
}
</style>
