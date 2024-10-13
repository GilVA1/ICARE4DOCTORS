
<script>
    // THIS IS THE OUTER LAYOUT, EVERYTHING HERE IS UNIVERSAL



</script>



<header class="header-container">
    <h1> I CARE 4 DOCTORS </h1>

    <nav class="nav-menu">
        <a href="/" class="nav-link"> TEAM VIEW </a>
        <a href="/individual" class="nav-link"> INDIVIDUAL VIEW </a>
        <a href="/pulse" class="nav-link">PULSE</a>
    </nav>

</header>


<main>
    <slot></slot>
</main>


<footer>
    <p>©2024 CS49 </p>
</footer>


<style>

:global(body) {
    background-color: #caf0f8;
}


.header-container {
        background-color: #0077b6; /* Darker blue for a professional look */
        color: white;
        padding: 15px 20px; /* Padding for spacing */
        display: flex;
        justify-content: space-between; /* Space out the elements */
        align-items: center; /* Center items vertically */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
    }

    h1 {
        font-size: 2em; /* Increase font size for prominence */
        margin: 0; /* Remove default margin */
    }

    .nav-menu {
        display: flex; /* Use flexbox for the navigation */
        gap: 20px; /* Space between links */
    }

    .nav-link {
        text-decoration: none; /* Remove underline */
        color: white; /* Link color */
        padding: 10px 15px; /* Padding around links */
        border-radius: 4px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background color change */
    }

    .nav-link:hover {
        background-color: rgba(255, 255, 255, 0.2); /* Lighten on hover */
        color: #ecf0f1; /* Slightly lighter color on hover */
    }

</style>

