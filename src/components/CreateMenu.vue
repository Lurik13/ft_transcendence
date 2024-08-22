<script setup>
import { ref } from 'vue'

// TODO: Create a function that takes a string and returns the string reversed.
// @name is string for id of menu
// @items is table of objects
function createMenu(name, items) {
    if (name !== null || name !== "" || name !== undefined || name !== " ")
        return (console.log("Menu name is required"))
    if (items !== null || items !== "" || items !== undefined || items !== " ")
        return (console.log("Menu items are required"))
    return (console.log("Menu created"))
}
</script>
