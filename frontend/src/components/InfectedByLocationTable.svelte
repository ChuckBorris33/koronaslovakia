<script lang="ts">
  import _ from "lodash";
  import {
    faSortUp,
    faSortDown,
    faSort,
  } from "@fortawesome/free-solid-svg-icons";
  import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
  import { ScrollableSection } from "@beyonk/svelte-scrollspy";
  import Icon from "fa-svelte";
  import { lastLogByLocation } from "../store";
  import { getInfectedByLocationTableRows } from "../utils";
  import Pagination from "./Pagination.svelte";

  import type { TableColumn, LastLogByLocation } from "../types";

  export let title: string;
  export let id: string;

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
      return "centered-icon text-muted";
    }
    return "centered-icon";
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
  <ScrollableSection {id}>
    <div class="text-center pb-2">
      <h3>{title}</h3>
    </div>
    <div>
      <div>
        <form class="form">
          <div class="form-group columns col-gapless py-2">
            <div class="column col-12 text-assistive">
              <label
                for="infectedByLocationFilter"
                class="form-inline">Hľadať</label>
            </div>
            <div class="column col-4 col-sm-12">
              <div class="has-icon-right">
                <input
                  id="infectedByLocationFilter"
                  type="text"
                  class="form-input"
                  placeholder="Hľadať"
                  readonly={false}
                  on:input={(e) => setFilter(e.target.value)} />
                {#if loading}
                  <i aria-hidden="true" class="form-icon loading" />
                {/if}
              </div>
            </div>
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
                class="d-flex c-hand justify-content-between"
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
              <td><span>{row[key]}</span></td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
    <Pagination {limit} bind:offset length={rows.length} />
  </ScrollableSection>
</div>
