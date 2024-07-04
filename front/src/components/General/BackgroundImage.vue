<template >
    <img src="/images/background.jpg" alt="" class="backgroundImage">
    <div class="overlay"></div>
</template>
<script>
export default {
    
}
</script>
<style >
.backgroundImage{
    position:absolute;
    top:0;
    left:0;
    z-index: -3;
    height:100vh;
    width:100vw;
}

.overlay{
    position: absolute;
    width:100vw;
    height:100vh;
    background-color: rgba(0,0,0,0.5);
    z-index: -2;
}
</style>