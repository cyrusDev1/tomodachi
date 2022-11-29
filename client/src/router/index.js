import { createRouter, createWebHistory } from 'vue-router'
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import Main from "../views/Main.vue"
import Message from "../views/Message.vue"


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
        {
            path: "/app",
            component: Main,
            name: 'Main',
        },
        {
                path: '/app/messages/:id',
                name: 'Message',
                component: Message
        }
        
        //component: () => import('../views/AboutView.vue')
    ]
})

export default router
