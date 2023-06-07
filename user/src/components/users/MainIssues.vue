<template lang="">
  <div>
    <div class="main-container">
      <div class="main-header">
        我的提问
      </div>
      <div class="main-body">
        <div class="main-body-item" v-for="issue in issues" :key="issue.id">
          <el-row>
            <el-text size="large" tag="b" class="mx-1 issue-title">
              <el-icon><QuestionFilled /></el-icon>
              {{ issue.issue_title }}
            </el-text>
          </el-row>
          <el-row justify="space-between">
            <el-text @click="jumpIssus(issue.id)" class="mx-1" type="info">创建于&nbsp;{{ issue.create_time }}</el-text>
            <el-text @click="jumpSpace" class="mx-1 space" type="info">所属空间:&nbsp;{{ issue.space_name }}</el-text>
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

let issues = reactive(new Array())

let userid = -1;

const jumpIssus = (id) => {
  _this.$router.push({
    name: 'detail',
    query: {
      id: id,
      type: 'questions'
    }
  })
}

const jumpSpace = () => {
  _this.$router.push({
    name: 'space'
  })
}

onMounted(() => {
  api.get('give').then(res => {
    if (res.data.error == 1) {
      userid = res.data.data;
    } else {
      return;
    }
    api.get('user/' + userid.toString() + '/questions').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          issues.push({
            id: data.id,
            space_name: data.space_name,
            issue_title: data.question_title,
            create_time: data.create_time,
            from_space_id: data.from_space_id
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

.issue-title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.space:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>