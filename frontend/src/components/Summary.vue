<template>
  <div class="summary">
    <BRow>
      <BCol v-for="(card, id) in cards" :key="id" md="6" sm="12" class="mb-3">
        <BCard :header="card.title" align="center">
          <div class="py-4">
            <h3 class="d-inline">{{ card.value }}</h3>
            <small class="text-muted"> {{ card.delta }}</small>
          </div>
        </BCard>
      </BCol>
    </BRow>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { fetchInfectedLog } from "@/api";
import { InfectedLog } from "@/types";
import { BCard, BCol, BRow } from "bootstrap-vue";

@Component({ components: { BRow, BCol, BCard } })
export default class Summary extends Vue {
  private infectedLog: InfectedLog[] = [];

  private get cards() {
    if (!this.infectedLog.length) {
      return [];
    }
    const lastLogs = this.infectedLog.slice().reverse();
    return [
      {
        title: "Nakazených",
        value: lastLogs[0].infected,
        delta: this.formatDelta(lastLogs[0].infected - lastLogs[1].infected)
      },
      {
        title: "Testovaných",
        value: lastLogs[0].tests,
        delta: this.formatDelta(lastLogs[0].tests - lastLogs[1].tests)
      },
      {
        title: "Úmrtia",
        value: lastLogs[0].deaths,
        delta: this.formatDelta(lastLogs[0].deaths - lastLogs[1].deaths)
      },
      {
        title: "Vyliečení",
        value: lastLogs[0].cured,
        delta: this.formatDelta(lastLogs[0].cured - lastLogs[1].cured)
      }
    ];
  }

  private formatDelta(value: number): string {
    if (value == 0) {
      return "";
    }
    return value > 0 ? `(+${value})` : `(${value})`;
  }

  async mounted() {
    const fetchResult = await fetchInfectedLog();
    this.infectedLog = fetchResult?.data?.results || [];
  }
}
</script>

<style lang="scss">
.summary {
  margin-bottom: 4em;
  min-height: 250px;
}
</style>
