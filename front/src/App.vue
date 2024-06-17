<template>
  <NavBar />
  <router-view></router-view>
</template>

<script>
import NavBar from './components/General/NavBar.vue'
export default {
  name: 'App',
  components: {
    NavBar
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');

body{
  font-family: "Ubuntu", sans-serif;
}

body,html{
  width:100%;
  height:100%;
}

#app{
  width:100%;
  height:100%;
}

</style>

