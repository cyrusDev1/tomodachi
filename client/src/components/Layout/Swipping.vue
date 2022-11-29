<template>
    <div class="col-md-6 mt-0 swip" style="overflow-y: visible;" id="swip">
        <div class="card text-white">
            <img class="card-img" :src="user.picture" height="620" alt="Card image">
            <div class="card-img-overlay my-100">
                <h3 class="card-title">{{user.first_name}} {{user.last_name}}</h3>
                <h5 class="card-title">{{user.age}}, {{user.country}}, {{user.gender}}</h5>
                <p class="card-text"><span v-for="i in user.interests">{{i.name}}</span></p>
                <div class="row interaction">
                    <div class="col-md-6">
                        <button @click="link(0)" class="dislike"><i class="fa fa-times"></i></button>
                    </div>
                    <div class="col-md-6">
                        <button @click="link(1)" class="like"><i class="fa fa-heart"></i></button>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
import req from '../../store/index.js';

export default {
    props: ['id'],
    data() {
        return {
            loading: true,
            Users: [],
            user: {},
            current_id: 0,
        }
    },


    watch: {
        id(id){
            this.getSwip(this.id)
        }
    },

    methods: {
        getSwip(user_id) {
            const url = `/user/${user_id}/swipping`
            req.get(url)
                .then(response => {
                    this.Users = response.data
                    console.log(response.data)
                    this.user = this.Users[current_id]
                }).catch(error => {
                    console.log(error.response)
                    this.$notify({
                        text: error.response.data.error,
                        type: 'error',
                    });
                });
        },

        nextUser(){
            this.current_id += 1
            this.user = this.Users[this.current_id]
            console.log(this.current_id)
        },
        
        link(link_type){
            const receiver_id = this.Users[this.current_id]
            const that = this
            req({
                method: 'post',
                url: '/link',
                data: {
                    "sender_id": that.id,
                    "receiver_id": receiver_id.id,
                    "link_type": +link_type
                }
            })
                .then(response => {
                    console.log(response.data);
                        if(response.data.match){
                            this.$notify({
                            text: "It was a match",
                            type: 'einfo',
                        });
                    }
                    this.nextUser()                    
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
#swip {
    overflow-y: visible;
    padding: 0px;
}

.card-img-overlay{
    margin-top: 65%;
}

.interaction{
    padding: 0px;
   
}
.interaction div{
    display: flex;
    justify-content: center;
}

.interaction div button{
border: none;
outline: none;
border-radius: 50%;
width: 50px;
height: 50px;
}

.interaction div .like{
background-color: green;
}

.interaction div .dislike{
background-color: red;
}

.interaction div i{
font-size: 30px;
color: white;

}

.card-img{
    border-radius: none;
}
.card-text span{
    margin-right: 6px;
}
</style>
