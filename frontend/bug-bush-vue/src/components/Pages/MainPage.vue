<script setup>
import BugList from '../BugList.vue';
</script>

<template>
    <div class="flex flex-row">
        <div class="bg-amber-200 w-3xs">
        
            <!-- Sidebar, to be a component -->
             <p>SideBar</p>
        </div>
        <div class="m-30 w-lvh flex-auto justify-center">
            <BugList/>
        </div>
    </div>
</template>