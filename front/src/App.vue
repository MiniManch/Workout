  <template>
    <img src="/images/background.jpg" alt="" class="backgroundImage">
    <div class="overlay"></div>
  <NavBar />
  <CoachActions />
  <router-view></router-view>
</template>

<script>
import NavBar from './components/General/NavBar.vue';
import CoachActions from './components/Coach/CoachActions.vue';

export default {
  name: 'App',
  components: {
    NavBar,
    CoachActions
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

#app{
  width:100%;
  height:100%;
}

</style>

