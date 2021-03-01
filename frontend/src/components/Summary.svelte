<script lang="ts">
  import { format } from "date-fns";
  import c3 from "c3";

  import {
    formatNumber,
    getSummaryValue,
    getChartConfig,
    getTooltipWithDeltaFormatter,
  } from "../utils";
  import { infectedLog } from "../store";
  import { InfectedLogDataKey, SubValueSummaryCard } from "../types";

  import type { SummaryValue } from "../types";
  import { ScrollableSection } from "@beyonk/svelte-scrollspy";
  import SubValueCard from "./SubValueCard.svelte"
  import type { ChartConfiguration, PrimitiveArray } from "c3";

  export let id: string = "";
  export const title: string = "";

  let medianCard: SummaryValue = {
    title: "Aktuálny kĺzavý medián",
    value: "",
    delta: "",
  };
  let simpleCards: SummaryValue[] = [];
  let hospitalizedCard: SubValueSummaryCard = {
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
      getSummaryValue(lastLogs, InfectedLogDataKey.INFECTED, "PCR pozitívnych"),
      getSummaryValue(lastLogs, InfectedLogDataKey.TESTS, "PCR testovaných"),
      getSummaryValue(
        lastLogs,
        InfectedLogDataKey.VACCINATED,
        "Očkovaných"
      ),
      getSummaryValue(lastLogs, InfectedLogDataKey.AG_POSITIVE, "Ag Pozitívnych"),
      getSummaryValue(lastLogs, InfectedLogDataKey.AG_TESTS, "Ag testovaných"),
      getSummaryValue(
        lastLogs,
        InfectedLogDataKey.VACCINATED_2ND_DOSE,
        "Očkovaných 2. dávkou:"
      ),
      getSummaryValue(lastLogs, InfectedLogDataKey.DEATHS, "Úmrtia"),
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
      <SubValueCard colClass="col-8" card="{hospitalizedCard}"/>
    </div>
  </ScrollableSection>
</div>
