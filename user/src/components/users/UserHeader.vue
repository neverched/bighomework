<template>
  <div class="container">
    <div class="cover" @click="handleCoverClick">
      <img class="cover-img" :src="coverImg" alt="封面图片">
      <el-button round plain :icon="CameraFilled" class="cover-btn">
        上传封面图片
      </el-button>
    </div>
    <div class="profile">
      <el-row>
        <el-col :span="6">
          <el-avatar class="avatar" :src="avatarImg" :size="160" @click="handleClickAvatar"></el-avatar>
        </el-col>
        <el-col class="profile-info-box" :span="12">
          <el-row>
            <el-text style="color: black; font-size: large; font-weight: bold;">{{ info.name }}</el-text>
            <span class="my-space"></span>
            <el-tag v-if="info.gender" type="info" class="mx-1" effect="light" round>
              <el-icon class="info-cion" v-if="info.gender == 0" color="#409EFC">
                <Male />
              </el-icon>
              <el-icon class="info-cion" v-else color="#F56C6C">
                <Female />
              </el-icon>
              {{ gender2Chinese }}
            </el-tag>
            <span class="my-space"></span>
            <el-tag v-if="info.address" type="info" class="mx-1" effect="light" round>
              <el-icon class="info-cion" color="#f8e3c5">
                <Location />
              </el-icon>
              {{ info.address }}
            </el-tag>
          </el-row>
          <br />
          <el-row>
            <el-descriptions :column="1">
              <el-descriptions-item v-if="info.profession" label="职业/所在行业">{{ info.profession }}</el-descriptions-item>
              <el-descriptions-item v-if="info.company" label="所在学校/单位">{{ info.company }}</el-descriptions-item>
              <el-descriptions-item v-if="info.profile" label="个人简介">{{ info.profile }}</el-descriptions-item>
            </el-descriptions>
          </el-row>
        </el-col>
        <el-col class="edit-btn-box" :span="6">
          <el-button class="edit-btn" type="primary" plain @click="handleEditClick">
            编辑个人资料
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script setup>
// import { Male, Female } from '@element-plus/icons-vue/dist/types';
import { reactive, computed, onMounted, getCurrentInstance } from 'vue'
import api from '@/plugins/axiosInstance'

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

let coverImg = require('@/assets/default_user_cover.jpg'); // 封面图片
let avatarImg = require('@/assets/minecraft-creeper-face.png'); // 头像图片

const info = reactive({
  name: 'Zhang San',
  gender: 0,
  address: '北京市',
  profession: '软件工程',
  company: '北京航空航天大学',
  profile: '简介test'
})

const handleCoverClick = () => {
  console.log('cover click')
}

const handleEditClick = () => {
  console.log('edit click')
  _this.$router.push({
    name: 'edit',
    params: {
      id: _this.$route.params.id
    }
  })
}

const handleClickAvatar = () => {
  console.log('avatar click')
}

const gender2Chinese = computed(() => {
  return info.gender == 0 ? '男' : '女';
})

let userid = -1;

onMounted(() => {
  api.get('give').then(res => {
    if (res.data.error == 1) {
      userid = res.data.data;
    } else {
      return;
    }
    api.get('user/' + userid.toString()).then(res => {
      if (res.data.error == 1) {
        const data = res.data;
        info.name = data.username;
        info.gender = data.gender;
        info.address = data.destination;
        info.profession = data.job;
        info.company = data.organization;
        info.profile = data.intro;
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
.container {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.cover {
  width: 100%;
  border-radius: 8px 8px 0 0;
  background-color: #fff;
  position: relative;
}

.cover:hover {
  cursor: pointer;
}

.cover-img {
  width: 100%;
  max-height: 240px;
  border-radius: 8px 8px 0 0;
  /*position: absolute;
  z-index: -1;*/
}

.cover-btn {
  position: absolute;
  z-index: 1;
  top: 0;
  right: 0;
  margin: 15px;
}

.profile {
  width: 100%;
  height: auto;
  box-sizing: border-box;
  border-radius: 0 0 8px 8px;
  background-color: #fff;
  padding: 10px;
  padding-bottom: 20px;
}

.profile-info-box {
  display: flex;
  flex-direction: column;
  justify-content: end;
  align-items: flex-start;
}

.info-cion {
  pointer-events: none;
}

.edit-btn-box {
  display: flex;
  justify-content: end;
  align-items: end;
}

.my-space {
  width: 10px;
}

.avatar {
  transition: filter 0.5s ease;
}

.avatar:hover {
  cursor: pointer;
  filter: brightness(75%);
}
</style>