<!--
This component allows users to change their password.
Users need to provide their current password, new password, and confirmation of the new password.
Validation checks ensure the new password meets the length requirement and matches the confirmation password.
Upon submission, the new password is sent to the backend for processing.
Error and success messages are displayed based on the outcome of the password update request.
-->

<template>
  <div class="user-page">
    <!-- Form for changing the password -->
    <el-form ref="passwordForm" :model="user" label-width="180px" class="form-box">
      <h3>Change Password</h3>
      <el-form-item label="Current Password">
        <el-input type="password" placeholder="Please enter current password" v-model="user.currentPassword" />
      </el-form-item>
      <el-form-item label="New Password">
        <el-input type="password" placeholder="Please enter new password (more than 6 characters)" v-model="user.newPassword" />
      </el-form-item>
      <el-form-item label="Confirm New Password">
        <el-input type="password" placeholder="Please confirm the new password" v-model="user.confirmPassword" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="updatePassword" class="update-button">Submit</el-button>
      </el-form-item>
    </el-form>

    <!-- Error message if the update fails -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- Success message if the password is successfully updated -->
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
  import axios from "axios";
  import { mapGetters } from "vuex";

  export default {
    name: "userPage",
    created() {
      // Emit events to display the header and footer
      this.$emit('header', true);
      this.$emit('footer', true);
    },
    computed: {
      ...mapGetters(['getUsername']),
      username() {
        return this.getUsername;  // Fetch the username from the store
      }
    },
    data() {
      return {
        user: {
          currentPassword: "",  // Input for the current password
          newPassword: "",  // Input for the new password
          confirmPassword: "",  // Input for confirming the new password
        },
        server_url: "http://127.0.0.1:5003",  // Backend server URL for updating the password
        errorMessage: "",  // Error message to display if the update fails
        successMessage: ""  // Success message to display if the update succeeds
      };
    },
    methods: {
      // Show an error message when validation fails or update fails
      showAlert(message) {
        this.$message({
          showClose: true,
          message: message,
          type: 'error'
        });
      },
      // Validate the form before submission
      validateForm() {
        if (this.user.currentPassword.trim().length === 0) {
          this.showAlert("Please enter your current password");
          return false;
        }
        if (this.user.newPassword.length < 6) {
          this.showAlert("New password must be at least 6 characters");
          return false;
        }
        if (this.user.newPassword !== this.user.confirmPassword) {
          this.showAlert("New passwords do not match");
          return false;
        }
        return true;
      },
      // Submit the form and send the password update request to the backend
      async updatePassword() {
        this.errorMessage = "";
        this.successMessage = "";

        if (!this.validateForm()) return;

        try {
          const param = new FormData();
          param.append("username", this.username);  // Append the username
          param.append("current_password", this.user.currentPassword);  // Append the current password
          param.append("new_password", this.user.newPassword);  // Append the new password

          const config = {
            headers: { "Content-Type": "multipart/form-data" },
          };

          const response = await axios.post(`${this.server_url}/update_password`, param, config);  // Send the request

          if (response.data.status === "1") {  // If the update is successful
            this.successMessage = "Password updated successfully!";
            this.user.currentPassword = "";
            this.user.newPassword = "";
            this.user.confirmPassword = "";
          } else {
            this.showAlert(response.data.message || "Password update failed");
          }
        } catch (error) {
          this.showAlert("An error occurred while updating the password");
        }
      }
    }
  };
</script>

<style scoped>
  /* Form styling */
  .form-box {
    border: 1px solid #DCDFE6;
    width: 600px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }

  /* Styling for the submit button */
  .update-button {
    margin-left: -180px;
  }

  /* Error message styling */
  .error-message {
    color: red;
    margin-top: -150px;
    font-size: larger;
  }

  /* Success message styling */
  .success-message {
    color: green;
    margin-top: -150px;
    font-size: larger;
  }
</style>
