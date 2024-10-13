<script>
// @ts-nocheck

    export let title;

    export let dataEntries={};
    
    let dataArray = Object.entries(dataEntries);


</script>

<div class="slot-container">


    <h2> {title} </h2>

    <ul class="data-list">
        {#each dataArray as [key, value]}
            {#if key !="teamId" && key !="name" && key !="_id"} 
                <li class="data-item">{key}: <span class="data-value">{typeof value === 'number' ? value.toFixed(3) : value}</span></li>
            {/if}
        {/each}
    </ul>   


</div>


<style>
    
    .slot-container {
        background-color: #00b4d8;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        color: white;
        font-family: 'Arial', sans-serif;
    }

    h2 {
        margin-bottom: 15px;
        font-size: 1.5em;
        text-align: center;
    }

    .data-list {
        list-style-type: none; /* Remove bullet points */
        padding: 0;
    }

    .data-item {
        
        padding: 10px;
        margin: 5px 0;
        background-color: rgba(255, 255, 255, 0.2); /* Semi-transparent background */
        border-radius: 4px;
        transition: background-color 0.3s;
    
    }

    .data-item:hover {
        background-color: rgba(255, 255, 255, 0.3); /* Lighter on hover */
    }

    .data-value {
        font-weight: bold;
    }
</style>