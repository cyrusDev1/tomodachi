<template>
    <div class="register">
        <FormKit type="form" submit-label="Register" @submit="login">

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


            <pre wrap>{{ value }}</pre>
            {{ img1 }}
        </FormKit>
    </div>

</template>
<script>
export default {
    data() {
        return {
            loading: true,
            img1: '',
            imageData: null
        }
    },

    methods: {
        previewImage(event) {
            this.uploadValue = 0;
            this.img1 = null;
            this.imageData = event.target.files[0];
            this.img1 = URL.createObjectURL(event.target.files[0]);
        },

        login(value) {
            alert(value);
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
