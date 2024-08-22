<script setup>
import { ref } from 'vue'

// @name is string for id of menu
// @items is table of objects
// @component is table component css.
function createButton(name, items, component) {
    if (!name || name.trim() === "") {
        console.log("Menu name is required");
        return;
    }
    if (!items || items.length === 0) {
        console.log("Menu items are required");
        return;
    }
    console.log("Menu created");
}
</script>
