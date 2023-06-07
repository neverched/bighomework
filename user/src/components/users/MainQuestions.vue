<template lang="">
  <div>
    <div class="main-container">
      <div class="main-header">
        我的习题
      </div>
      <div class="main-body">
        <div class="main-body-item" v-for="question in questions" :key="question.id">
          <el-row>
            <el-text @click="jumpQu(question.id)" size="large" tag="b" class="mx-1 question-title">
              {{ question.content }}
            </el-text>
            <el-tag class="ml-2" :type="difficultyType(question.difficulty)" style="margin-left: 5px;">{{ question.difficulty }}</el-tag>
          </el-row>
          <el-row justify="space-between">
            <el-text class="mx-1" type="info">创建于&nbsp;{{ question.create_time }}</el-text>
            <el-text @click="jumpSpace" class="mx-1 space" type="info">所属空间:&nbsp;{{ question.space_name }}</el-text>
          </el-row>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, computed, onMounted, getCurrentInstance } from 'vue';
import api from '@/plugins/axiosInstance';

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

let questions = reactive(new Array())

const difficultyType = computed(() => (d) => {
  if (d == '简单') {
    return 'success';
  } else if (d == '中等') {
    return 'warning';
  } else if (d == '困难') {
    return 'danger'
  }
  return ''
})

const jumpQu = id => {
  _this.$router.push({
    name: 'detail',
    query: {
      id: id,
      type: 'exercises'
    }
  })
}

const jumpSpace = () => {
  _this.$router.push({
    name: 'space'
  })
}

let userid = -1;

onMounted(() => {
  api.get('give').then(res => {
    if (res.data.error == 1) {
      userid = res.data.data;
    } else {
      return;
    }
    api.get('user/' + userid.toString() + '/exercises').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          questions.push({
            id: data.uid,
            space_name: data.space_name,
            content: data.content,
            create_time: data.create_time,
            from_space_id: data.from_space_id,
            difficulty: data.difficulty
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

.question-title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.space:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>