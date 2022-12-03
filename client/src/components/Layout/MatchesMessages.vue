<template>
    <div class="col-md-3 mt-0 matmess">
        {{ this.$router.currentRoute.fullPath }}
        <tabs :options="{ useUrlFragment: false }">
            <tab name="Matches">
                <div class="matches">
                    <div class="row d-flex mt-1">
                        <div v-for="match in Matches" class="card text-white w-50">
                            <RouterLink :to="{path: this.path + match.id }">
                            <img class="card-img" :src="match.picture" height="155" width="50" alt="Card image">
                            <div class="card-img-overlay">
                                <h6 class="card-title">{{ match.first_name + " " + match.last_name + " " + match.age }}</h6>
                            </div>
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </tab>
        </tabs>
    </div>
</template>
<script>
import req from '../../store/index.js';

export default {
    props: ['id', 'type'],
    data() {
        return {
            loading: true,
            Matches: [],
            ListMessages: [],
            path: ''
        }
    },


    watch: {
        id(id) {
            console.log(this.id)
            this.getMatches(this.id)
            this.getListMessages(this.id)
            if(this.$route.fullPath == '/app/' || this.$route.fullPath == '/app'){
                this.path = "/app/messages/"
            }
        },

    },

    methods: {
        getMatches(user_id) {
            const url = `/user/${user_id}/matches`
            req.get(url)
                .then(response => {
                    this.Matches = response.data
                    console.log(this.Matches)
                }).catch(error => {
                    console.log(error.response)
                });
        },
        getListMessages(user_id) {
            const url = `/user/${user_id}/messages`
            req.get(url)
                .then(response => {
                    this.ListMessages = response.data
                    console.log(this.ListMessages)
                }).catch(error => {
                    console.log(error.response)
                });
        },
    },
}
</script>
<style>
.matmess {
    padding: 0px;

}

.tabs-component-tabs {
    display: flex;
    list-style: none;
    justify-content: space-between;
    align-items: center;
    margin: 0;
    padding: 0;
}

.tabs-component-tab {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 90%;
    padding: 7px;
    
}

.tabs-component-tab a {
    text-decoration: none;
    font-size: 20px;
    color: black;
    width: 100%;
    text-align: center;
}

.is-active {
    background-color: rgb(182, 198, 203);
}



.matches div .card{
    border: none;
}
.matches div .card div h6{
    font-size: 12px;
    margin-left: 10px;

}
.matches div div a{
    color: white;
    text-decoration: none;
    margin-bottom: 20px;
}
</style>
