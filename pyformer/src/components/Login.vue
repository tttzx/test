<template>
  <div class="login-container">
    <el-col>
      <el-form :model="form" label-width="120px" class="login-form">
        <el-form-item label="Username" :rules="[{ required: true, message: 'Please input username', trigger: 'blur' }]">
          <el-input v-model="form.username" placeholder="Enter username"></el-input>
        </el-form-item>

        <el-form-item label="Password" :rules="[{ required: true, message: 'Please input password', trigger: 'blur' }]">
          <el-input type="password" v-model="form.password" placeholder="Enter password"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="login">Login</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </div>
</template>

<script>
import {axPost} from '@/utils'

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      axPost('/login', this.form).then((response) => {
        // 如果登录成功，保存 token 到 localStorage
        localStorage.setItem('token', response.data.token);
        this.$router.push('/protected'); // 登录成功后跳转到受保护的页面
      })
        .catch((error) => {
          console.error(error);
          this.$message.error('Invalid credentials');
        });
    },
  },
};
</script>

<style scoped>
.login-container {
  width: 400px;
  margin: 100px auto;
}
</style>
