<template >
    <div class='Navbar'>
        <div class="navLink" v-if="coach">Username</div>
        <div class="logging">
            <div class="navLink">Login</div>
            <div class="navLink" >Signup as a Coach!</div>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            coach:localStorage.getItem("coach"),
        }
    }
}
</script>
<style scoped>
    .Navbar{
        width:100vw;
        display: flex;
        flex-direction: row;
        justify-content: center;
    }

    .logging{
        display: flex;
        flex-direction: row;

        min-width:fit-content;
        gap:2vw;
    }
</style>