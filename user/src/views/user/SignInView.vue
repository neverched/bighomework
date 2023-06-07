<template>
  <div class="container">
    <img :src="url" alt="logo" />
    <div v-show="activeForm == 'login'" class="form-area">
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1" class="navi-item">密码登录</el-menu-item>
        <el-menu-item index="2" class="navi-item">验证码登录</el-menu-item>
      </el-menu>
      <el-form v-show="activeIndex == 1" class="form-all" label-position="left" :model="form" label-width="0px">
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.email" placeholder="邮箱" type="email"></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.password" placeholder="密码(8~18位, 有且仅有字母与数字)" type="password"
            show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button class="input" @click="handleClickPassLogin" type="primary" style="width: 100%">登录</el-button>
          <!-- <el-button class="input" @click="handleClickLogout" type="primary" style="width: 100%">登出</el-button> -->
        </el-form-item>
      </el-form>
      <el-form v-show="activeIndex == 2" class="form-all" label-position="left" :model="form" label-width="0px">
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.email" placeholder="邮箱" type="email"></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <div class="verify-code-box">
            <el-input class="input" v-model="form.code" placeholder="验证码"></el-input>
            <span :style="verifyCodeStyle" @click="handleClickVerifyCodeLogin" class="verify-code-btn">{{ verifyCodeBtn
            }}</span>
          </div>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button @click="handleClickCodeLogin" class="input" type="primary" style="width: 100%">登录</el-button>
        </el-form-item>
      </el-form>
      <span class="login-signin" @click="handleChangeLogin">
        {{ loginSignInMsg }}
      </span>
    </div>
    <div v-show="activeForm == 'register'" class="form-area">
      <el-menu :default-active="'1'" class="el-menu-demo" mode="horizontal">
        <el-menu-item index="1" class="navi-item">账号注册</el-menu-item>
      </el-menu>
      <el-form class="form-all" label-position="left" :model="form" label-width="0px">
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.name" placeholder="昵称" type="text"></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.email" placeholder="邮箱" type="email"></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.password" placeholder="密码(8~18位, 有且仅有字母与数字)" type="password"
            show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.confirmPassword" placeholder="确认密码" type="password"
            show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <div class="verify-code-box">
            <el-input class="input" v-model="form.code" placeholder="验证码"></el-input>
            <span :style="verifyCodeStyle" @click="handleClickVerifyCode" class="verify-code-btn">{{ verifyCodeBtn
            }}</span>
          </div>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button class="input" @click="handleClickRegister" type="primary" style="width: 100%">注册</el-button>
        </el-form-item>
      </el-form>
      <span class="login-signin" @click="handleChangeLogin">
        {{ loginSignInMsg }}
      </span>
    </div>
  </div>
</template>
<script>
import { reactive, ref, computed, getCurrentInstance } from 'vue'
import api from '@/plugins/axiosInstance'
import { ElMessage } from 'element-plus'

