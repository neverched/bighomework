<template lang="">
  <div>
    <div class="main-container">
      <el-tabs v-model="activeName" class="demo-tabs main-header">
        <el-tab-pane label="空间资源" name="space"></el-tab-pane>
        <el-tab-pane label="个人资源" name="person"></el-tab-pane>
      </el-tabs>
      <div class="main-body">
        <div v-if="activeName == 'space'">
          <div class="main-body-item" v-for="doc in spaceDocs" :key="doc.title">
            <el-row style="flex-wrap: wrap;">
              <el-text @click="jumpRe(doc.id)" class="doc-title" tag="b">
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
        <div v-else>
          <div class="main-body-item" v-for="doc in personDocs" :key="doc.title">
            <el-row style="flex-wrap: wrap;">
              <el-text @click="jumpRe(doc.id)" class="doc-title" tag="b">
                <el-icon><Document /></el-icon>
                {{ doc.title }}
                <el-icon><Lock /></el-icon>
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
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref, onMounted, getCurrentInstance } from 'vue';
import api from '@/plugins/axiosInstance'

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

let activeName = ref('space')

let spaceDocs = reactive(new Array())

let personDocs = reactive(new Array())

const jumpRe = id => {
  _this.$router.push({
    name: 'detail',
    query: {
      id: id,
      type: 'resources'
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
    api.get('user/' + userid.toString() + '/resources').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          personDocs.push({
            id: data.id,
            title: data.file_name,
            type: 'private',
            date: data.create_time,
            space: data.space_name,
            space_id: data.from_space_id
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('spaces/1/resources').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          personDocs.push({
            id: data.id,
            title: data.file_name,
            type: 'public',
            date: data.create_time,
            space: data.space_name,
            space_id: data.from_space_id
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

.doc-title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.space:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
