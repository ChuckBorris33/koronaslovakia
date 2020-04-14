<template>
  <div class="chart">
    <div class="text-center pb-3">
      <h3>{{ title }}</h3>
    </div>
    <div class="text-right py-3">
      <BFormRadioGroup
        v-model="timespanValue"
        :options="options"
        buttons
        size="sm"
        button-variant="outline-primary"
      />
    </div>
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { BFormRadioGroup } from "bootstrap-vue";

@Component({
  components: {
    BFormRadioGroup
  }
})
export default class ChartLayout extends Vue {
  @Prop({ type: String, required: true })
  private title!: string;
  @Prop({ type: Number, required: true })
  private timespan!: number;

  private get timespanValue() {
    return this.timespan;
  }

  private set timespanValue(value) {
    this.$emit("update:timespan", value);
  }

  private options = [
    { text: "Všetko", value: -1 },
    { text: "Mesiac", value: 30 },
    { text: "Dva týždne", value: 14 }
  ];
}
</script>

<style lang="scss">
.chart {
  margin-bottom: 4em;
  min-height: 250px;
}
</style>
