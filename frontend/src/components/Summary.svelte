<script lang="ts">
  import { Card, CardBody, CardHeader, CardTitle, Col, Row } from "sveltestrap";
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
  export let title: string = "";

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

  function getChartDataRows(lastLogs: InfectedLog[]): PrimitiveArray[] {
    return lastLogs.slice(0, 7).map((item) => {
      const date = new Date(item.date);
      const dateString: string = format(date, "yyyy-MM-dd");
      return [dateString, item[InfectedLogDataKey.MEDIAN]];
    });
  }

  function getMedianChartConfig(lastLogs: InfectedLog[]): ChartConfiguration {
    const rows = [["Dátum", "Medián"], ...getChartDataRows(lastLogs)];
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
          InfectedLogDataKey.HOSPITALIZED,
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

    c3.generate(getMedianChartConfig(lastLogs));
  }
</script>

<style lang="scss">
  .summary {
    margin-bottom: 4em;
    min-height: 250px;
  }
</style>

<div {id} class="summary">
  <Row class="align-content-stretch">
    <Col md="4" sm="12" class="mb-3">
      <Card class="h-100 text-center">
        <CardHeader>
          <CardTitle class="m-0">{medianCard.title}</CardTitle>
        </CardHeader>
        <CardBody>
          <div class="d-flex align-items-center justify-content-center h-100">
            <div>
              <h1 class="median d-inline">{medianCard.value}</h1>
              <small class="text-muted">{medianCard.delta}</small>
            </div>
          </div>
        </CardBody>
      </Card>
    </Col>
    <Col md="8" sm="12" class="mb-3">
      <Card class="h-100 text-center">
        <CardHeader>
          <CardTitle class="m-0">Vývoj kĺzavého mediánu</CardTitle>
        </CardHeader>
        <CardBody>
          <div id="medianGraph" />
        </CardBody>
      </Card>
    </Col>
  </Row>
  <Row class="align-content-stretch">
    {#each simpleCards as card, index}
      <Col md="4" sm="12" class="mb-3">
        <Card class="h-100 text-center">
          <CardHeader>
            <CardTitle class="m-0">{card.title}</CardTitle>
          </CardHeader>
          <CardBody>
            <div
              class="py-4 d-flex align-items-center justify-content-center h-100">
              <div>
                <h3 class="d-inline">{card.value}</h3>
                <small class="text-muted">{card.delta}</small>
              </div>
            </div>
          </CardBody>
        </Card>
      </Col>
    {/each}
    <Col md="4" sm="12" class="mb-3">
      <Card class="h-100 text-center">
        <CardHeader>
          <CardTitle class="m-0">{hospitalizedCard.main.title}</CardTitle>
        </CardHeader>
        <CardBody>
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
        </CardBody>
      </Card>
    </Col>
  </Row>
</div>
