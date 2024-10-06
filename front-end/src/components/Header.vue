<!--
This is the header component for the DPIRD AgriVision frontend.
It provides user options like navigating to the "Upload" and "TimeCapsule" pages, and it includes a dropdown for user-specific actions such as changing the password or exiting the platform.
The header displays a welcome message and offers navigation functionality using Vue Router.
Element-UI components are used for dropdowns, icons, and styling.
-->

<template>
  <div id="Header">
    <!-- Top-left section with user information and dropdown menu -->
    <div class="top-left-edition">
      <el-dropdown trigger="hover" class="custom-dropdown">
        <span class="el-dropdown-link user-info">
          <i class="el-icon-user" style="font-size: 23px"></i>
          <span id="name">{{ username }}</span> <!-- Displays the username -->
        </span>
        <!-- Dropdown menu for user options -->
        <el-dropdown-menu slot="dropdown" class="custom-dropdown-menu">
          <el-dropdown-item @click.native="goUserPage" class="custom-dropdown-item">Change Password</el-dropdown-item>
          <el-dropdown-item divided @click.native="goFrontPage" class="custom-dropdown-item">Exit</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>

    <!-- Middle section with navigation links -->
    <nav class="middle">
      <router-link to="/uploadPage" class="nav-link">Upload</router-link>
      <router-link to="/timeCapsule" class="nav-link">TimeCapsule</router-link>
    </nav>

    <!-- Right section with the project name and home button -->
    <div id="word">
      <h1>{{ msg }}</h1>
      <i class="el-icon-s-home home-icon" v-on:click="goMainPage"></i> <!-- Home icon to navigate to the main page -->
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';

  export default {
    name: "Header",
    computed: {
      // Get the username from the Vuex store
      ...mapGetters(['getUsername']),
      username() {
        return this.getUsername;  // Return the stored username
      }
    },
    data() {
      return {
        msg: "Precision Agriculture: DPIRD AgriVision",  // The header message
        activeIndex: "2",  // Default active menu index
      };
    },
    methods: {
      // Navigate to the front page
      goFrontPage() {
        this.$router.push({
          path: "/frontPage",
          name: "frontPage",
        });
      },
      // Navigate to the main page
      goMainPage() {
        this.$router.push('/mainPage');
      },
      // Navigate to the user page for changing password
      goUserPage(){
        this.$router.push({
          path: "/userPage",
          name: "userPage",
        });
      }
    },
  };
</script>

<style scoped>
  /* Main header styling */
  #Header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0px 40px;
    width: 90%;
    margin: 10px auto;
    background-color: #36471f;
    color: white;
  }

  /* Right section with project name and home button */
  #word {
    display: flex;
    align-items: center;
    margin: 0;
  }

  h1 {
    color: white;
    letter-spacing: 1px;
    font-size: 1.8em;
    margin-right: 10px;
  }

  /* User info and icon styling */
  .user-info {
    font-size: 20px;
    color: white;
    line-height: 24px;
    cursor: pointer;
  }

  #name {
    margin-left: 5px;
  }

  /* Navigation links styling */
  .nav-link {
    margin: 0 15px;
    text-decoration: none;
    font-size: 20px;
    color: white;
  }

  .nav-link:hover {
    color: #d9f0ea;  /* Change color on hover */
  }

  /* Home icon styling */
  .home-icon {
    font-size: 30px;
    cursor: pointer;
    color: white;
  }

  .home-icon:hover {
    color: #d9f0ea;  /* Change color on hover */
  }

  /* Custom styles for dropdown menu */
  .custom-dropdown-menu {
    margin-left: 50px;
  }

  .custom-dropdown-item {
    color: black;
    font-family: "Helvetica Neue";
  }
</style>
