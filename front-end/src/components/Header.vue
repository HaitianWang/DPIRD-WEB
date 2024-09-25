<template>
  <div id="Header">
    <div class="top-left-edition">
      <el-dropdown trigger="hover" class="custom-dropdown">
        <span class="el-dropdown-link user-info">
          <i class="el-icon-user" style="font-size: 23px"></i>
          <span id="name">{{ username }}</span>
        </span>
        <el-dropdown-menu slot="dropdown" class="custom-dropdown-menu">
          <el-dropdown-item @click.native="goUserPage" class="custom-dropdown-item">Change Password</el-dropdown-item>
          <el-dropdown-item divided @click.native="goFrontPage" class="custom-dropdown-item">Exit</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
    <nav class="middle">
      <router-link to="/uploadPage" class="nav-link">Upload</router-link>
      <router-link to="/timeCapsule" class="nav-link">TimeCapsule</router-link>
    </nav>
    <div id="word">
      <h1>{{ msg }}</h1>
      <i class="el-icon-s-home home-icon" v-on:click="goMainPage"></i>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';

  export default {
    name: "Header",
    computed: {
      ...mapGetters(['getUsername']),
      username() {
        return this.getUsername;
      }
    },
    data() {
      return {
        msg: "Precision Agriculture: DPIRD AgriVision",
        activeIndex: "2",
      };
    },
    methods: {
      goFrontPage() {
        this.$router.push({
          path: "/frontPage",
          name: "frontPage",
        });
      },
      goMainPage() {
        this.$router.push('/mainPage');
      },
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

  .el-menu-demo {
    width: 80%;
    margin: 0px auto;
    padding: 0px;
  }

  .user-info {
    font-size: 20px;
    color: white;
    line-height: 24px;
    cursor: pointer;
  }

  #name {
    margin-left: 5px;
  }

  .nav-link {
    margin: 0 15px;
    text-decoration: none;
    font-size: 20px;
    color: white;
  }

  .nav-link:hover {
    color: #d9f0ea;
  }

  .home-icon {
    font-size: 30px;
    cursor: pointer;
    color: white;
  }

  .home-icon:hover {
    color: #d9f0ea;
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
