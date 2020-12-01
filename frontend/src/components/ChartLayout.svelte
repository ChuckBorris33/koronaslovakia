<script lang="ts">
  import { ScrollableSection } from "@beyonk/svelte-scrollspy";

  export let id: string;
  export let title: string;
  export let timespan: number;

  const options = [
    { text: "Všetko", value: -1 },
    { text: "Mesiac", value: 30 },
    { text: "Dva týždne", value: 14 },
  ];
</script>

<div class="chart">
  <ScrollableSection {id}>
    <div class="text-center">
      <h3>{title}</h3>
    </div>
    <div class="text-right py-2">
      <div
        role="radiogroup"
        tabindex="-1"
        class="btn-group"
        id={`timespan_options_${id}`}>
        {#each options as option, index}
          <button
            class="btn btn-sm btn-no-focus"
            class:active={option.value === timespan}
            on:click={() => {
              timespan = option.value;
            }}>
            <span>{option.text}</span>
          </button>
        {/each}
      </div>
    </div>
    <slot />
  </ScrollableSection>
</div>
