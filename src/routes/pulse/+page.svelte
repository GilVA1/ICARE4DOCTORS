<script>
// @ts-nocheck

    import Pulse from "$lib/pulse.svelte";
    import { onMount } from 'svelte';

    let fetch_array = [];
    let physician = 77;

    let p_array = [];
    let pulseData = [];

    let render_pulses = 0;

    onMount(async () => { 
        const response = await fetch(`http://localhost:5173/api/HeartRate?id=${physician}`);
        const data = await response.json();
        fetch_array = data.ans;
        console.log("fetch", fetch_array);

        const p_response = await fetch(`http://localhost:5173/api/HeartRate`);
        p_array = await p_response.json() || [];
        p_array = p_array.ids;
        console.log("prayy", p_array);

        // Fetch HeartRate for each id in p_array
        for (let item of p_array) {
            const res = await fetch(`http://localhost:5173/api/HeartRate?id=${item}`);
            const pulseDataItem = await res.json();
            pulseData.push({ans:pulseDataItem.ans,id:item});
        }


        console.log("pulseData10001", pulseData);
        pulseData.reverse();
        render_pulses=1;
    });

</script>


{#if render_pulses}
    {#each pulseData as data}
        <h1> Pulse value for physician {data.id}</h1>
        <Pulse data={data.ans} />
    {/each}
{:else}
    <h1> Loading... </h1>
{/if}


