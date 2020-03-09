<template>
  <div class="d-flex my-4 btn-group">
    <button
      class="btn flex-grow-1 btn-outline-primary"
      @click="selectDay(dates[selectedIndex - 1].date)"
    >
      &lt;
    </button>
    <button
      v-for="day in dates"
      :key="day.dateString"
      class="btn flex-grow-1"
      :class="{
        'btn-primary': day.active,
        'btn-outline-primary': !day.active
      }"
      @click="selectDay(day.date)"
    >
      {{ day.dayOfWeek }}<br />
      {{ day.dateString }}
    </button>
    <button
      class="btn flex-grow-1 btn-outline-primary"
      @click="selectDay(dates[selectedIndex + 1].date)"
      :disabled="selectedIndex === 6"
    >
      &gt;
    </button>
  </div>
</template>

<script lang="ts">
import { Component, Model, Vue } from "vue-property-decorator";

import { differenceInCalendarDays, addDays, getDay, format } from "date-fns";

@Component
export default class DaySelect extends Vue {
  @Model("selectDay", { type: Date, required: true })
  private readonly selectedDay!: Date;

  private dayToStringMap: string[] = [
    "NE.",
    "PO.",
    "UT.",
    "ST.",
    "ŠT.",
    "PIA.",
    "SO."
  ];

  private selectDay(newDate: Date) {
    this.$emit("selectDay", newDate);
  }

  private nextDay() {
    this.selectDay(addDays(this.selectedDay, 1))
  }

  private prevDay() {
    this.selectDay(addDays(this.selectedDay, 1))
  }


  private get selectedIndex(): number {
    const daysToToday: number = differenceInCalendarDays(
      new Date(),
      this.selectedDay
    );
    return daysToToday < 3 ? 6 - daysToToday : 3;
  }

  private get dates(): {
    dayOfWeek: string;
    dateString: string;
    date: Date;
    active: boolean;
  }[] {
    const startDate = addDays(this.selectedDay, -1 * this.selectedIndex);
    const dates = [];
    for (let dayOffset = 0; dayOffset < 7; dayOffset++) {
      const date = addDays(startDate, dayOffset);
      dates.push({
        dayOfWeek: this.dayToStringMap[getDay(date)],
        dateString: format(date, "d.L."),
        date,
        active: dayOffset == this.selectedIndex
      });
    }
    return dates;
  }
}
</script>
