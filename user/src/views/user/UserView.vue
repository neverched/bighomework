<template lang="">
  <div>
    <MyHeader></MyHeader>
    <div class="con-box">
      <div class="container">
        <el-container>
          <el-header height="auto" style="padding: 0px">
            <UserHeader></UserHeader>
          </el-header>
          <el-container style="margin-top: 10px">
            <el-aside width="auto">
              <UserAside></UserAside>
            </el-aside>
            <el-main style="padding: 0px; margin-left: 10px; border-radius: 8px;">
              <UserMain></UserMain>
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
import UserMain from '@/components/users/UserMain.vue'

</script>
<style scoped>
.con-box {
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  display: flex;
  justify-content: center;
  /* align-items: center; */
}

.container {
  width: auto;
  margin-top: 5px;
  border-radius: 8px;
}
</style>