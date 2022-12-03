<template>
    <div class="register">
        <FormKit type="form" submit-label="Login" @submit="login">
            <h1 class="">Login!</h1>
            <p>
                Login Tomodachi to meet new friends.
            </p>
            <p>New user ? <RouterLink to="/register">Register</RouterLink></p>

            <hr />
            <FormKit type="email" name="email" label="Your email" placeholder="jane@gmail.com" validation="required" />
            <FormKit type="password" name="password" label="Your password" placeholder="Your password"
                validation="required" />
        </FormKit>
    </div>

</template>
<script>
import req from '../store/index.js';
import { useCookies } from "vue3-cookies";


export default {
    data() {
        return {
        }
    },

    setup() {
        const { cookies } = useCookies();
        return { cookies };
    },

    methods: {
        login(data) {
            req({
                method: 'post',
                url: '/login',
                data: data
            })
                .then(response => {
                    console.log(response);
                    const id = response.data.id
                    this.cookies.set("user_id", id, "10d");
                    let my_cookie_value = this.cookies.get("user_id");
                    console.log(my_cookie_value);
                    this.$router.push('/app')
                })
                .catch(error => {
                    if (error.response) {
                        this.$notify({
                            text: error.response.data.error,
                            type: 'error',
                        });
                    }
                })
        }
    }
}
</script>
<style>

</style>
