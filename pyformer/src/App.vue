<template>
  <div id="app">
    <Navbar v-if="showNavbar"></Navbar>

    <el-col style="margin-top: 10px">
      <router-view/>
    </el-col>

  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      user: 'asdf'
    }
  },
  computed: {
    showNavbar() {
      // 判断当前路由是否是登录页面，如果是登录页，则不显示 Navbar
      return this.$route.path !== '/login';
    },
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.logo {
  height: 50px;
}
</style>
