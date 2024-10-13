<script>
// @ts-nocheck


import { onMount } from "svelte";
import Slot from "$lib/slot.svelte";

    let render_now=0;
    let doctors=[];

    async function getAllDoctors(){
        const res =await fetch("http://localhost:5173/api/Doctor")
        const res2 = await res.json();
        console.log(res2)
        return res2.result // LIST OF DOCTOR JSONS
    }


onMount(async () =>{
    doctors = await getAllDoctors()
    console.log("DOCTORS",doctors);
    render_now=1;
})

</script>

<h1>Individual values for each doctor</h1>

{#if render_now}
{#each doctors as doc} 
        
        <Slot title = {doc._id} dataEntries = {doc} />
{/each}
{:else}

<h1> LOADING... </h1>

{/if}