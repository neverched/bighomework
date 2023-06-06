<template lang="">
  <div>
    <MyHeader></MyHeader>
    <div class="con-box">
    <div class="container">
      <el-container>
        <el-header height="auto">
          <UserHeader></UserHeader>
        </el-header>
        <el-container>
          <el-aside width="150">
            <UserAside></UserAside>
          </el-aside>
          <el-main>
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>
    </div>
    </div>
  </div>
</template>
<script setup>
import MyHeader from '@/components/MyHeader.vue'
import UserAside from '@/components/users/UserAside.vue'
import UserHeader from '@/components/users/UserHeader.vue'

</script>
<style scoped>
.con-box {
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  /*align-items: center;*/
}

.container {
  width: 1070px;
  margin-top: 5px;
  border-radius: 8px;
}
</style>