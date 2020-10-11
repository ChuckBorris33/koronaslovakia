<script lang="ts">
  import { format } from "date-fns";
  import c3 from "c3";

  import {
    formatNumber,
    getSummaryValue,
    getActiveSummaryValue,
    getChartConfig,
    getTooltipWithDeltaFormatter,
  } from "../utils";
  import { infectedLog } from "../store";
  import { InfectedLogDataKey } from "../types";

  import type { SummaryValue, InfectedLog } from "../types";
  import type { ChartConfiguration, PrimitiveArray } from "c3";

  export let id: string = "";
  export const title: string = "";

  let medianCard: SummaryValue = {
    title: "Aktuálny kĺzavý medián",
    value: "",
    delta: "",
  };
  let simpleCards: SummaryValue[] = [];
  let hospitalizedCard: { main: SummaryValue; subValues: SummaryValue[] } = {
    main: { title: "Hospitalizovaných", value: "", delta: "" },
    subValues: [],
  };

  function getChartDataRows(): PrimitiveArray[] {
    return $infectedLog.slice(-7).map((item) => {
      const date = new Date(item.date);
      const dateString: string = format(date, "yyyy-MM-dd");
      return [dateString, item[InfectedLogDataKey.MEDIAN]];
    });
  }

  function getMedianChartConfig(): ChartConfiguration {
    const rows = [["Dátum", "Medián"], ...getChartDataRows()];
    return getChartConfig({
      bindto: "#medianGraph",
      data: {
        rows,
        labels: { format: formatNumber },
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
    });
  }

  $: lastLogs = $infectedLog.slice().reverse();

  $: if (lastLogs.length) {
    simpleCards = [
      getSummaryValue(lastLogs, InfectedLogDataKey.INFECTED, "Nakazených"),
      getSummaryValue(lastLogs, InfectedLogDataKey.TESTS, "Testovaných"),
      getSummaryValue(lastLogs, InfectedLogDataKey.DEATHS, "Úmrtia"),
      getSummaryValue(lastLogs, InfectedLogDataKey.CURED, "Vyliečení"),
      getActiveSummaryValue(lastLogs),
    ];
    hospitalizedCard = {
      main: getSummaryValue(
        lastLogs,
        InfectedLogDataKey.HOSPITALIZED,
        "Hospitalizovaných"
      ),
      subValues: [
        getSummaryValue(
          lastLogs,
          InfectedLogDataKey.CONFIRMED_HOSPITALIZED,
          "Potvrdený covid19:"
        ),
        getSummaryValue(
          lastLogs,
          InfectedLogDataKey.CONFIRMED_HOSPITALIZED_ICU,
          "Na JIS:"
        ),
        getSummaryValue(
          lastLogs,
          InfectedLogDataKey.CONFIRMED_HOSPITALIZED_VENTILATION,
          "Na ventilácií:"
        ),
      ],
    };
    medianCard = getSummaryValue(
      lastLogs,
      InfectedLogDataKey.MEDIAN,
      "Aktuálny kĺzavý medián"
    );

    c3.generate(getMedianChartConfig());
  }
</script>

<style lang="scss">
  .summary {
    margin-bottom: 4em;
    min-height: 250px;
  }
</style>

<div {id} class="summary">
  <div class="row align-content-stretch">
    <div class="col col-md-4 col-sm-12 mb-3">
      <div class="card h-100 text-center">
        <div class="card-header">
          <div class="card-title m-0">{medianCard.title}</div>
        </div>
        <div class="card-body">
          <div class="d-flex align-items-center justify-content-center h-100">
            <div>
              <h1 class="median d-inline">{medianCard.value}</h1>
              <small class="text-muted">{medianCard.delta}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col col-md-8 col-sm-12 mb-3">
      <div class="card h-100 text-center">
        <div class="card-header">
          <div class="card-title m-0">Vývoj kĺzavého mediánu</div>
        </div>
        <div class="card-body">
          <div id="medianGraph" />
        </div>
      </div>
    </div>
  </div>
  <div class="row align-content-stretch">
    {#each simpleCards as card}
      <div class="col col-md-4 col-sm-12 mb-3">
        <div class="card h-100 text-center">
          <div class="card-header">
            <div class="card-title m-0">{card.title}</div>
          </div>
          <div class="card-body">
            <div
              class="py-4 d-flex align-items-center justify-content-center h-100">
              <div>
                <h3 class="d-inline">{card.value}</h3>
                <small class="text-muted">{card.delta}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    {/each}
    <div class="col col-md-4 col-sm-12 mb-3">
      <div class="card h-100 text-center">
        <div class="card-header">
          <div class="card-title m-0">{hospitalizedCard.main.title}</div>
        </div>
        <div class="card-body">
          <div
            class="d-flex flex-column align-items-center justify-content-center
            h-100">
            <div class="pb-2">
              <h4 class="d-inline">{hospitalizedCard.main.value}</h4>
              <small class="text-muted">{hospitalizedCard.main.delta}</small>
            </div>
            <table class="text-left">
              {#each hospitalizedCard.subValues as value}
                <tr>
                  <td class="pr-1">{value.title}</td>
                  <td>
                    {value.value}
                    <small class="text-muted">{value.delta}</small>
                  </td>
                </tr>
              {/each}
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
