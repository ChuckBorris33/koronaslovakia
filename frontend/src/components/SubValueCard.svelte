<div class="column col-4 col-md-12 my-2">
    <div class="card h-100 text-center">
        <div class="card-header">
        <div class="card-title h6">{card.main.title}</div>
        </div>
        <div class="card-body">
        <div class="card-content flex-column h-100">
            <div class="pb-2">
            <h4 class="d-inline">{card.main.value}</h4>
            <small class="text-muted">{card.main.delta}</small>
            </div>
            <table class="text-left">
            {#each card.subValues as value}
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
        </div>
    </div>
</div>

<script  lang="ts">
    import type { SubValueSummaryCard } from "../types"

    export let card: SubValueSummaryCard
</script>