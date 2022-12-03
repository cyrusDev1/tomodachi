<template>
    <div class="col-md-6 mt-0 swip" style="" id="swip">
        <section style="background-color: #eee;">
            <div class="container">
                <div class="row d-flex justify-content-center">
                    <div class="col-md-12">

                        <div class="card" id="chat2">
                            <div class="card-header d-flex justify-content-between align-items-center p-3">
                                <img :src="UserMsg.picture" alt="avatar 1" style="width: 50px; height: 50px;"
                                    class=" rounded-circle">
                                <h5 class="mb-0">{{ UserMsg.first_name + " " + UserMsg.last_name }}</h5>
                                <button @click="this.$router.push('/app')" class="btn btn-danger btn-sm"
                                    data-mdb-ripple-color="dark"><i class="fa fa-times"></i></button>
                            </div>
                            <div class="card-body" id="scr"  
                                style="position: relative; overflow-y: auto; height: 400px;">

                                <!--div class="divider d-flex align-items-center mb-4">
                                    <p class="text-center mx-3 mb-0" style="color: #a2aab7;">Today</p>
                                </div-->

                                <div v-for="mesg in Messages"
                                    v-bind:class="mesg.sender_id == user.id ? class_sender[0] : class_receiver[0]">
                                    <div v-show="mesg.sender_id == user.id">
                                        <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">
                                            {{ mesg.message }}
                                        </p>

                                        <p class="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">
                                            {{ mesg.created_at.split('T')[1] }}
                                        </p>
                                    </div>
                                    <img v-show="mesg.sender_id == user.id"
                                        :src="user.picture"
                                        alt="avatar 1" class="rounded-circle" style="width: 50px; height: 50px;">

                                    

                                    <img v-show="mesg.sender_id != user.id"
                                    :src="UserMsg.picture"
                                         alt="avatar 1" class="rounded-circle" style="width: 50px; height: 50px;">
                                    <div v-show="mesg.sender_id != user.id">
                                        <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;"> {{ mesg.message }}</p>
                                        <p class="small ms-3 mb-3 rounded-3 text-muted"> {{ mesg.created_at.split('T')[1] }}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="card-footer text-muted d-flex justify-content-start align-items-center p-3">
                                <img :src="user.picture" alt="avatar 3" class="rounded-circle"
                                    style="width: 40px; height: 40px;">
                                <input v-model="msg" type="text" class="form-control form-control-lg"
                                    id="exampleFormControlInput1" placeholder="Type message">
                                <a @click="doMessages(this.$route.params.id, 'post')" class="ms-3" href="#"><i
                                        class="fas fa-paper-plane"></i></a>
                            </div>
                        </div>

                    </div>
                </div>

            </div>
        </section>

    </div>

</template>
<script>
import req from '../../store/index.js';
import moment from 'moment';


export default {
    props: ['id', 'user'],
    data() {
        return {
            loading: true,
            UserMsg: [],
            msg: null,
            Messages: [],
            class_sender: ["d-flex flex-row justify-content-end mb-4 pt-1",
                "small p-2 me-3 mb-1 text-white rounded-3 bg-primary", "small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end", this.user.picture],
            class_receiver: ["d-flex flex-row justify-content-start", "small p-2 ms-3 mb-1 rounded-3", "small ms-3 mb-3 rounded-3 text-muted"]
        }
    },


    created() {
        this.getUserMsg(this.$route.params.id)
        this.$watch(
            () => this.$route.params, (toParams, previousParams) => {
                console.log(toParams.id)
                this.getUserMsg(toParams.id)
                this.doMessages(toParams.id, "get")
            }
        )

         
    },

    watch: {
        user(user) {
            console.log(user)
            this.doMessages(this.$route.params.id, "get")
        },
        Messages(){
            const objDiv = document.getElementById("scr");
		    objDiv.scrollTop = objDiv.scrollHeight;
            console.log( objDiv.scrollHeight)
        }
    },

    methods: {
        getUserMsg(id) {
            const url = `/user/${id}`
            req.get(url)
                .then(response => {
                    this.UserMsg = response.data
                }).catch(error => {
                    console.log(error.response)
                    this.$notify({
                        text: error.response.data?.error,
                        type: 'error',
                    });
                });
        },

        moment: function () {
            return moment();
        },

        doMessages(rec_id, types) {
            const that = this
            console.log(types)
            req({
                method: 'post',
                url: '/messages',
                data: {
                    "sender_id": that.user.id,
                    "receiver_id": rec_id,
                    types,
                    message: that.msg
                }
            })
                .then(response => {
                    console.log(response.data);
                    if (types == "get") {
                        this.Messages = response.data.reverse()
                    } else if (types == "post") {
                        this.Messages.push(response.data)
                        this.msg = null
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
.card-img-overlay {
    margin-top: 65%;
}

.interaction {
    padding: 0px;

}

.interaction div {
    display: flex;
    justify-content: center;
}

.interaction div button {
    border: none;
    outline: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
}

.interaction div .like {
    background-color: green;
}

.interaction div .dislike {
    background-color: red;
}

.interaction div i {
    font-size: 30px;
    color: white;

}

.card-img {
    border-radius: none;
}

.card-text span {
    margin-right: 6px;
}
</style>
