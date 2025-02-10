<template>
  <div class="protected-container">
    <h2>Welcome to the Protected Page</h2>
    <p>This is a protected route, accessible only with a valid token.</p>
    <el-button @click="logout">Logout</el-button>
  </div>
</template>

<script>
import {axGet} from '@/utils'
export default {
  created() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push('/'); // 如果没有 token，则跳转回登录页面
    }
    axGet('/protected').then((response) => {
      console.log(response.data())
    })
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/'); // 退出登录后跳转回登录页面
    },
  },
};
</script>

<style scoped>
.protected-container {
  text-align: center;
  margin-top: 100px;
}
</style>
