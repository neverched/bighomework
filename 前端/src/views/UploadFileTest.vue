<template>
  <el-row>
    <el-col :offset="2" :span="18">
      <br>
      <br>
      <el-text tag='b' style="font-size:30px;color:black;">本地上传</el-text>
      <br>
      <br>
      <br>
      <input type="file" ref="fileInput" style="font-size: large;">
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <el-text tag="b" style="font-size:20px;">文件标题</el-text>
      <br>
      <br>
      <el-input v-model="title" placeholder="标题（必填）" />
      <div style="margin: 20px 0"></div>
      <br>
      <br>
      <br>
    </el-col>
    <el-cow :offset="2" :span="18">
      <el-button type="primary" @click="outPut">保存修改</el-button>
      <el-button @click="jumpBack">取消</el-button>
    </el-cow>
  </el-row>
</template>

<script>
import axios from 'axios';
import router from '@/router';
import { ref } from 'vue'
import { h } from 'vue'
import { ElNotification } from 'element-plus'
import api from '@/plugins/axiosInstance'
export default {
  data() {
    return {
      title: '',
      content: ''
    }
  },
  methods: {
    outPut() {
      const fileInput = this.$refs.fileInput
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      const file = fileInput.files[0]
      if (typeof file == 'undefined') {
        alert('文件不能为空');
        return;
      }
      if (this.title === '') {
        alert('标题不能为空');
        return;
      }
      const formData = new FormData()
      formData.append('is_create', '1')
      formData.append('resource_name', this.title)
      formData.append('file', file)
      api.post('spaces/1/resources/new', formData, config).then(
        res => {
          console.log(res)
          router.push('/resource')
        },
        err => {
          console.log(err)
        }
      )
    },
    jumpBack() {
      router.push('/resource');
    }
  }

}
</script>