<template lang="">
  <div>
    <div class="main-container">
      <el-tabs v-model="activeName" class="demo-tabs main-header">
        <el-tab-pane label="空间资源" name="space"></el-tab-pane>
        <el-tab-pane label="提问" name="issue"></el-tab-pane>
        <el-tab-pane label="回答" name="answer"></el-tab-pane>
        <el-tab-pane label="习题" name="question"></el-tab-pane>
      </el-tabs>
      <div class="main-body">
        <div v-if="activeName == 'space'">
          <div class="main-body-item" v-for="doc in spaceDocs" :key="doc.title">
            <el-row style="flex-wrap: wrap;">
              <el-text @click="jump(doc.id, 'resources')" class="title" tag="b">
                <el-icon><Document /></el-icon>
                {{ doc.title }}
              </el-text>
              <el-tag style="margin-left: 5px; margin-right: 5px" v-for="tag in doc.tags" :key="tag" type="info" class="mx-1" effect="light">
                {{ tag }}
              </el-tag>
            </el-row>
            <el-row style="justify-content: space-between">
              <el-text type="info">创建于 {{ doc.date }}</el-text>
              <el-text @click="jumpSpace" class="space" type="info">所属空间: {{ doc.space }}</el-text>
            </el-row>
          </div>
        </div>
        <div v-else-if="activeName == 'issue'">
          <div class="main-body-item" v-for="issue in issues" :key="issue.id">
            <el-row>
              <el-text @click="jump(issue.id, 'questions')" size="large" tag="b" class="mx-1 title">
                <el-icon><QuestionFilled /></el-icon>
                {{ issue.issue_title }}
              </el-text>
            </el-row>
            <el-row justify="space-between">
              <el-text class="mx-1" type="info">创建于&nbsp;{{ issue.create_time }}</el-text>
              <el-text @click="jumpSpace" class="mx-1 space" type="info">所属空间:&nbsp;{{ issue.space_name }}</el-text>
            </el-row>
          </div>
        </div>
        <div v-else-if="activeName == 'answer'">
          <div class="main-body-item" v-for="answer in answers" :key="answer.id">
            <el-row>
              <el-text size="large" tag="b" class="mx-1 title">
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
        <div v-else>
          <div class="main-body-item" v-for="question in questions" :key="question.id">
            <el-row>
              <el-text @click="jump(question.id, 'exercises')" size="large" tag="b" class="mx-1 title">
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
  </div>
</template>
<script setup>
import { reactive, ref, computed, onMounted, getCurrentInstance } from 'vue';
import api from '@/plugins/axiosInstance'

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

let activeName = ref('space')

let spaceDocs = reactive(new Array())

let issues = reactive(new Array())

let answers = reactive(new Array())

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

const jumpSpace = () => {
  _this.$router.push({
    name: 'space'
  })
}

const jump = (id, type) => {
  _this.$router.push({
    name: 'detail',
    query: {
      id,
      type
    }
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
    api.get('user/' + userid.toString() + '/collects/resources').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          spaceDocs.push({
            id: data.id,
            space_name: data.space_name,
            create_time: data.create_time,
            title: data.file_name,
            from_space_id: data.from_space_id,
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('user/' + userid.toString() + '/collects/questions').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          issues.push({
            id: data.id,
            space_name: data.space_name,
            issue_title: data.question_title,
            create_time: data.create_time,
            from_space_id: data.from_space_id,
            uid: data.uid
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('user/' + userid.toString() + '/collects/answers').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          answers.push({
            id: data.id,
            space_name: data.space_name,
            content: data.content,
            create_time: data.create_time,
            from_space_id: data.from_space_id,
            uid: data.uid
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('user/' + userid.toString() + '/collects/exercises').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          questions.push(data)
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
  /* border-bottom: 1px solid #ebebeb; */
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

.title:hover {
  text-decoration: underline;
  cursor: pointer;
}

/* .title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.title:hover {
  text-decoration: underline;
  cursor: pointer;
} */

.space:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
