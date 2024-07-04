  <template>
  <BackgroundImage v-if="!isHomePage"/>
  <NavBar />
  <CoachActions />
  <router-view></router-view>
</template>

<script>
import NavBar from './components/General/NavBar.vue';
import BackgroundImage from "@/components/General/BackgroundImage.vue";
import CoachActions from './components/Coach/CoachActions.vue';

export default {
  name: 'App',
  computed:{
    isHomePage(){
      return this.$route.path === '/';
    }
  },
  components: {
    NavBar,
    CoachActions,
    BackgroundImage
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,100..900;1,100..900&family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap');

body{
  font-family: "Ubuntu", sans-serif;
  background-color: #151515;
  overflow-x: hidden;


  color:#EEEEEE;
  margin:0;
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

