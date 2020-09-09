<script lang="ts">
  import _ from "lodash";
  import {
    faSortUp,
    faSortDown,
    faSort,
  } from "@fortawesome/free-solid-svg-icons";
  import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
  import Icon from "fa-svelte";
  import { lastLogByLocation } from "../store";
  import { getInfectedByLocationTableRows } from "../utils";
  import Pagination from "./Pagination.svelte";

  import type { TableColumn, LastLogByLocation } from "../types";

  let loading = false;
  let filter = "";
  let debouncedFilter = "";

  let limit = 10;
  let offset = 0;

  let rows: LastLogByLocation[] = [];
  let paginatedRows: LastLogByLocation[] = [];

  const columns: Record<string, TableColumn> = {
    location: {
      title: "Obec",
      sort: null,
    },
    infected: {
      title: "Nakazení",
      sort: "desc",
    },
    infected_delta: {
      title: "Rozdiel nakazených",
      sort: null,
    },
    last_updated: {
      title: "Posledný prípad",
      sort: null,
    },
  };

  function getSortIcon(columnKey: string): IconDefinition {
    switch (columns[columnKey].sort) {
      case "asc":
        return faSortUp;
      case "desc":
        return faSortDown;
      default:
        return faSort;
    }
  }

  function getSortIconClass(columnKey: string): string {
    if (columns[columnKey].sort === null) {
      return "text-muted";
    }
    return "";
  }

  function setSort(sortKey: string) {
    switch (columns[sortKey].sort) {
      case "desc":
        columns[sortKey].sort = "asc";
        break;
      case "asc":
        columns[sortKey].sort = "desc";
        break;
      default:
        for (const columnKey in columns) {
          columns[columnKey].sort = columnKey === sortKey ? "desc" : null;
        }
    }
  }

  function setFilter(value: string) {
    loading = true;
    filter = value;
    _.debounce(() => {
      debouncedFilter = filter;
      loading = false;
    }, 1000)();
    offset = 0;
  }

  $: if ($lastLogByLocation.length) {
    rows = getInfectedByLocationTableRows(
      $lastLogByLocation,
      columns,
      debouncedFilter
    );

    paginatedRows = [...rows].splice(offset, limit);
  }
</script>

<div class="chart">
  <div class="text-center pb-3">
    <h3>Prehľad podľa okresov</h3>
  </div>
  <div id="by-location-table">
    <div class="px-3">
      <form class="form">
        <div class="form-group row">
          <label for="infectedByLocationFilter" class="sr-only">Hľadať</label>
          <input
            id="infectedByLocationFilter"
            type="text"
            class="form-control col-md-4 col-sm-12"
            placeholder="Hľadať"
            readonly={false}
            on:input={(e) => setFilter(e.target.value)} />
          {#if loading}
            <div class="col-form-label pl-3 d-sm-none d-md-inline-block">
              <div
                role="status"
                class="spinner-border spinner-border-sm text-primary">
                <span class="sr-only">Hľadám...</span>
              </div>
            </div>
          {/if}
        </div>
      </form>
    </div>
  </div>
  <table class="table">
    <thead role="rowgroup">
      <tr>
        {#each Object.keys(columns) as key}
          <th>
            <div
              class="cursor-pointer d-flex justify-content-between"
              on:click={() => setSort(key)}>
              <div>{columns[key].title}</div>
              <div class={getSortIconClass(key)}>
                <Icon icon={getSortIcon(key)} />
              </div>
            </div>
          </th>
        {/each}
      </tr>
    </thead>
    <tbody role="rowgroup">
      {#each paginatedRows as row}
        <tr>
          {#each Object.keys(columns) as key}
            <td>
              <span>{row[key]}</span>
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
  <Pagination {limit} bind:offset length={rows.length} />
</div>
