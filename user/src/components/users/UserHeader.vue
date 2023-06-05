<template>
  <div class="container">
    <div class="cover" @click="handleCoverClick">
      <img class="cover-img" :src="coverImg" alt="封面图片">
      <el-button type="primary" plain :icon="CameraFilled" class="cover-btn">
        上传封面图片
      </el-button>
    </div>
    <div class="profile">
      <el-row>
        <el-col :span="6">
          <el-avatar :src="avatarImg" size="160px"></el-avatar>
        </el-col>
        <el-col :span="12">
          <el-row>
            <el-text size="large">{{ info.name }}</el-text>
            <el-tag v-if="info.gender" type="info" class="mx-1" effect="light" round>{{ gender2Chinese }}</el-tag>
            <el-tag v-if="info.address" type="info" class="mx-1" effect="light" round>{{ info.address }}</el-tag>
          </el-row>
          <el-row>
            <el-descriptions :column="1">
              <el-descriptions-item v-if="info.profession" label="职业/所在行业">{{ info.profession }}</el-descriptions-item>
              <el-descriptions-item v-if="info.company" label="所在学校/单位">{{ info.company }}</el-descriptions-item>
              <el-descriptions-item v-if="info.profile" label="个人简介">{{ info.profile }}</el-descriptions-item>
            </el-descriptions>
          </el-row>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" plain @click="handleEditClick">
            编辑个人资料
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<script setup>
// import { Male, Female } from '@element-plus/icons-vue/dist/types';
import { ref, reactive, computed } from 'vue'

let coverImg = ref(''); // 封面图片
let avatarImg = ref(''); // 头像图片

const info = reactive({
  name: 'Zhang San',
  gender: 'male',
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
}

const gender2Chinese = computed(() => {
  return info.gender == 'male' ? '男' : '女';
})

</script>
<style scoped>
.container {
  width: 100%;
  height: 470px;
  border-radius: 8px;
}

.cover {
  width: 100%;
  height: 240px;
  border-radius: 8px 8px 0 0;
}

.cover-img {
  width: 100%;
  position: absolute;
  z-index: -1;
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
  height: 230px;
  border-radius: 0 0 8px 8px;
  background-color: #fff;
  padding: 8px;
}
</style>