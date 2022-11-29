<template>
    <div class="register">
        <FormKit type="form" submit-label="Register" @submit="register" #default="{ value }">

            <h1 class="">Register!</h1>
            <p>
                Join Tomodachi to meet new friends.
            </p>
            <hr />
            <FormKit type="text" name="first_name" label="Your first name" placeholder="Jane" validation="required" />
            <FormKit type="text" name="last_name" label="Your last name" placeholder="Doe" validation="required" />
            <FormKit type="text" name="email" label="Your email" placeholder="jane@example.com"
                validation="required|email" />
            <FormKit type="select" label="What is your gender?" name="gender" :options="[
                'Male',
                'Female',
            ]" />
            <FormKit type="text" name="age" label="Your age" placeholder="20" validation="required" />
            <FormKit type="text" name="country" label="Your country" placeholder="Benin" validation="required" />
            <div class="double">
                <FormKit type="password" name="password" label="Password"
                    validation="required|length:6|matches:/[^a-zA-Z]/" :validation-messages="{
                        matches: 'Please include at least one symbol',
                    }" placeholder="Your password" />
                <FormKit type="password" name="password_confirm" label="Confirm password" placeholder="Confirm password"
                    validation="required|confirm" />
                <FormKit @change="previewImage" type="file" label="Profile Picture" name="picture" required
                    accept=".png,.jpg,.jpeg,.PNG,.JPG,.JPEG" />
            </div>



            <div v-if="imageData != null">
                <img class="preview" height="268" width="356" :src="img1">
                <br>
            </div>

            <FormKit type="checkbox" label="Interests" name="interests"
                :options="[{ 'value': '30ca46ff-fdcc-421b-8e71-7ab7b06fab9a', 'label': 'Naruto' }, { 'value': 'b58f0850-bc15-4ba5-a952-3354f1e64c2c', 'label': 'Bleach' }]"
                decorator-icon="heart" help="Select your interests" validation="min:0" />

            <pre>{{ value }}</pre>
        </FormKit>
    </div>

</template>
<script>
import firebase from 'firebase';
import req from '../store/index.js';
import { useCookies } from "vue3-cookies";

export default {
    data() {
        return {
            loading: true,
            img1: '',
            imageData: null,
            uploadValue: 0,
            Interests: []
        }
    },

    //
    created() {
        const url = `/interests`
        const that = this
        req.get(url)
            .then(response => {
                const Interests = []
                response.data.forEach(interest => {
                    const select = {
                        "value": interest.id,
                        "label": interest.name
                    }
                    that.Interests.push(select)
                });
            }).catch(error => {
                console.log(error)
            });
    },
    methods: {
        previewImage(event) {
            this.uploadValue = 0;
            this.img1 = null;
            this.imageData = event.target.files[0];
            this.img1 = URL.createObjectURL(event.target.files[0]);
            //this.onUpload()
        },

        getInterests() {

        },

        register(value) {
            value.picture = null
            const storageRef = firebase.storage().ref(`${this.imageData.name}`).put(this.imageData);
            storageRef.on(`state_changed`, snapshot => {
                this.uploadValue = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            }, error => { console.log(error.message) },
                () => {
                    this.uploadValue = 100;
                    storageRef.snapshot.ref.getDownloadURL().then((url) => {
                        value.picture = url;
                        req({
                            method: 'post',
                            url: '/users',
                            data: value
                        })
                            .then(response => {
                                console.log(response);
                                const user_id = response.data.id
                                this.postInterests(user_id, value.interests)
                            })
                            .catch(error => {
                                if (error.response) {
                                    this.$notify({
                                        text: error.response.data.error,
                                        type: 'error',
                                    });
                                }
                            })
                    });
                }
            );
        },

        postInterests(user_id, interests) {
            req({
                method: 'post',
                url: '/user/interests',
                data: {
                    user_id,
                    interests,
                }
            })
                .then(response => {
                    console.log(response);
                    this.$router.push('/login')
                }).catch(error => {
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
.register {
    margin-top: 60px;
    width: 400px;
    margin-left: auto;
    margin-right: auto;
}
</style>
