<template >
    <div class="loginForm">
        <h1>Login</h1>
        <form action="POST">
            <input type="text" name="coachName" :value="coachName">
            <button>Login!</button>
        </form>
    </div>
</template>

<script>
export default {
    data(){
        return{
            backendUrl:process.env.VUE_APP_BACKEND_URL,
            coachName:''
        }
    },
    methods:{
        async LogInCoach(){

        }
    }
}
</script>

<style scoped>
     .loginForm{
        width:100%;
        height:60%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;

        font-size:2em;
     }

     form{
        width:25vw;
        height:30vh;
        background-color: #C73659;
        display:flex;
        flex-direction: column;

        justify-content: center;
        align-items: center;
        gap:2vh;
     }

     input{
        width:20vw;
        height:4vh;
     }

     button{
        width:5vw;

        font-size:1em;
        background-color:#EEEEEE;;
     }
</style>