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
              <a class="nav-link" href="#outcome-count">
                Výsledky ochorenia
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#tested-count">
                Počet testov
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#results-per-day">
                Výsledky testov za deň
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#by-location-table">
                Prehľad podľa obcí
              </a>
            </li>
          </ul>
        </div>
        <div class="col-md-9 col-12">
          <div>
            <InfectedLogChart id="infected-count" />
            <OutcomeChart id="outcome-count" />
            <TestedChart id="tested-count" />
            <InfectedIncreaseChart id="results-per-day" />
            <InfectedByLocationTable id="by-location-table" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import InfectedLogChart from "@/components/InfectedLogChart.vue";
import InfectedIncreaseChart from "@/components/TestsPerDayChart.vue";
import TestedChart from "@/components/TestedChart.vue";
import OutcomeChart from "@/components/OutcomeChart.vue";
import InfectedByLocationTable from "@/components/InfectedByLocationTable.vue";

@Component({
  components: {
    InfectedByLocationTable,
    OutcomeChart,
    TestedChart,
    InfectedIncreaseChart,
    InfectedLogChart
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
@import "~c3/c3.css";
@import "~bootstrap/scss/bootstrap";
@import "~bootstrap-vue/dist/bootstrap-vue.css";

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
