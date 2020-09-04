<script lang="ts">
  import { each } from "svelte/internal";

  export let id: string;
  export let title: string;
  export let timespan: number;

  const options = [
    { text: "Všetko", value: -1 },
    { text: "Mesiac", value: 30 },
    { text: "Dva týždne", value: 14 },
  ];
</script>

<style lang="scss">
  .chart {
    margin-bottom: 4em;
    min-height: 250px;
  }

  .btn-group-toggle:focus {
    outline: none;
  }
</style>

<div class="chart" {id}>
  <div class="text-center pb-3">
    <h3>{title}</h3>
  </div>
  <div class="text-right py-3">
    <div
      role="radiogroup"
      tabindex="-1"
      class="btn-group-toggle btn-group btn-group-sm bv-no-focus-ring"
      id={`timespan_options_${id}`}>
      {#each options as option, index}
        <label
          class={`btn btn-sm ${option.value === timespan ? 'btn-primary' : 'btn-outline-primary'}`}
          on:click={() => {
            timespan = option.value;
          }}>
          <input
            type="radio"
            autocomplete="off"
            value={option.value}
            id={`timespan_options_${index}_${id}`}
            name={`timespan_options_${index}_${id}`} />
          <span>{option.text}</span>
        </label>
      {/each}
    </div>
  </div>
  <slot />
</div>
