<template>
  <div id="stats">
    <template v-if="dayStats">
      <DaySelect v-model="selectedDay" />
      <DayGraph
        :visitor-data="dayStats[selectedDayString] || []"
        :date-string="selectedDayString"
        :loading="loading"
      />
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import axios from "../axios";
import { formatISO } from "date-fns";

import DayGraph from "./DayGraph.vue";
import DaySelect from "./DaySelect.vue";

@Component({
  components: {
    DayGraph,
    DaySelect
  }
})
export default class Stats extends Vue {
  private dayStats: Record<
    string,
    { datetime: string; visitors: number }[]
  > = {};

  private selectedDay = new Date();
  private loading = false;

  private get selectedDayString(): string {
    return formatISO(this.selectedDay, { representation: "date" });
  }

  @Watch("selectedDayString", { immediate: true })
  private async loadSelectedDayData() {
    if (!this.dayStats[this.selectedDayString]) {
      this.loading = true;
      const visitors = await this.setDayStats(this.selectedDayString);
      this.dayStats = {
        ...this.dayStats,
        [this.selectedDayString]: visitors
      };
      this.loading = false;
    }
  }

  private async setDayStats(dateString: string) {
    const stats = await axios.get(`/visitor_per_day/?date=${dateString}`);
    return stats.data.results;
  }
}
</script>
