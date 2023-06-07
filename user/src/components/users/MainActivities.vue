<template lang="">
  <div>
    <div class="main-container">
      <div class="main-header">
        我的动态
      </div>
      <div class="main-body">
        <div class="main-body-item" v-for="activity in activities" :key="activity.title">
          <el-row>
            <el-text class="mx-1" type="info">{{ activity.title }}</el-text>
          </el-row>
          <el-row>
            <el-text @click="jump(activity.id, activity.type)" class="mx-1 item-content" size="large">{{ activity.content }}</el-text>
          </el-row>
          <el-row justify="space-between">
            <el-col :span="6">
              <el-text class="mx-1" type="info">创建于&nbsp;{{ activity.date }}</el-text>
            </el-col>
            <el-col :span="18" v-show="activity.space !== '不属于空间'" align="end">
              <el-text class="mx-1" type="info">所属空间:&nbsp;{{ activity.space }}</el-text>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, onMounted, getCurrentInstance } from 'vue';
import api from '@/plugins/axiosInstance'

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

let activities = reactive(new Array())

onMounted(() => {
  api.get('user/activities').then(res => {
    if (res.data.error == 1) {
      const datas = res.data.data;
      for (let data of datas) {
        activities.push({
          id: data.t_id,
          type: data.type,
          date: data.create_time,
          title: data.programs,
          content: data.title,
          space: data.space_name
        })
      }
    }
  }).catch(err => {
    console.log(err);
  })
})

const jump = (id, type) => {
  _this.$router.push({
    name: 'detail',
    query: {
      id: id,
      type: type
    }
  })
}

</script>
<style scoped>
.main-container {
  width: 100%;
  background-color: #fff;
}

.main-header {
  height: 50px;
  margin-left: 20px;
  margin-right: 20px;
  font-size: larger;
  font-weight: bolder;
  border-bottom: 1px solid #ebebeb;
}

.main-body-item {
  padding: 20px;
  border-bottom: 1px solid #ebebeb;
}

.item-content {
  font-size: larger;
  font-weight: bolder;
}

.item-content:hover {
  color: #409eff;
  cursor: pointer;
}
</style>