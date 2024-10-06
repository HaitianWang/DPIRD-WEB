<!--
This is the login component for the DPIRD AgriVision frontend.
It allows users to input their username and password, submit the form, and log in to the system.
The component integrates with the backend API to verify credentials.
Additionally, users who do not have an account can navigate to the registration page.
The UI is styled using Element-UI components and custom CSS for a clean, responsive layout.
-->

<template>
  <div class="login-container">
    <el-form ref="loginForm" label-width="80px" class="login-box">
      <!-- The title for the login page -->
      <h3 class="login-title">DPIRDAgriVision</h3>
      <!-- Input for the username -->
      <el-form-item label="username" prop="username">
        <el-input type="text" placeholder="please enter username" v-model="username"/>
      </el-form-item>
      <!-- Input for the password -->
      <el-form-item label="password" prop="pwd">
        <el-input type="password" placeholder="please enter password" v-model="pwd"/>
      </el-form-item>
      <!-- Login button -->
      <el-form-item>
        <el-button type="primary" v-on:click="loginUser('loginForm')" id="btn">login</el-button>
      </el-form-item>
      <!-- Link to the registration page if the user does not have an account -->
      <h5>no account? please <span v-on:click="goRegister()" style="color: blue;text-decoration: underline">register</span></h5>
    </el-form>
  </div>
</template>

<script>
  import axios from "axios";
  import { mapActions } from 'vuex';

  export default {
    name: "frontPage",
    created() {
      // Hide header, content, and footer when the login page is active
      this.$emit('header', false);
      this.$emit('content', false);
      this.$emit('footer', false);
    },
    data() {
      return {
        username: "",  // Username input field
        pwd: "",  // Password input field
        server_url: "http://127.0.0.1:5003"  // Backend API server URL
      }
    },
    created: function () {
      // Set the document title when the page is loaded
      document.title = "DPIRD AgriVision";
      this.$emit('header', false);  // Hide header
      this.$emit('footer', false);  // Hide footer
    },
    methods: {
      ...mapActions(['login']),
      // Handles the user login process
      loginUser(data) {
        console.log("Attempting login with:", this.username, this.pwd);
        let param = new FormData();  // Prepare form data
        param.append("username", this.username);  // Append username
        param.append("pwd", this.pwd);  // Append password
        let config = {
          headers: { "Content-Type": "multipart/form-data" },
        };
        axios
          .post(this.server_url + "/login", param, config)  // Send login request
          .then((response) => {
            console.log("Login response:", response.data);
            if (response.data.status === "1") {  // If login is successful
              console.log("Login successful");
              this.login(this.username);  // Dispatch Vuex action to store user info
              this.$router.replace('/mainPage');  // Navigate to the main page
            } else {
              console.log("Login failed");
              window.alert(response.data.message || "Username or password error");  // Show error message
            }
          })
          .catch((error) => {
            console.error("Login error:", error);  // Handle login error
            window.alert("An error occurred during login");
          });
      },
      // Navigate to the registration page
      goRegister(){
        this.$router.push('/regiPage');
      }
    },
  };
</script>

<style scoped>
  /* Style for the login page container */
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-image: url('~@/assets/8.jpg');  /* Set background image for the login page */
    background-size: cover;
    background-position: center;
  }

  /* Style for the login form box */
  .login-box {
    background: rgba(255, 255, 255, 0.9);  /* Semi-transparent background */
    border: 1px solid #DCDFE6;
    width: 350px;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    box-shadow: 0 0 25px #909399;  /* Box shadow for depth */
  }

  /* Style for the login button */
  #btn {
    margin-left: -60px;
  }
</style>
