<template>
    <Header :user="this.User"></Header>
    <Layout :id="this.User.id" :user="this.User"></Layout>
 </template>
 
<script>
import { useCookies } from "vue3-cookies";
import req from '../store/index.js';
import Header from '../components/Header.vue'
import Layout from '../components/Layout.vue'
export default {
    components: {
        Header,
        Layout,
    },
    data() {
        return {
            loading: true,
            User: [],
            msg_id: this.$route.params.id
        }
    },

    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },

    created() {
        const user_id = this.cookies.get('user_id')
        this.getUser(user_id)
    },

    methods: {
        getUser(user_id) {
            const url = `/user/${user_id}`
            req.get(url)
                .then(response => {
                    this.User = response.data
                    console.log(this.User)
                    const text = `Welcome ${this.User.last_name} ${this.User.first_name}`
                    this.$notify({
                        text,
                        type: 'success',
                    });
                }).catch(error => {
                    console.log(error.response)
                    this.$router.push('/login')
                    this.$notify({
                        text: error.response.data.error,
                        type: 'error',
                    });
                });
        },

    },
}
</script>
<style>

</style>
