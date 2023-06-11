<template>
  <div>
    <el-row>
      <el-col :span="14" :offset="2">
        <el-image :src="course.imageUrl" :fit="fit" />
        <br>
        <br>
        <el-button type="primary" round @click="jumpToEdit">编辑</el-button>
        <h1>学习指南</h1>
        <v-md-preview v-model:text="str" />
      </el-col>
    </el-row>
  </div>
</template>
<script>

import router from '@/router'
import api from '@/plugins/axiosInstance'
export default {
  data() {
    return {
      str: '',
      course: {
        imageUrl: 'https://picture.zhuiyue.vip:444/images/2023/06/08/57b7cbb90011882ba12740dfec4bbc4.md.jpg',
      }
    };
  },
  methods: {
    jumpToEdit: function () {
      this.$http.get('give').then(
        res => {
          if(res.data.msg == '没有登录') this.$message('尚未登录，请先登录')
          else router.push('/about');
        },
        err => {
          console.log(err)
        }
      )
    },

    getContent: function () {
      const formData = new FormData();
      api.post('spaces/1', formData).then(
        res => {
          this.str = res.data.data.space_index;
          console.log(this.str)
        },
        err => {
          console.log(err)
        }
      )
    }
  },
  mounted() {
    console.log('开始调用')
    this.getContent();
  }
}
</script>


<style scoped>
.content {
  height: 540px;
  /* 容器高度 */
  width: 100%;
  /* 容器宽度 */
  padding: 10px;
  /* 可选。内容与容器的内边距 */
  box-sizing: border-box;
  /* 可选。将内边距纳入容器宽高计算 */
  overflow: auto;
  /* 让内容超出容器尺寸时出现滚动条 */
}
</style>
