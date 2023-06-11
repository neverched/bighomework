<template lang="">
  <div>
    <div class="main-container">
      <div class="main-header">
        我的回答
      </div>
      <div class="main-body">
        <div class="main-body-item" v-for="answer in answers" :key="answer.id">
          <el-row>
            <el-text @click="jumpUp(answer.element_id, answer.type)" size="large" tag="b" class="mx-1 answer-title">
              {{ answer.issue_title }}
            </el-text>
          </el-row>
          <el-row style="margin-top: 5px; margin-bottom: 5px;">
            <el-text truncated>{{ answer.content }}</el-text>
          </el-row>
          <el-row justify="space-between">
            <el-text class="mx-1" type="info">创建于&nbsp;{{ answer.create_time }}</el-text>
            <el-text @click="jumpSpace" class="mx-1 space" type="info">所属空间:&nbsp;{{ answer.space_name }}</el-text>
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
  // console.log('route', _this.$route);
}

let answers = reactive(new Array())

let userid = -1;

const jumpUp = (eleId, type) => {
  _this.$router.push({
    name: 'detail',
    query: {
      id: eleId,
      type: type
    }
  })
}

const jumpSpace = () => {
  _this.$router.push({
    name: 'space'
  })
}

onMounted(() => {
  // console.log('id', _this.$route.params.id);
  api.get('give').then(res => {
    if (res.data.error == 1) {
      userid = res.data.data;
    } else {
      return;
    }
    api.get('user/' + userid.toString() + '/answers').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          answers.push({
            id: data.id,
            issue_title: data.issue_title,
            space_name: data.space_name,
            content: data.content,
            create_time: data.create_time,
            from_space_id: data.from_space_id,
            element_id: data.element_id,
            type: data.type
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
  }).catch(err => {
    console.log(err);
  })
})

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

.answer-title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.space:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>