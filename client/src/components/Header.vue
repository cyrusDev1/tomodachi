<template>
    <header class="py-3 border-bottom container-fluid d-flex  align-items-center">
        <div class="col-md-3">
            <a @click="this.$router.push('/app')" href="#" class="d-flex fs-1 justify-content-center align-items-center link-dark text-decoration-none" aria-expanded="false">
                TOMODACHI
            </a>
        </div>

        <div class="col-md-6 border-end border-start">
            <form class="w-100 d-flex justify-content-center" role="search">
                <input type="search" class="form-control w-75" placeholder="Search..." aria-label="Search">
            </form>
        </div>

        <div class="col-md-3 d-flex justify-content-around">
            <a href="#" class="d-flex link-dark text-decoration-none">
                <img :src="user.picture" alt="mdo" width="50" height="50" class="rounded-circle mx-2">
                <span>{{ user.first_name }}<br>{{ user.last_name }}</span>
            </a>

            <button @click="logout" class="border rounded-circle"><i class="fa fa-sign-out-alt"></i></button>
        </div>

    </header>
</template>
<script>
import req from '../store/index.js';

export default {
    props: ['user'],
    data() {
        return {
            loading: true,
        }
    },


    created() {

    },

    methods: {
        getUser(user_id) {
            const url = `/user/${user_id}`
            req.get(url)
                .then(response => {
                    this.User = response.data
                    console.log(this.User)
                    const text = `Welcome ${this.User.last_name} ${this.User.first_name}`
                    if (this.$route.fullPath == '/app/'){
                        this.$notify({
                            text,
                            type: 'success',
                        });
                    }
                  
                }).catch(error => {
                    console.log(error.response)
                    this.$router.push('/login')
                    this.$notify({
                        text: error.response.data.error,
                        type: 'error',
                    });
                });

        },
        logout(){
            localStorage.clear();
            this.$router.push('/login')
            this.$notify({
                text: "Logout succesfuly",
                type: 'warn',
            });
        }

    },
}
</script>
<style>
.border{
    width: 50px;
    height: 50px;
    background-color: black;
    color: white;
}
</style>
