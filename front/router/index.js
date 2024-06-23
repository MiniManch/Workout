import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../src/components/HomePage.vue';
import CoachLogin from '../src/components/Logging/CoachLogin.vue';
import CoachSignUp from '../src/components/Logging/CoachSignUp.vue';
import CoachProfile from '../src/components/Coach/CoachProfile.vue';


const routes = [
    { path: '/', component: HomePage, name: 'Home' },
    { path: '/about', component: HomePage, name: 'about' },
    { path: '/login', component: CoachLogin, name: 'Login' },
    { path: '/register', component: CoachSignUp, name: 'SignUp' },
    { path: '/coach_profile', component: CoachProfile, name: 'CoachProfile' },

];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
