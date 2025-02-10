<template>
  <div>
    <el-row>
      <el-menu
        class="el-menu-demo"
        mode="horizontal"
        router
        background-color="#025C67"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-col :span="4">
          <p style="color: aliceblue">PipeLine Desk</p>
        </el-col>
        <el-col :span="4">
          <el-menu-item index="/area/list">台区经理</el-menu-item>
        </el-col>
        <el-col :span="4">
          <el-menu-item index="/area/add">增加台区</el-menu-item>
        </el-col>
        <el-col :span="4">
          <el-menu-item index="/area/query">上传工单</el-menu-item>
        </el-col>
        <el-col :span="4">
          <el-submenu index="/gongdan/list">
            <template slot="title">工单列表</template>
            <el-menu-item index="/gongdan/list/guzhang">故障工单</el-menu-item>
            <el-menu-item index="/gongdan/list/fuwu">服务工单</el-menu-item>
            <el-menu-item index="/gongdan/list/neibu">内部工单</el-menu-item>
          </el-submenu>
        </el-col>
        <el-col :span="4">
          <el-menu-item index="/">用户：{{ user }}</el-menu-item>
        </el-col>
      </el-menu>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return {
      user: localStorage.getItem('token') || '未登录',
    };
  },
}
</script>

<style scoped>
.logo {
  height: 50px;
}
</style>
