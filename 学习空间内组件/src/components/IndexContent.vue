<template>
    <div class="content">
    <el-row>
      <el-col :span="14" :offset="2">
        <el-button @click="login">登录</el-button>
        <el-image :src="course.imageUrl" :fit="fit" />
        <el-button type="primary" round @click="jumpToEdit">编辑</el-button>
        <h1>学习空间</h1>  
        <v-md-preview :text="str"/>
      </el-col>
      <el-col :span="5" :offset="1">
        <IndexRight/>
      </el-col>
    </el-row>
  </div>
    

</template>
<script>

  import router from '@/router';
  import IndexRight from './IndexRight.vue'
  import api from '@/plugins/axiosInstance'
  export default {
  components:{IndexRight},
  data() {
    return {
      str: '',
      course:{
                    imageUrl:'https://file.learnerhub.net/crop-avatar-1652083511762/se.png',
              }
    };
  },
  methods:{
    jumpToEdit:function(){
              router.push('/about');
    },

    login:function(){
              const formData = new FormData()
              formData.append('email', '2434786497@qq.com')
              formData.append('password', 'wxy123456')
              api.post('/api/login',formData).then(
              res => {
                console.log(res)
              },
              err => {
                console.log(err)
              }
              )
      },
    getContent:function(){
      const formData = new FormData();
      api.post('spaces/1',formData).then(
      res => {
        console.log(res)
        this.str = res.data.data.space_index;
      },
      err => {
        console.log(err)
      }
    )
  }
  },
  mounted(){
    this.getContent();
  }

};
</script>


<style scoped>
.content {
  height: 540px; /* 容器高度 */
  width: 100%; /* 容器宽度 */
  padding: 10px; /* 可选。内容与容器的内边距 */
  box-sizing: border-box; /* 可选。将内边距纳入容器宽高计算 */
  overflow: auto; /* 让内容超出容器尺寸时出现滚动条 */
}
</style>
