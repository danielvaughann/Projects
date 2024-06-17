import app from "../api/firebase";

import { createRouter, createWebHistory } from 'vue-router';

function loadPage(component) {
    // '@' is aliased to src/components
    return () => import(/* webpackChunkName: "[request]" */
        `@/pages/${component}.vue`)
}
export default [
    { path: '/', component: loadPage('Login') },
    { path: '/signup', component: loadPage('Signup') },
    { path: '/chat', component: loadPage('Chat') },
    { path: '/chatbox', component: loadPage('Chatbox') },
    { path: '/profile', component: loadPage('Profile') },

]

