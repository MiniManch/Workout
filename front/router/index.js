import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../src/components/HomePage.vue';
import CoachLogin from '../src/components/Logging/CoachLogin.vue';

const routes = [
    { path: '/', component: HomePage, name: 'Home' },
    { path: '/about', component: HomePage, name: 'about' },
    { path: '/login', component: CoachLogin, name: 'Login' },

];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
