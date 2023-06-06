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
          <el-input class="input" v-model="form.password" placeholder="密码" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button class="input" @click="passLogin()" type="primary" style="width: 100%">登录</el-button>
        </el-form-item>
      </el-form>
      <el-form v-show="activeIndex == 2" class="form-all" label-position="left" :model="form" label-width="0px">
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.email" placeholder="邮箱" type="email"></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.code" placeholder="验证码">
            <template #append>
              <span class="verify-code-btn">{{ verifyCodeBtn }}</span>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button class="input" type="primary" style="width: 100%">登录</el-button>
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
          <el-input class="input" v-model="form.password" placeholder="密码" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-input class="input" v-model="form.code" placeholder="验证码">
            <template #append>
              <span @click="checkEmail(form.code)" class="verify-code-btn">{{ verifyCodeBtn }}</span>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item class="input-item">
          <el-button class="input" @click="checkRegister(form)" type="primary" style="width: 100%">注册</el-button>
        </el-form-item>
      </el-form>
      <span class="login-signin" @click="handleChangeLogin">
        {{ loginSignInMsg }}
      </span>
    </div>
  </div>
</template>
<script>
import { reactive, ref, computed } from 'vue'
import api from '@/plugins/axiosInstance'

export default {
  name: 'SignInView',
  setup() {
    let url = ref('https://vue.learnerhub.net/static/img/logo1.c54dc75.png')
    let form = reactive({
      name: '',
      email: '',
      password: '',
      code: ''
    })
    let activeIndex = ref('1')
    let activeForm = ref('login')
    let verifyCodeBtn = ref('获取验证码')

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

    const passLogin = () => {
      api({
        url: 'login',
        method: 'post',
        data: {
          email: form.email,
          password: form.password
        }
      }).then(res => {
        console.log('登录成功', res)
        clearForm(form)
      }).catch(err => {
        console.log('登录失败', err)
        clearForm(form)
      })
    }

    const isEmailLegal = (email) => {
      const reg = /^([a-zA-Z]|[0-9])(\w|-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
      return reg.test(email)
    }

    const checkEmail = (email) => {
      if (!email) {
        alert('邮箱不能为空')
      } else if (!isEmailLegal(email)) {
        alert('邮箱格式不正确')
      } else {
        handleGetCode()
      }
    }

    const handleGetCode = () => {
      getCode()
      let count = 60
      const timer = setInterval(() => {
        if (count > 0) {
          count--
          verifyCodeBtn.value = count + 's后重新获取'
        } else {
          clearInterval(timer)
          verifyCodeBtn.value = '获取验证码'
        }
      }, 1000)
    }

    const getCode = () => {
      api({
        url: '',
        method: 'post',
        data: {
          name: form.name,
          email: form.email,
          password: form.password,
          code: form.code
        }
      })
    }

    const checkRegister = (form) => {
      if (!form.name) {
        alert('昵称不能为空')
      } else if (!form.email) {
        alert('邮箱不能为空')
      } else if (!isEmailLegal(form.email)) {
        alert('邮箱格式不正确')
      } else if (!form.password) {
        alert('密码不能为空')
      } else if (!form.code) {
        alert('验证码不能为空')
      } else {
        handleRegister(form)
      }
    }

    const clearForm = (form) => {
      form.name = ''
      form.email = ''
      form.password = ''
      form.code = ''
    }

    const handleRegister = (form) => {
      api({
        url: 'register',
        method: 'post',
        data: {
          name: form.name,
          email: form.email,
          password: form.password,
          code: form.code
        }
      }).then(res => {
        console.log('注册成功', res)
        clearForm(form)
        activeForm.value = 'login'
      }).catch(err => {
        console.log('注册失败', err)
        clearForm(form)
      })
    }

    return {
      url,
      form,
      activeIndex,
      activeForm,
      verifyCodeBtn,
      loginSignInMsg,
      handleSelect,
      handleChangeLogin,
      checkEmail,
      checkRegister,
      passLogin
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

.verify-code-btn {
  color: #409eff;
}

.verify-code-btn:hover {
  /*width: 100px;*/
  color: #7dccf9;
  cursor: pointer;
}
</style>