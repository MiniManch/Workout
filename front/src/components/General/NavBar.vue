<template >
    <div class='Navbar'>
        <a class="navLink" href="/">Home</a>
        <a class="navLink" href='/coach_profile' v-if="coach">{{coach.name}}</a>
        
        <div class="logging" v-else>
            <a class="navLink" href="/login">Login</a>
            <a class="navLink" href="/register">Signup as a Coach!</a>
        </div>
    </div>
</template>

<script>
export default {
    data(){
        return{
            coach:JSON.parse(localStorage.getItem("coach")),
        }
    }
}
</script>

<style scoped>
.Navbar {
    width: 100vw;
    height: 8vh;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 2vw;

    background-color: #A91D3A;
    font-size: 2em;
}

.logging {
    display: flex;
    flex-direction: row;
    min-width: fit-content;
    gap: 2vw;
}

.navLink {
    position: relative;
    padding-bottom: 2px;
    cursor: pointer;
    color:#EEEEEE;

    text-decoration: none;
}

.navLink:before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background-color: #EEEEEE;
    transition: width 0.3s ease, left 0.3s ease;
}

.navLink:hover:before {
    width: 100%;
    left: 0;
}
</style>