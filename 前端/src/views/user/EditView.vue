<template lang="">
  <div class="backcc">
    <div class="edit-container">
      <div class="edit-box">
        <el-row style="display: flex; justify-content: end;">
          <el-text class="mx-1 back" type="info" @click="back">返回个人主页>></el-text>
        </el-row>
        <el-form
          :label-position="labelPosition"
          label-width="120px"
          :model="formLabelAlign"
          
        >
          <el-form-item label="昵称">
            <el-input v-model="formLabelAlign.username" />
          </el-form-item>
          <el-form-item label="性别">
            <el-select v-model="formLabelAlign.gender" class="m-2" placeholder="Select">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="个人标签">
            <el-input v-model="formLabelAlign.tags" />
          </el-form-item>
          <el-form-item label="现居地">
            <el-input v-model="formLabelAlign.address" />
          </el-form-item>
          <el-form-item label="职业/所在行业">
            <el-input v-model="formLabelAlign.job" />
          </el-form-item>
          <el-form-item label="所在学校/单位">
            <el-input v-model="formLabelAlign.organization" />
          </el-form-item>
          <el-form-item label="个人简介" type="textarea">
            <el-input v-model="formLabelAlign.intro" />
          </el-form-item>
        </el-form>
        <el-row style="display: flex; justify-content: center;">
          <el-button @click="submit" type="primary">
            保存
          </el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref, onMounted, getCurrentInstance } from 'vue';
import api from '@/plugins/axiosInstance';
import { ElMessage } from 'element-plus';

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

const labelPosition = ref('left')

const options = [
  {
    value: 0,
    label: '男'
  },
  {
    value: 1,
    label: '女'
  }
]

const formLabelAlign = reactive({
  username: '',
  gender: 0,
  tags: '',
  address: '',
  job: '',
  organization: '',
  intro: ''
})

const back = () => {
  _this.$router.push({
    name: 'users',
    params: {
      id: userid
    }
  })
}

const submit = () => {
  const formData = new FormData()
  formData.append('username', formLabelAlign.username)
  formData.append('gender', formLabelAlign.gender)
  formData.append('tags', formLabelAlign.tags)
  formData.append('destination', formLabelAlign.address)
  formData.append('job', formLabelAlign.job)
  formData.append('organization', formLabelAlign.organization)
  formData.append('intro', formLabelAlign.intro)
  api.post('user/' + userid.toString() + '/edit', formData).then(res => {
    if (res.data.error == 1) {
      ElMessage({
        message: '修改成功',
        type: 'success'
      })
      back()
    } else {
      ElMessage({
        message: '修改失败: ' + res.data.msg,
        type: 'error'
      })
      back()
    }
  }).catch(err => {
    ElMessage({
      message: '修改失败: ' + err.code,
      type: 'error'
    })
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
    api.get('user/' + userid.toString()).then(res => {
      if (res.data.error == 1) {
        const data = res.data;
        formLabelAlign.username = data.username;
        formLabelAlign.gender = data.gender;
        formLabelAlign.tags = data.tags;
        formLabelAlign.address = data.destination;
        formLabelAlign.job = data.job;
        formLabelAlign.organization = data.organization;
        formLabelAlign.intro = data.intro;
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
.backcc {
  width: 100%;
  height: 680px;
  background-color: #f5f5f5;
}

.edit-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.edit-box {
  width: auto;
  height: fit-content;
  border-radius: 8px;
  background-color: #fff;
  padding: 20px;
}

.back {
  margin-bottom: 10px;
}

.back:hover {
  color: #409eff;
  text-decoration: underline;
  cursor: pointer;
}
</style>