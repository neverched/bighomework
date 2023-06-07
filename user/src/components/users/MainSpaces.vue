<template lang="">
  <div>
    <div class="main-container">
      <el-tabs v-model="activeName" class="demo-tabs main-header">
        <el-tab-pane label="管理" name="admin"></el-tab-pane>
        <el-tab-pane label="关注" name="collection"></el-tab-pane>
      </el-tabs>
      <div class="main-body">
        <div v-if="activeName == 'admin'">
          <div class="main-body-item" v-for="space in adminSpaces" :key="space.space_name">
            <el-row>
              <el-col :span="2">
                <el-avatar shape="square" :size="large" :src="coverImg" />
              </el-col>
              <el-col :span="18">
                <el-row style="flex-wrap: wrap;">
                  <el-text @click="jumpSpace" class="space-title" size="large" tag="b">{{ space.space_name }}</el-text> - <el-text class="space-title" type="info">{{ space.creator_name }}</el-text>
                  <el-tag style="margin-left: 5px; margin-right: 5px" v-for="tag in space.tags" :key="tag" type="info" class="mx-1" effect="light">
                    {{ tag }}
                  </el-tag>
                </el-row>
                <el-row>
                  <el-text truncated>{{ space.space_introduction }}</el-text>
                </el-row>
              </el-col>
              <el-col :span="4">
                <el-row>
                  <el-text type="info" style="margin-right: 5px">
                    <el-icon><Opportunity /></el-icon>
                    0
                  </el-text>
                  <el-text type="info" style="margin-right: 5px">
                    <el-icon><View /></el-icon>
                    0
                  </el-text>
                  <el-tooltip
                    v-if="space.type == 'public'"
                    class="box-item"
                    effect="dark"
                    content="公开-该空间可被任何人访问"
                    placement="bottom-end"
                  >
                    <el-text type="info">
                      <el-icon><Connection /></el-icon>
                    </el-text>
                  </el-tooltip>
                  <el-tooltip
                    v-else
                    class="box-item"
                    effect="dark"
                    content="私有-私有空间只对空间成员开放"
                    placement="bottom-end"
                  >
                    <el-text type="info">
                      <el-icon><Lock /></el-icon>
                    </el-text>
                  </el-tooltip>
                </el-row>
                <el-row>
                  <el-text type="info">创建于 {{ space.create_time }}</el-text>
                </el-row>
              </el-col>
            </el-row>
          </div>
        </div>
        <div v-else>
          <div class="main-body-item" v-for="space in collectionSpaces" :key="space.space_name">
            <el-row>
              <el-col :span="2">
                <el-avatar shape="square" :size="large" :src="coverImg" />
              </el-col>
              <el-col :span="18">
                <el-row style="flex-wrap: wrap;">
                  <el-text @click="jumpSpace" class="space-title" size="large" tag="b">{{ space.space_name }}</el-text> - <el-text class="space-title" type="info">{{ space.admin }}</el-text>
                  <el-tag style="margin-left: 5px; margin-right: 5px" v-for="tag in space.tags" :key="tag" type="info" class="mx-1" effect="light">
                    {{ tag }}
                  </el-tag>
                </el-row>
                <el-row>
                  <el-text truncated>{{ space.space_introduction }}</el-text>
                </el-row>
              </el-col>
              <el-col :span="4">
                <el-row>
                  <el-text type="info" style="margin-right: 5px">
                    <el-icon><Opportunity /></el-icon>
                    0
                  </el-text>
                  <el-text type="info" style="margin-right: 5px">
                    <el-icon><View /></el-icon>
                    0
                  </el-text>
                  <el-tooltip
                    v-if="space.type == 'public'"
                    class="box-item"
                    effect="dark"
                    content="公开-该空间可被任何人访问"
                    placement="bottom-end"
                  >
                    <el-text type="info">
                      <el-icon><Connection /></el-icon>
                    </el-text>
                  </el-tooltip>
                  <el-tooltip
                    v-else
                    class="box-item"
                    effect="dark"
                    content="私有-私有空间只对空间成员开放"
                    placement="bottom-end"
                  >
                    <el-text type="info">
                      <el-icon><Lock /></el-icon>
                    </el-text>
                  </el-tooltip>
                </el-row>
                <el-row>
                  <el-text type="info">创建于 {{ space.create_time }}</el-text>
                </el-row>
              </el-col>
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

let coverImg = require('@/assets/10001.default_product_avatar.jpg')

let activeName = ref('admin')

let collectionSpaces = reactive(new Array())

let adminSpaces = reactive(new Array())

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
    api.get('user/' + userid.toString() + '/adminspaces').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          data.type = 'public'
          adminSpaces.push(data)
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('user/' + userid.toString() + '/followspaces').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          data.type = 'public'
          collectionSpaces.push(data)
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

.space-title:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
