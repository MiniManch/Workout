import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../src/components/HomePage.vue';
import CoachLogin from '../src/components/Logging/CoachLogin.vue';
import CoachSignUp from '../src/components/Logging/CoachSignUp.vue';
import CoachProfile from '../src/components/Coach/CoachProfile.vue';
import CreateClient from '@/components/Client/CreateClient.vue';

const routes = [
    { path: '/', component: HomePage, name: 'Home' },
    { path: '/about', component: HomePage, name: 'about' },
    { path: '/login', component: CoachLogin, name: 'Login' },
    { path: '/register', component: CoachSignUp, name: 'SignUp' },
    { path: '/coach_profile', component: CoachProfile, name: 'CoachProfile' },
    { path: '/create_client', component: CreateClient, name: 'CreateClient' },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
