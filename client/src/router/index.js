import { createRouter, createWebHistory } from 'vue-router'
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/login",
            component: Login,
            name: 'Login'
        },
        {
            path: "/register",
            component: Register,
            name: 'Register'
        },
        /*{
            path: "/app",
            component: Main,
            name: 'Main',
            children:[
                {
                    path: '/home',
                    name: 'Home',
                    component: Home
                }
            ]
        }*/
        //component: () => import('../views/AboutView.vue')
    ]
})

export default router
