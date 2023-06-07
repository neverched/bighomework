<template>
  <router-link to="/users/sign_in">登录/注册</router-link>
  <router-link :to="{
    name: 'users',
    params: { id: 1 }
  }">
    用户列表</router-link>
  <router-view></router-view>
</template>

<script setup>
</script>
