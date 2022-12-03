<template>
    <div class="register">
        <FormKit type="form" submit-label="Register" @submit="register" #default="{ value }">
            <h1 class="">Register!</h1>
            <p>
                Join Tomodachi to meet new friends.
            </p>
            <p>Have you account ? <RouterLink to="/login">Login</RouterLink></p>
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

            <FormKit type="checkbox" label="Interests" name="interests" :options="[
                {
                    'value': '2c4a1e9e-6655-44ca-9022-8e8f1854fb19',
                    'label': 'Design'
                },
                {
                    'value': '480cbbae-3a52-4310-8f98-2d1cd6f8be88',
                    'label': 'World Cup'
                },
                {
                    'value': '546c598a-c991-405e-ad80-59f8a475654a',
                    'label': 'Football'
                },
                {
                    'value': '582afc07-306c-4dfc-8d7c-0b43ee506bd0',
                    'label': 'Github'
                },
                {
                    'value': '87dd7266-8e06-4cda-9013-39e3e94361ed',
                    'label': 'Bleach'
                },
                {
                    'value': '9671f29e-d506-4870-baf1-c170bba9252a',
                    'label': 'Software'
                },
                {
                    'value': '9b74b40b-af55-4769-b416-a74c49a1d06c',
                    'label': 'Reading'
                },
                {
                    'value': 'a978deda-f670-41d9-9c5e-f343d536db13',
                    'label': 'Python'
                },
                {
                    'value': 'd08b87ed-5d3a-4f23-b4b5-fce1095b2e58',
                    'label': 'Naruto'
                },
                {
                    'value': 'd99d57f3-6425-4acd-8edd-ea01e5cba4df',
                    'label': 'Programming'
                },
                {
                    'value': 'e1c5d8bd-1b42-481a-871e-86dff97a44e0',
                    'label': 'Anime'
                },
                {
                    'value': 'f796ce5f-675f-4773-a68f-f5c8e88ac516',
                    'label': 'TikTok'
                },
                {
                    'value': 'fc0add0a-ba64-4d84-adb6-c50155c689ab',
                    'label': 'Game'
                }
            ]" decorator-icon="heart" help="Select your interests" validation="min:0" />

        </FormKit>
        <div v-show="load" class="chargement" style="margin-top: -20px; display:inline">
                <div class="d-flex justify-content-center align-items-center" style="margin-top: -50px;">
                    <div class="spinner-border" role="status">
                        <span class="sr-only">Loading...</span>
                    </div>
                </div>
        </div>
    </div>

</template>
<script>
import firebase from 'firebase';
import req from '../store/index.js';

export default {
    data() {
        return {
            load: false,
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
            this.load = true
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
