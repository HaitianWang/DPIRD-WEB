<template>
  <div class="user-page">
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
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
  import axios from "axios";
  import { mapGetters } from "vuex";

  export default {
    name: "userPage",
    created() {
      this.$emit('header', true);
      this.$emit('footer', true);
    },
    computed: {
      ...mapGetters(['getUsername']),
      username() {
        return this.getUsername;
      }
    },
    data() {
      return {
        user: {
          currentPassword: "",
          newPassword: "",
          confirmPassword: "",
        },
        server_url: "http://127.0.0.1:5003",
        errorMessage: "",
        successMessage: ""
      };
    },
    methods: {
      showAlert(message) {
        this.$message({
          showClose: true,
          message: message,
          type: 'error'
        });
      },
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
      async updatePassword() {
        this.errorMessage = "";
        this.successMessage = "";

        if (!this.validateForm()) return;

        try {
          const param = new FormData();
          param.append("username", this.username);
          param.append("current_password", this.user.currentPassword);
          param.append("new_password", this.user.newPassword);

          const config = {
            headers: { "Content-Type": "multipart/form-data" },
          };

          const response = await axios.post(`${this.server_url}/update_password`, param, config);

          if (response.data.status === "1") {
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
  .form-box {
    border: 1px solid #DCDFE6;
    width: 600px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }

  .update-button {
    margin-left: -180px;
  }

  .error-message {
    color: red;
    margin-top: -150px;
    font-size: larger;
  }

  .success-message {
    color: green;
    margin-top: -150px;
    font-size: larger;
  }
</style>
