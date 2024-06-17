<template >
    <div>
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
     
</style>