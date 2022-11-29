<template>
    <div class="col-md-3 mt-0 req">
            <tabs :options="{ useUrlFragment: false }">
                <tab name="Likes received">
                    <div  v-for="(rec, index) in Received" class="col-md-12 rec d-flex justify-content-around align-items-center">
                        <a href="#" class="d-flex link-dark text-decoration-none">
                            <img :src="rec.picture" alt="mdo" width="40" height="40" class="rounded-circle mx-2">
                            <span class="name__rec">{{ rec.first_name }}<br>{{ rec.last_name }}</span>
                        </a>
                        <button @click="link(index, 1, rec.id)" class="lik">Like</button>
                        <button  @click="link(index, 0, rec.id)" class="dlik">Dislike</button>
                    </div>
                </tab>
            </tabs>
        </div>
</template>
<script>
import req from '../../store/index.js';

export default {
    props: ['id'],
    data() {
        return {
            loading: true,
            Received: [],
            isDisplay: true
        }
    },


    watch: {
        id(id) {
            console.log(this.id)
            this.getReceived(this.id)
        }
    },

    methods: {
        getReceived(user_id) {
            const url = `/user/${user_id}/received`
            req.get(url)
                .then(response => {
                    this.Received = response.data
                    console.log(this.Received)
                }).catch(error => {
                    console.log(error.response)
                });
        },

        link(index, link_type, receiver_id){
            const that = this
            req({
                method: 'post',
                url: '/link',
                data: {
                    "sender_id": that.id,
                    receiver_id,
                    "link_type": +link_type
                }
            })
                .then(response => {
                    console.log(response.data);
                    this.Received.splice(index, 1);
                        if(response.data.match){
                            this.$notify({
                            text: "It was a match",
                            type: 'info',
                        });
                    }
                })
                .catch(error => {
                    if (error.response) {
                        this.$notify({
                            text: error.response.data.error,
                            type: 'error',
                        });
                    }
                })
        },

    },
}
</script>
<style>
.req{
    padding: 0px;

}
.name__rec{
    font-size: 15px;
}
.tabs-component-tabs{
    display: flex;
    list-style: none;
    justify-content: space-between;
    align-items: center;
    margin: 0;
    padding: 0;
}
.tabs-component-tab{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 7px;
}
.tabs-component-tab a{
    text-decoration: none;
    font-size: 20px;
    color: black;
    width: 100%;
    text-align: center;
}
.is-active{
    background-color: rgb(203, 182, 197);
}

.rec{
    padding-top: 8px;
    padding-bottom: 8px;
}

.rec button{
    height: 20px;
    font-size: 10px;
    text-transform: capitalize;
    color: white;
    border: none;
    outline: none;
}
 
.rec .lik{
    background-color: green;
}

.rec .dlik{
    background-color: red;
}
</style>
