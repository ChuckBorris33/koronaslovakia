<template>
  <div id="app">
    <BNavbar toggleable="lg" class="navbar-dark bg-primary">
      <div class="container">
        <BNavbarBrand href="#">Koronavírus na slovensku</BNavbarBrand>
        <BNavbarNav class="ml-auto">
          <BNavItem
            href="https://github.com/ChuckBorris33/koronaslovakia"
            alt="Source"
          >
            <i class="fab fa-github"></i>
          </BNavItem>
        </BNavbarNav>
      </div>
    </BNavbar>
    <div class="container main">
      <ChartList />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ChartList from "@/components/ChartList.vue";
import { BNavbar, BNavbarBrand, BNavbarNav, BNavItem } from "bootstrap-vue";

@Component({
  components: {
    ChartList,
    BNavbar,
    BNavbarBrand,
    BNavbarNav,
    BNavItem
  }
})
export default class App extends Vue {}
</script>

<style lang="scss">
@import "~c3/c3.css";

$primary: #2d7dd2;
$body-color: #303036;

@import "~bootstrap/scss/bootstrap";
@import "~bootstrap-vue/dist/bootstrap-vue.css";

@import "~@fortawesome/fontawesome-free/css/all.css";

.main {
  padding-top: 4em;
}

#main-navigation {
  position: fixed;

  .active {
    font-weight: bold;
  }
}
</style>
