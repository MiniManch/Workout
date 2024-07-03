<template lang="">
    <div>
        homepag
    </div>
</template>
<script>

export default {
    data(){
        return{
            coach:null,
        }
    },
    mounted(){
        this.coach = JSON.parse(localStorage.getItem('coach')) || null;
        if(this.coach){
            this.$router.push("/coach_profile");
        }
        else{
            this.$router.push("/login");
        }
    }

}
</script>
<style scoped>
    
</style>