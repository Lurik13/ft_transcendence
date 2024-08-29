<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();
function goToNewPage() {
    router.push('/game'); // Remplacez '/new-page' par la route que vous souhaitez
}
</script>

<template>
    <div class="buttonContainer">
        <button class="button" @click="goToNewPage">
            <i class="fas fa-play" style="margin-right: 8px;"></i>
            <span class="buttonText buttonTextSize">Play</span>
        </button>

        <button class="button button-credits" @click="clickButton">
            <span class="buttonText">Credits</span>
        </button>

        <button class="button button-log" @click="clickButton">
            <span class="buttonText">Login</span>
        </button>
        <button class="button button-settings" @click="clickButton">
            <i class="fas fa-gear"></i>
        </button>
    </div>
</template>

<style>
.buttonContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 140vh;
    position: relative;
}

.button {
    background-color: rgba(255, 255, 255, 0.0);
    padding: 1rem 1rem;
    border: 4px solid rgba(255, 255, 255, 0.5);
    border-radius: 0.4vw;
    border-width: 0.15vw;
    transition: border-color 0.5s;
    margin-top: 10px;
    width: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.buttonText {
    color: rgb(255, 255, 255);
    font-size: 1.25rem;
    font-weight: 600;
    cursor: pointer;
    opacity: 1;
}

.button i {
    color: rgb(255, 255, 255);
    font-size: 1.5rem;
    cursor: pointer;
}

.button:hover {
    border-color: rgba(255, 255, 255, 1);
    background-color: rgba(255, 255, 255, 0.4);
    transition: border-color, background-color 0.5s;
}

.button-log {
    position: absolute;
    width: 120px;
    height: 50px;
    top: 40px;
    right: 10px;
}

.button-settings {
    position: absolute;
    width: 60px;
    height: 50px;
    top: 40px;
    right: 140px;
}

.button-credits {
    /* position: absolute; */
    width: 120px;
    height: 50px;
    /* bottom: -40px; */
}
</style>
