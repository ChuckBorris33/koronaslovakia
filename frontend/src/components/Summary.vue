<template>
  <div class="summary">
    <BRow class="align-content-stretch">
      <BCol md="4" sm="12" class="mb-3">
        <BCard header="Aktuálny kĺzavý medián" align="center" class="h-100">
          <div
            v-if="this.infectedLog.length"
            class="d-flex align-items-center justify-content-center h-100"
          >
            <div>
              <h1 class="median d-inline">{{ lastLogs[0].median }}</h1>
              <small class="text-muted">
                {{
                  formatDelta(lastLogs[0].median - lastLogs[1].median)
                }}</small
              >
            </div>
          </div>
        </BCard>
      </BCol>
      <BCol md="8" sm="12" class="mb-3">
        <BCard header="Vývoj kĺzavého mediánu" align="center">
          <div id="medianGraph"></div>
        </BCard>
      </BCol>
    </BRow>
    <BRow class="align-content-stretch">
      <BCol v-for="(card, id) in cards" :key="id" md="4" sm="12" class="mb-3">
        <BCard :header="card.title" align="center" class="h-100">
          <div
            class="py-4 d-flex align-items-center justify-content-center h-100"
          >
            <div>
              <h3 class="d-inline">{{ card.value }}</h3>
              <small class="text-muted"> {{ card.delta }}</small>
            </div>
          </div>
        </BCard>
      </BCol>
      <BCol md="4" sm="12" class="mb-3">
        <BCard header="Hospitalizovaných" align="center" class="h-100">
          <div
            class="d-flex flex-column align-items-center justify-content-center h-100"
          >
            <div class="pb-2">
              <h4 class="d-inline">{{ hospitalizedData.hospitalized }}</h4>
              <small class="text-muted">
                {{ hospitalizedData.hospitalizedDelta }}</small
              >
            </div>
            <table class="text-left">
              <tr>
                <td class="pr-1">Potvrdený covid19:</td>
                <td>
                  {{ hospitalizedData.confirmedHospitalized
                  }}<small class="text-muted">{{
                    hospitalizedData.confirmedHospitalizedDelta
                  }}</small>
                </td>
              </tr>
              <tr>
                <td class="pr-1">Na JIS:</td>
                <td>
                  {{ hospitalizedData.confirmedHospitalizedIcu
                  }}<small class="text-muted">{{
                    hospitalizedData.confirmedHospitalizedIcuDelta
                  }}</small>
                </td>
              </tr>
              <tr>
                <td class="pr-1">Na pľúcnej ventilácií:</td>
                <td>
                  {{ hospitalizedData.confirmedHospitalizedVentilation
                  }}<small class="text-muted">{{
                    hospitalizedData.confirmedHospitalizedVentilationDelta
                  }}</small>
                </td>
              </tr>
            </table>
          </div>
        </BCard>
      </BCol>
    </BRow>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { fetchInfectedLog } from "@/api";
import { InfectedLog, InfectedLogDataKey } from "@/types";
import { BCard, BCol, BRow } from "bootstrap-vue";
import {
  formatNumber,
  getChartConfig,
  getTooltipWithDeltaFormatter,
} from "@/utils";
import c3, { ChartConfiguration, PrimitiveArray } from "c3";
import { format, subDays } from "date-fns";

const MEDIAN_GRAPH_DAYS = 8;

@Component({ components: { BRow, BCol, BCard } })
export default class Summary extends Vue {
  private infectedLog: InfectedLog[] = [];

  private get lastLogs() {
    if (!this.infectedLog.length) {
      return [];
    }
    return this.infectedLog.slice().reverse();
  }

