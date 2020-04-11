<template>
  <div id="app">
    <div class="container">
      <div class="text-center title">
        <h1 class="text-uppercase">Koronavírus na slovensku</h1>
      </div>
      <ChartList />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ChartList from "@/components/ChartList.vue";

@Component({
  components: {
    ChartList
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
