<template lang="">
  <div class="container">
    <div class="form-area">
      <el-row style="display: flex; justify-content: end;">
        <el-text class="mx-1 back" type="info" @click="back">返回主页>></el-text>
      </el-row>
      <el-form class="form-all" label-position="top" :model="form" label-width="100px">
        <el-form-item class="input-item" label="昵称" >
          <el-input class="input" v-model="form.username" type="text" disabled></el-input>
        </el-form-item>
        <el-form-item class="input-item" label="新密码" >
          <el-input class="input" v-model="form.password1" placeholder="新密码(8~18位, 同时有且仅有字母与数字)" type="password"
            show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item" label="密码确认" >
          <el-input class="input" v-model="form.password2" placeholder="请再次输入密码" type="password"
            show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button class="input" @click="handleClick" type="primary" style="width: 100%">确认</el-button>
          <!-- <el-button class="input" @click="handleClickLogout" type="primary" style="width: 100%">登出</el-button> -->
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script setup>
import { reactive, onMounted, getCurrentInstance } from 'vue';
import api from '@/plugins/axiosInstance';
import { ElMessage } from 'element-plus';

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

const form = reactive({
  username: '昵称',
  password1: '',
  password2: '',
})

onMounted(() => {
  api.get('give').then(res => {
    if (res.data.error === 1) {
      userid = res.data.data;
      api.get('user/' + userid.toString()).then(res => {
        if (res.data.error === 1) {
          const data = res.data;
          form.username = data.username;
        }
      }).catch(err => {
        console.log(err);
      })
    } else {
      ElMessage.error('获取用户信息失败: ' + res.data.msg)
      return;
    }
  }).catch(err => {
    console.log(err);
    return;
  })
})

const back = () => {
  _this.$router.push('/')
}

const isPasswordLegal = (password) => {
  const reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$/
  return reg.test(password)
}

let userid = -1

const handleClick = () => {
  if (!isPasswordLegal(form.password1)) {
    ElMessage.error('密码格式不合法')
    return
  }
  if (form.password1 !== form.password2) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  api.get('give').then(res => {
    if (res.data.error === 1) {
      const formData = new FormData()
      formData.append('newPass', form.password1)
      api.post('changepassword', formData).then(res => {
        if (res.data.error === 1) {
          ElMessage.success('修改成功')
          back()
        } else {
          ElMessage.error('修改失败: ' + res.data.msg)
        }
      }).catch(err => {
        ElMessage.error('修改失败: ' + err.code);
        console.log(err);
      })
    } else {
      ElMessage.error('修改失败: ' + res.data.msg)
    }
  }).catch(err => {
    console.log('give err', err);
    ElMessage.error('修改失败: ' + err.code);
  })
}

</script>
<style scoped>
.container {
  width: 100%;
  /* height: 760px; */
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.form-area {
  width: 400px;
  /*height: 400px;*/
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 100px;
}


.form-all {
  margin-top: 20px;
  width: 100%;
  padding-left: 20px;
  padding-right: 20px;
  align-items: center;
}

.input-item {
  padding-left: 20px;
  padding-right: 20px;
}

.input {
  height: 40px;
}

.back {
  margin-top: 20px;
  margin-bottom: 10px;
}

.back:hover {
  color: #409eff;
  text-decoration: underline;
  cursor: pointer;
}
</style>