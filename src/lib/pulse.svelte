<script>
// @ts-nocheck

    export let data = [];
    
    
    
</script>

<style>
    .graph {
        display: flex;
        align-items: flex-end;
        height: 200px;
        width: 100%;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
    }

    .bar {
        width: calc(100% / 200);
        background-color: #007bff;
    }
</style>

<div class="graph">
    {#each data as value (value)}
        <div class="bar" style="height: {value}%"></div>
    {/each}
</div>