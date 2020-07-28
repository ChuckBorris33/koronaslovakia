<template>
  <div class="w-100 row">
    <div class="col-3 d-none d-md-block">
      <ul id="main-navigation" class="nav flex-column">
        <li v-for="(chart, index) in charts" class="nav-item" :key="chart.id">
          <a
            class="nav-link"
            :class="{ active: index === 0 }"
            :href="`#${chart.id}`"
          >
            {{ chart.title }}
          </a>
        </li>
      </ul>
    </div>
    <div class="col-md-9 col-12">
      <template v-for="chart in charts">
        <component
          :is="chart.component"
          :id="chart.id"
          :key="chart.id + '_chart'"
        />
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import InfectedLogChart from "@/components/InfectedLogChart.vue";
import OutcomeChart from "@/components/OutcomeChart.vue";
import TestedChart from "@/components/TestedChart.vue";
import InfectedByLocationTable from "@/components/InfectedByLocationTable.vue";
import TestsPerDayChart from "@/components/TestsPerDayChart.vue";
import { VueConstructor } from "vue";
import Summary from "@/components/Summary.vue";

@Component
export default class ChartList extends Vue {
  private get charts(): {
    title: string;
    component: VueConstructor<Vue>;
    id: string;
  }[] {
    return [
      {
        title: "Súhrn",
        component: Summary,
        id: "summary"
      },
      {
        title: "Počet nakazených",
        component: InfectedLogChart,
        id: "infected-count"
      },
      {
        title: "Výsledky ochorenia",
        component: OutcomeChart,
        id: "outcome-count"
      },
      {
        title: "Počet testov",
        component: TestedChart,
        id: "tested-count"
      },
      {
        title: "Výsledky testov za deň",
        component: TestsPerDayChart,
        id: "results-per-day"
      },
      {
        title: "Prehľad podľa okresov",
        component: InfectedByLocationTable,
        id: "by-location-table"
      }
    ];
  }
}
</script>
