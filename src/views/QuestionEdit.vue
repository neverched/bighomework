<template>
  <el-row>
    <el-col :offset="2" :span="18">
      <br>
      <br>
      <el-text tag='b' style="font-size:30px;color:black;">创建习题</el-text>
      <br>
      <br>
      <br>
      <br>
      <br>
      <el-input
        v-model="textarea1"
        placeholder="标题（必填）"
      />
      <div style="margin: 20px 0" ></div>
      <br>
      <br>
      <el-input
        v-model="textarea2"
        :autosize="{ minRows: 2, maxRows: 4 }"
        type="textarea"
        placeholder="题干（必填）"
      />
      <div style="margin: 20px 0" ></div>
      <br>
      <br>
      <el-input
        v-model="textarea3"
        :autosize="{ minRows: 2, maxRows: 4 }"
        type="textarea"
        placeholder="答案（必填）"
      />
      </el-col>
      <el-button type="primary" @click="save">保存修改</el-button>
      <el-button @click="jumpToBack">取消</el-button>
  </el-row>
  
</template>

<script setup>
import router from '@/router';
import { ref } from 'vue'
import { h } from 'vue'
import { ElNotification } from 'element-plus'
import api from '@/plugins/axiosInstance'
const textarea1 = ref('')
const textarea2 = ref('')
const textarea3 = ref('')
const save=function(){ 
  if(textarea1.value === ''){
    open1('标题不能为空');
    return;
  }
  if(textarea2.value === ''){
    open1('题干不能为空');
    return;
  }
  if(textarea3.value === ''){
    open1('答案不能为空');
    return;
  }
  const formData = new FormData()
  formData.append('is_create','1')
  formData.append('type', textarea1.value)
  formData.append('content', textarea2.value)
  formData.append('answer', textarea3.value)
  formData.append('difficulty','1')
  api.post('/api/spaces/1/exercises/new',formData).then(
    res => {
      console.log(res)
      router.push('/question')
    },
    err => {
      console.log(err)
    }
  )
}
const open1 = (msg) => {
  ElNotification({
    title: '警告',
    message: h('i', { style: 'color: red' }, msg),
  })
}
const jumpToBack=function(){
  router.push('/question')
}
</script>