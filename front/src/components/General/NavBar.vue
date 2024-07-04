<template>
    <div class="NavbarWrapper">
      <nav class="Navbar">
        <ul>
          <li><div class="navLink" @click="goTo('/')">Home</div></li>
          <li v-if="coach"><div class="navLink" @click="goTo('/coach_profile')">{{ coach.name }}</div></li>
          <template  v-else>
            <li><div class="navLink" @click="goTo('login')">Login</div></li>
            <li><div class="navLink" @click="goTo('register')">Signup as a Coach!</div></li>
          </template>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        coach: JSON.parse(localStorage.getItem("coach")),
      };
    },
    methods:{
      goTo(link){
        this.$router.push(link);
      },
    }
  };
  </script>
  
  <style scoped>
  @import url('https://fonts.googleapis.com/css?family=Open+Sans');
  
  .NavbarWrapper {
    width: 100vw;
    height: 8vh;
    
    display: flex;
    position: fixed;
    justify-content: center;
    align-items: center;
    
    z-index: 3;
  }
  
  .Navbar {
    max-width: 960px;
    width: 100%;
    mask-image: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, #ffffff 25%, #ffffff 75%, rgba(255, 255, 255, 0) 100%);
    margin: 0 auto;
    padding: 10px 0;
    padding-top:0;
  }
  
  .Navbar ul {
    display: flex;
    justify-content: center;
    background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.2) 25%, rgba(255, 255, 255, 0.2) 75%, rgba(255, 255, 255, 0) 100%);
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.1), inset 0 0 1px rgba(255, 255, 255, 0.6);
    padding: 0;
    list-style: none;
    margin: 0;
    width: 100%;
  }
  
  .Navbar ul li {
    display: inline-block;
  }
  
  .Navbar ul li div {
    padding: 18px;
    font-family: "Open Sans", sans-serif;
    text-transform: uppercase;
    color: white;
    font-size: 18px;
    text-decoration: none;
    display: block;

    cursor:pointer;

    transition: all 0.4s;
  }
  
  .Navbar ul li div:hover {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1), inset 0 0 1px rgba(255, 255, 255, 0.6);
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }
  </style>
  