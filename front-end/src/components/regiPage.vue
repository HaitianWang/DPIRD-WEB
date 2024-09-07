<template>
  <div>
    <el-form ref="regiForm" :model="user" label-width="120px" class="login-box">
      <h3 class="regi-title">Welcome to Register</h3>
      <el-form-item label="Username" prop="username">
        <el-input type="text" placeholder="Please enter username" v-model="user.username" />
      </el-form-item>
      <el-form-item label="Password" prop="pwd">
        <el-input type="password" placeholder="Please enter password (more than 6 characters)" v-model="user.pwd" />
      </el-form-item>
      <el-form-item label="Repeat Password" prop="pwd2">
        <el-input type="password" placeholder="Please repeat the password" v-model="user.pwd2" />
      </el-form-item>
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
        username: "",
        pwd: "",
        pwd2: ""
      },
      server_url: "http://127.0.0.1:5003"
    };
  },
  created() {
    this.$emit('header', false);
    this.$emit('content', false);
    this.$emit('footer', false);
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
    async regi() {
      console.log("Attempting registration with:", this.user.username);
      if (!this.validateForm()) return;
      try {
        const param = new FormData();
        param.append("username", this.user.username);
        param.append("pwd", this.user.pwd);
        const config = {
          headers: { "Content-Type": "multipart/form-data" },
        };
        console.log("Sending registration request");
        const response = await axios.post(`${this.server_url}/regi`, param, config);
        console.log("Registration response:", response.data);
        if (response.data.status === "1") {
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
        console.error("Registration error:", error);
        this.showAlert("An error occurred during registration");
      }
    },
    goFrontPage() {
      this.$router.push('/frontPage');
    }
  }
};
</script>

<style scoped>
.login-box {
  border: 1px solid #DCDFE6;
  width: 600px;
  margin: 180px auto;
  padding: 35px 35px 15px 35px;
  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;
  box-shadow: 0 0 25px #909399;
}

#btn {
  margin-left: -100px;
}
</style>