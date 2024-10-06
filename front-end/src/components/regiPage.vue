<!--
This is the registration component for the DPIRD AgriVision frontend.
It allows users to register a new account by providing a username and password.
The component validates the input (password length and matching passwords) before sending the registration request to the backend.
The form also provides navigation back to the login page.
Element-UI components are used for form fields and buttons.
-->

<template>
  <div>
    <el-form ref="regiForm" :model="user" label-width="120px" class="login-box">
      <!-- Registration title -->
      <h3 class="regi-title">Welcome to Register</h3>
      <!-- Input for the username -->
      <el-form-item label="Username" prop="username">
        <el-input type="text" placeholder="Please enter username" v-model="user.username" />
      </el-form-item>
      <!-- Input for the password -->
      <el-form-item label="Password" prop="pwd">
        <el-input type="password" placeholder="Please enter password (more than 6 characters)" v-model="user.pwd" />
      </el-form-item>
      <!-- Input to repeat the password -->
      <el-form-item label="Repeat Password" prop="pwd2">
        <el-input type="password" placeholder="Please repeat the password" v-model="user.pwd2" />
      </el-form-item>
      <!-- Confirm and back buttons -->
      <el-form-item>
        <el-button type="primary" @click="regi" id="btn">Confirm</el-button>
        <el-button type="primary" @click="goFrontPage" id="btn2">Back</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import axios from "axios";

  export default {
    name: "regiPage",
    data() {
      return {
        user: {
          username: "",  // The username input field
          pwd: "",  // The password input field
          pwd2: ""  // The repeated password input field
        },
        server_url: "http://127.0.0.1:5003"  // Backend server URL for registration
      };
    },
    created() {
      // Hide header, content, and footer when on the registration page
      this.$emit('header', false);
      this.$emit('content', false);
      this.$emit('footer', false);
    },
    methods: {
      // Show an error message in case of form validation failure or registration failure
      showAlert(message) {
        this.$message({
          showClose: true,
          message: message,
          type: 'error'
        });
      },
      // Validate the form before submitting
      validateForm() {
        if (this.user.username.trim().length === 0) {
          this.showAlert("Please enter username");
          return false;
        }
        if (this.user.pwd.length < 6) {
          this.showAlert("Password must be at least 6 characters");
          return false;
        }
        if (this.user.pwd !== this.user.pwd2) {
          this.showAlert("Passwords do not match");
          return false;
        }
        return true;
      },
      // Register the user by sending the registration data to the backend
      async regi() {
        console.log("Attempting registration with:", this.user.username);
        if (!this.validateForm()) return;
        try {
          const param = new FormData();
          param.append("username", this.user.username);  // Append username
          param.append("pwd", this.user.pwd);  // Append password
          const config = {
            headers: { "Content-Type": "multipart/form-data" },
          };
          console.log("Sending registration request");
          const response = await axios.post(`${this.server_url}/regi`, param, config);  // Send registration request
          console.log("Registration response:", response.data);
          if (response.data.status === "1") {  // If registration is successful
            this.$message({
              message: "Registration successful! Please log in.",
              type: 'success',
              duration: 3000
            });
            setTimeout(() => {
              this.$router.push('/');  // Redirect to the front page (login page)
            }, 2000);
          } else {
            this.showAlert(response.data.message || "Registration failed");
          }
        } catch (error) {
          console.error("Registration error:", error);  // Handle registration error
          this.showAlert("An error occurred during registration");
        }
      },
      // Navigate back to the login page
      goFrontPage() {
        this.$router.push('/frontPage');
      }
    }
  };
</script>

<style scoped>
  /* Style for the registration form container */
  .login-box {
    border: 1px solid #DCDFE6;
    width: 600px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }

  /* Style for the confirm button */
  #btn {
    margin-left: -100px;
  }
</style>
