<script>
    // @ts-nocheck
    import Component from "../lib/comp.svelte";
    import { onMount } from 'svelte';
    import Slot from "$lib/slot.svelte";
    // TEAM VIEW, QUERY ALL TEAM AVERAGES

    let fetch_array=[];
    let error;
    let render_now=0;

    // Function to get all the different teams.
    async function getAllTeams(){
        try{
            const response = await fetch(`http://localhost:5173/api/Team`)
            const res = await response.json()
             

            return res.result
        }
        catch(error){
            error=err.message
            console.error(error);
        }
    }



    // Function to fetch the average of a team
    async function fetchTeamAverage(tid) {
        try {
            const response = await fetch(`http://localhost:5173/api/TeamAverages?teamId=${tid}`); // Averages of team "tid"
            
        
            if (!response.ok) { 
                
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            
            let fetch_data = result.result; 

            fetch_array.push(fetch_data)
            
            //console.log("fetch_arraying:",fetch_array); // logs the correct value to send to custom slot component {reactionTime: 2687.25, redness: 141, pupils: 25003.75, heartBeats: 303.75, teamId: 12}

            
        } catch (err) {
            console.log("full stack error")
            error = err.message; 
        }
    }

    onMount(async () => {
        const team_array= await getAllTeams();
        //console.log("TR",team_array) // ARRAY OF IDS OF TEAMS
        for (const team of team_array){
		    const f = await fetchTeamAverage(team);
        }
        render_now=1
	});
    
</script>

<Component/>

{#if render_now}
{#each fetch_array as fetch_data} 
        <Slot title = {"Team "+ fetch_data.teamId + ":" + fetch_data.name} dataEntries = {fetch_data} />
{/each}
{:else}

<h1> LOADING... </h1>

{/if}




<section>


</section>




<style>
    
</style>