<template>
  <router-link to="/users/sign_in">登录/注册</router-link>
  <router-link to="/users">用户列表</router-link>
  <router-view></router-view>
</template>

<script>

export default {
  name: 'App',
}
</script>