  private get cards() {
    if (!this.lastLogs.length) {
      return [];
    }
    const lastLogs = this.lastLogs;
    return [
      {
        title: "Nakazených",
        value: formatNumber(lastLogs[0].infected),
        delta: this.formatDelta(lastLogs[0].infected - lastLogs[1].infected),
      },
      {
        title: "Testovaných",
        value: formatNumber(lastLogs[0].tests),
        delta: this.formatDelta(lastLogs[0].tests - lastLogs[1].tests),
      },
      {
        title: "Úmrtia",
        value: formatNumber(lastLogs[0].deaths),
        delta: this.formatDelta(lastLogs[0].deaths - lastLogs[1].deaths),
      },
      {
        title: "Vyliečení",
        value: formatNumber(lastLogs[0].cured),
        delta: this.formatDelta(lastLogs[0].cured - lastLogs[1].cured),
      },
      {
        title: "Aktívnych",
        value: formatNumber(this.getActive(0)),
        delta: this.formatDelta(this.getActive(0) - this.getActive(1)),
      },
    ];
  }

  private get hospitalizedData() {
    if (!this.lastLogs.length) {
      return {};
    }
    return {
      hospitalized: formatNumber(this.lastLogs[0].hospitalized),
      hospitalizedDelta: this.formatDelta(
        this.lastLogs[0].hospitalized - this.lastLogs[1].hospitalized
      ),
      confirmedHospitalized: formatNumber(
        this.lastLogs[0].confirmed_hospitalized
      ),
      confirmedHospitalizedDelta: this.formatDelta(
        this.lastLogs[0].confirmed_hospitalized -
          this.lastLogs[1].confirmed_hospitalized
      ),
      confirmedHospitalizedIcu: formatNumber(
        this.lastLogs[0].confirmed_hospitalized_icu
      ),
      confirmedHospitalizedIcuDelta: this.formatDelta(
        this.lastLogs[0].confirmed_hospitalized_icu -
          this.lastLogs[1].confirmed_hospitalized_icu
      ),
      confirmedHospitalizedVentilation: formatNumber(
        this.lastLogs[0].confirmed_hospitalized_ventilation
      ),
      confirmedHospitalizedVentilationDelta: this.formatDelta(
        this.lastLogs[0].confirmed_hospitalized_ventilation -
          this.lastLogs[1].confirmed_hospitalized_ventilation
      ),
    };
  }

  private formatDelta(value: number): string {
    if (value == 0) {
      return "";
    }
    const formattedValue = formatNumber(value);
    return value > 0 ? `(+${formattedValue})` : `(${formattedValue})`;
  }

  async mounted() {
    const fetchResult = await fetchInfectedLog();
    this.infectedLog = fetchResult?.data?.results || [];
    c3.generate(this.chartConfig);
  }

  private getActive(id: number) {
    if (!this.lastLogs.length) {
      return 0;
    }
    const log = this.lastLogs[id];
    if (log) {
      return log.infected - log.deaths - log.cured;
    }
    return 0;
  }

  private get chartConfig(): ChartConfiguration {
    const rows = [["Dátum", "Medián"], ...this.chartDataRows];
    return getChartConfig(
      {
        bindto: "#medianGraph",
        data: {
          rows,
        },
        tooltip: {
          format: {
            value: getTooltipWithDeltaFormatter(rows),
          },
        },
        legend: {
          show: false,
        },
        size: {
          height: 200,
        },
      },
      MEDIAN_GRAPH_DAYS
    );
  }

  private get chartDataRows(): PrimitiveArray[] {
    return this.infectedLog
      .filter((item) => {
        const date = new Date(item.date);
        const from = subDays(new Date(), MEDIAN_GRAPH_DAYS);
        return date > from;
      })
      .map((item) => {
        const date = new Date(item.date);
        const dateString: string = format(date, "yyyy-MM-dd");
        return [dateString, item[InfectedLogDataKey.MEDIAN]];
      });
  }
}
</script>

<style lang="scss">
.summary {
  margin-bottom: 4em;
  min-height: 250px;
}

.median {
  font-size: 5em;
}

#medianGraph {
  max-height: 200px;
}
</style>
