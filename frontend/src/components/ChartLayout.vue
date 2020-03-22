<template functional>
  <div class="chart">
    <div class="text-center pb-3">
      <h3>{{ props.title }}</h3>
    </div>
    <slot></slot>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class ChartLayout extends Vue {
  @Prop({ type: String, required: true })
  private title!: string;
}
</script>

<style lang="scss">
.chart {
  margin-bottom: 4em;
  min-height: 250px;
}
</style>
