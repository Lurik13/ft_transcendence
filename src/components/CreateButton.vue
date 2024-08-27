<script setup> </script>

<template>
    <button class="button">
        <text class="buttonText">
            Play
        </text>
    </button>
</template>

<style>
.button {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 1rem 2rem;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    border-width: 0.2vw;
    transition: border-color 0.5s;
}

.buttonText {
    color: rgb(255, 255, 255);
    padding: 1rem 2rem;
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
    opacity: 1;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    transition: border-color 0.5s;
}

</style>
