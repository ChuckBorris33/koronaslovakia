<template>
  <div id="app">
    <div class="container">
      <div class="center-screen">
        <div class="w-100">
          <h2 class="text-uppercase">Obsadenosť pertžalskej plavárne</h2>
          <Stats />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Stats from "./components/Stats.vue";

@Component({
  components: {
    Stats
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
@import "~c3/c3.css";
@import "~bootstrap/scss/bootstrap";

.container {
  max-width: 50em;
  min-height: 100vh;
}

.center-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100vh;
}
</style>