export default {
  name: 'SignInView',
  setup() {
    const instance = getCurrentInstance();

    let _this = null

    if (instance != null) {
      _this = instance.appContext.config.globalProperties //vue3获取当前this
    }

    let url = ref('https://vue.learnerhub.net/static/img/logo1.c54dc75.png')
    let form = reactive({
      name: '',
      email: '',
      password: '',
      confirmPassword: '',
      code: ''
    })
    let activeIndex = ref('1')
    let activeForm = ref('login')
    let verifyCodeBtn = ref('获取验证码')
    let verifyCodeStyle = ref('pointer-events:auto;')

    const loginSignInMsg = computed(() => {
      return activeForm.value == 'login' ? '还没有账号?立即注册>>' : '已有账号?立即登录>>'
    })

    const handleSelect = (index) => {
      console.log(index)
      activeIndex.value = index
    }

    const handleChangeLogin = () => {
      if (activeForm.value == 'login') {
        activeForm.value = 'register'
        console.log('跳转到注册页面, activeForm.value:', activeForm.value)
      } else {
        activeForm.value = 'login'
        console.log('跳转到登录页面, activeForm.value:', activeForm.value)
      }
    }

    const handleClickPassLogin = () => {
      if (!form.email) {
        alert('邮箱不能为空')
      } else if (!isEmailLegal(form.email)) {
        alert('邮箱格式不正确')
      } else if (!form.password) {
        alert('密码不能为空')
      } else if (!isPasswordLegal(form.password)) {
        alert('密码格式不正确')
      } else {
        passLogin()
      }
    }

    const passLogin = () => {
      const formData = new FormData()
      formData.append('email', form.email)
      formData.append('password', form.password)
      api.post('login', formData).then(res => {
        if (res.data.error == 1) {
          clearForm(form)
          ElMessage({
            message: '登陆成功',
            type: 'success',
          })
          //TODO: 跳转到主界面
          _this.$router.push('/');
        } else {
          ElMessage({
            message: '登陆失败: ' + res.data.msg,
            type: 'error',
          })
        }
      }).catch(err => {
        console.log('登录失败', err)
        ElMessage({
          message: '登陆失败:' + err.code,
          type: 'error',
        })
        clearForm(form)
      })
    }

    const handleClickCodeLogin = () => {
      const formData = new FormData()
      formData.append('code', form.code)
      api.post('loginbyconfirm', formData).then(res => {
        if (res.data.error == 1) {
          clearForm(form)
          ElMessage({
            message: '登陆成功',
            type: 'success',
          })
          //TODO: 跳转到主界面
          _this.$router.push('/');
        } else {
          ElMessage({
            message: '登陆失败: ' + res.data.msg,
            type: 'error',
          })
        }
      }).catch(err => {
        console.log('登录失败', err)
        ElMessage({
          message: '登陆失败:' + err.code,
          type: 'error',
        })
        clearForm(form)
      })
    }

    const isEmailLegal = (email) => {
      const reg = /^([a-zA-Z]|[0-9])(\w|-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
      return reg.test(email)
    }

    const isPasswordLegal = (password) => {
      const reg = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,18}$/
      return reg.test(password)
    }

    const handleClickVerifyCodeLogin = () => {
      if (!form.email) {
        alert('邮箱不能为空')
      } else if (!isEmailLegal(form.email)) {
        alert('邮箱格式不正确')
      } else {
        handleGetCode(login_getCode)
      }
    }

    const handleClickVerifyCode = () => {
      if (!form.name) {
        alert('昵称不能为空')
      } else if (!form.email) {
        alert('邮箱不能为空')
      } else if (!isEmailLegal(form.email)) {
        alert('邮箱格式不正确')
      } else if (!form.password) {
        alert('密码不能为空')
      } else if (!isPasswordLegal(form.password)) {
        alert('密码格式不正确')
      } else if (!form.confirmPassword) {
        alert('请确认密码')
      } else if (form.password !== form.confirmPassword) {
        alert('两次密码不一致')
      } else {
        handleGetCode(reg_getCode)
      }
    }

    const handleGetCode = (getCode) => {
      getCode()
      let count = 60
      verifyCodeStyle.value = 'pointer-events:none;'
      const timer = setInterval(() => {
        if (count > 0) {
          count--
          verifyCodeBtn.value = count + 's后重新获取'
        } else {
          clearInterval(timer)
          verifyCodeBtn.value = '获取验证码'
          verifyCodeStyle.value = 'pointer-events:auto;'
        }
      }, 1000)
    }

    const reg_getCode = () => {
      const formData = new FormData()
      formData.append('username', form.name)
      formData.append('email', form.email)
      formData.append('password1', form.password)
      formData.append('password2', form.confirmPassword)
      api.post('register', formData).then(res => {
        console.log('获取验证码成功', res)
        if (res.data.error == 1) {
          ElMessage({
            message: '验证码已发送至邮箱, 请注意查收',
            type: 'success'
          })
        } else {
          ElMessage({
            message: '获取验证码失败: ' + res.data.msg,
            type: 'warning'
          })
        }
      }).catch(err => {
        console.log('获取验证码失败', err)
        ElMessage({
          message: '获取验证码失败, 请稍后重试',
          type: 'error'
        })
      })
    }

    const login_getCode = () => {
      const formData = new FormData()
      formData.append('email', form.email)
      api.post('login/confirm', formData).then(res => {
        console.log('获取验证码结果: ', res)
        if (res.data.error == 1) {
          ElMessage({
            message: '验证码已发送至邮箱, 请注意查收',
            type: 'success'
          })
        } else {
          ElMessage({
            message: '获取验证码失败: ' + res.data.msg,
            type: 'warning'
          })
        }
      }).catch(err => {
        console.log('获取验证码失败', err)
        ElMessage({
          message: '获取验证码失败, 请稍后重试',
          type: 'error'
        })
      })
    }

    const handleClickRegister = () => {
      if (!form.name) {
        alert('昵称不能为空')
      } else if (!form.email) {
        alert('邮箱不能为空')
      } else if (!isEmailLegal(form.email)) {
        alert('邮箱格式不正确')
      } else if (!form.password) {
        alert('密码不能为空')
      } else if (!isPasswordLegal(form.password)) {
        alert('密码格式不正确')
      } else if (!form.confirmPassword) {
        alert('请确认密码')
      } else if (form.password !== form.confirmPassword) {
        alert('两次密码不一致')
      } else if (!form.code) {
        alert('验证码不能为空')
      } else {
        handleRegister()
      }
    }

    const clearForm = (form) => {
      form.name = ''
      form.email = ''
      form.password = ''
      form.confirmPassword = ''
      form.code = ''
    }

    const handleRegister = () => {
      const formData = new FormData()
      formData.append('code', form.code)
      api.post('register/confirm', formData).then(res => {
        if (res.data.error == 1) {
          clearForm(form)
          ElMessage({
            message: '注册成功',
            type: 'success',
          })
        } else {
          ElMessage({
            message: '注册失败: ' + res.data.msg,
            type: 'error',
          })
        }
        clearForm(form)
        activeForm.value = 'login'
      }).catch(err => {
        console.log('注册失败', err)
        ElMessage({
          message: '注册失败: ' + err.code,
          type: 'error'
        })
        // clearForm(form)
      })
    }

    const handleClickLogout = () => {
      api({
        url: 'logout',
        method: 'post'
      }).then(res => {
        console.log('登出成功', res)
      }).catch(err => {
        console.log('登出失败', err)
      })
    }

    return {
      url,
      form,
      activeIndex,
      activeForm,
      verifyCodeBtn,
      loginSignInMsg,
      verifyCodeStyle,
      handleSelect,
      handleChangeLogin,
      handleClickVerifyCode,
      handleClickRegister,
      handleClickPassLogin,
      handleClickLogout,
      handleClickCodeLogin,
      handleClickVerifyCodeLogin
    }
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 700px;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  flex-direction: column;
}

img {
  width: 215px;
  margin-top: 100px;
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
}

.el-menu-demo {
  width: 100%;
  margin-top: 20px;
  padding-left: 20px;
}

.navi-item {
  color: #2E2E2E;
  font-size: 16px;
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

.login-signin {
  color: #909399;
  font-size: 13px;
}

.login-signin:hover {
  text-decoration: underline;
  cursor: pointer;
}

.verify-code-box {
  position: relative;
  width: 100%;
}

.verify-code-btn {
  color: #409eff;
  width: fit-content;
  position: absolute;
  z-index: 1;
  right: 0;
  top: 0;
  margin: 4px;
  margin-right: 10px;
}

.verify-code-btn:hover {
  /*width: 100px;*/
  color: #7dccf9;
  cursor: pointer;
}
</style>