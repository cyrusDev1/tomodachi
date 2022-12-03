<template>
    <div class="row">
        <MatchesMessages :id="id"></MatchesMessages>
        <Swipping v-if="path == '/app/' || path == '/app'" :id="id"></Swipping>
        <Chatbox v-else :id="id" :user="this.user"></Chatbox>
        <Request :id="id"></Request>
    </div>
</template>
<script>
import MatchesMessages from "../components/Layout/MatchesMessages.vue"
import Swipping from "../components/Layout/Swipping.vue"
import Request from "../components/Layout/Request.vue"
import Chatbox from "../components/Layout/Chatbox.vue"


export default {
    components: {
        MatchesMessages,
        Swipping,
        Request,
        Chatbox,
    },
    props: ['id', 'user'],

    data() {
        return {
            loading: true,
            path: this.$route.fullPath,
            id_message: ''
        }
    },


    created() {
        console.log(this.path)
    },

}
</script>
<style>

</style>
