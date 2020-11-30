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

  import type { SummaryValue } from "../types";
  import { ScrollableSection } from "@beyonk/svelte-scrollspy";
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

<div {id} class="summary">
  <ScrollableSection {id}>
    <div class="columns">
      <div class="column col-4 col-md-12 my-2">
        <div class="card h-100 text-center">
          <div class="card-header">
            <div class="card-title h6">{medianCard.title}</div>
          </div>
          <div class="card-body">
            <div class="card-content h-100">
              <h1 class="median d-inline">{medianCard.value}</h1>
              <small class="text-muted">{medianCard.delta}</small>
            </div>
          </div>
        </div>
      </div>
      <div class="column col-8 col-md-12 my-2">
        <div class="card h-100 text-center">
          <div class="card-header">
            <div class="card-title h6">Vývoj kĺzavého mediánu</div>
          </div>
          <div class="card-body">
            <div id="medianGraph" />
          </div>
        </div>
      </div>
    </div>
    <div class="columns">
      {#each simpleCards as card}
        <div class="column col-4 col-md-12 my-2">
          <div class="card h-100 text-center">
            <div class="card-header">
              <div class="card-title h6">{card.title}</div>
            </div>
            <div class="card-body">
              <div class="card-content h-100">
                <div>
                  <h3 class="d-inline">{card.value}</h3>
                  <small class="text-muted">{card.delta}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      {/each}
      <div class="column col-4 col-md-12 my-2">
        <div class="card h-100 text-center">
          <div class="card-header">
            <div class="card-title h6">{hospitalizedCard.main.title}</div>
          </div>
          <div class="card-body">
            <div class="card-content flex-column h-100">
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
  </ScrollableSection>
</div>
