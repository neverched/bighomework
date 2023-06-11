<template>
  <div>
    <div class="main-container">
      <el-tabs v-model="activeName" class="demo-tabs" @tab-change="handleTabsChange">
        <el-tab-pane label="动态" name="activities"></el-tab-pane>
        <el-tab-pane label="空间" name="spaces"></el-tab-pane>
        <el-tab-pane label="资源" name="docs"></el-tab-pane>
        <el-tab-pane label="提问" name="issues"></el-tab-pane>
        <el-tab-pane label="回答" name="answers"></el-tab-pane>
        <el-tab-pane label="习题" name="questions"></el-tab-pane>
        <el-tab-pane label="收藏" name="collections"></el-tab-pane>
        <el-tab-pane label="关注" name="following"></el-tab-pane>
      </el-tabs>
      <router-view @changeUserMainTabs="handleSon"></router-view>
      <div class="main-footer">
        <el-text class="mx-1" type="info">没有更多了</el-text>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, getCurrentInstance, onMounted } from 'vue'

const instance = getCurrentInstance()

let activeName = ref('activities')

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

const handleTabsChange = (name) => {
  console.log('name', name);
  if (activeName.value == 'following') {
    _this.$router.push({
      name: activeName.value,
      params: {
        type: 'follows'
      }
    })
  } else {
    _this.$router.push({
      name: activeName.value
    })
  }

}

const handleSon = (type) => {
  console.log('type', type);
}

onMounted(() => {
  activeName.value = 'activities'
  _this.$router.push({ name: 'activities' })
})

</script>
<style scoped>
.main-container {
  width: 790px;
  background-color: #fff;
  border-radius: 8px;
}

.demo-tabs {
  margin-left: 20px;
  margin-right: 20px;
}

.main-footer {
  height: 50px;
  margin-left: 20px;
  margin-left: 20px;
  font-size: larger;
  font-weight: bolder;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>