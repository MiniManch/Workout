import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../src/components/HomePage.vue';
import CoachLogin from '../src/components/Logging/CoachLogin.vue';
import CoachSignUp from '../src/components/Logging/CoachSignUp.vue';
import CoachProfile from '../src/components/Coach/CoachProfile.vue';
import CreateClient from '@/components/Client/CreateClient.vue';
import ClientProfile from '@/components/Client/ClientProfile.vue';
import AddSession from '@/components/Session/AddSession.vue';
import UpdateSession from '@/components/Session/UpdateSession.vue';
import SessionCalendar from '@/components/Session/SessionCalendar.vue';

const routes = [
    { path: '/', component: HomePage, name: 'Home' },
    { path: '/login', component: CoachLogin, name: 'Login' },
    { path: '/register', component: CoachSignUp, name: 'SignUp' },
    { path: '/coach_profile', component: CoachProfile, name: 'CoachProfile' },
    { path: '/create_client', component: CreateClient, name: 'CreateClient' },
    { path: '/update/client/:id', component: ClientProfile, name: 'ClientProfile' },
    { path: '/create_session/:date?', component: AddSession, name: 'AddSession' }, 
    { path: '/update/session/:id', component: UpdateSession, name: 'UpdateSession' },
    { path: '/session_calendar', component: SessionCalendar, name: 'SessionCalendar' },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
