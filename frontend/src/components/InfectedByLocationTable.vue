<template>
  <ChartLayout title="Prehľad podľa obcí">
    <BTable
      :fields="fields"
      :items="items"
      :sort-by.sync="sortBy"
      :sort-desc.sync="sortDesc"
      :per-page="perPage"
      :current-page="page"
    />
    <BPagination
      v-model="page"
      :per-page="perPage"
      :total-rows="data.length"
      align="right"
    />
  </ChartLayout>
</template>

<script lang="ts">
import { Vue, Component } from "vue-property-decorator";
import { fetchLastLogByLocation } from "@/api";
import { LastLogByLocation } from "@/types";
import { BTable, BPagination, BvTableFieldArray } from "bootstrap-vue";
import ChartLayout from "@/components/ChartLayout.vue";
import { format } from "date-fns";

@Component({
  components: {
    ChartLayout,
    BTable,
    BPagination
  }
})
export default class InfectedByLocationTable extends Vue {
  private data: LastLogByLocation[] = [];
  private sortBy = "infected";
  private sortDesc = true;

  private perPage = 10;
  private page = 1;

  private orderBy: { column: string; direction: "asc" | "desc" } = {
    column: "infected",
    direction: "desc"
  };
  private get fields(): BvTableFieldArray {
    return [
      {
        key: "location",
        label: "Obec",
        sortable: true
      },
      {
        key: "infected",
        label: "Nakazení",
        sortable: true,
        formatter: this.logItemFormatter
      },
      {
        key: "cured",
        label: "Vyliečení",
        sortable: true,
        formatter: this.logItemFormatter
      },
      {
        key: "deaths",
        label: "Úmrtia",
        sortable: true,
        formatter: this.logItemFormatter
      },
      {
        key: "last_updated",
        label: "Posledný prípad",
        sortable: true,
        formatter: value => {
          const date = new Date(value);
          return format(date, "d.M.yyyy");
        }
      }
    ];
  }

  private logItemFormatter(value: number, key: string, item: any): string {
    const deltaKey = `${key}_delta`;
    if (!item[deltaKey]) {
      return String(value);
    }
    return `${value} (+${item[deltaKey]})`;
  }

  private get items() {
    return this.data;
  }

  async mounted() {
    const fetchResult = await fetchLastLogByLocation();
    this.data = fetchResult?.data?.results || [];
  }
}
</script>

<style scoped></style>
