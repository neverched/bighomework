<template>
    <el-row >
      <el-col :span="16" :offset="2" >
        <el-image :src="course.imageUrl" :fit="fit" />
        <el-row>
          <el-col :span="22">
            <h1>学习空间</h1>
          </el-col>
          <el-col :span="1">
            <el-button plain>编辑</el-button>
          </el-col>
        </el-row>
        <div class="markdown-body">
          <p>123<br>456</p>
          <h1>1</h1>
          <h2>2</h2>
          <h3>3</h3>
          <h4>4</h4><!--21-->
        </div>

      </el-col>
      <el-col :span="3" :offset="1">
        <IndexRight/>
      </el-col>
    </el-row>
    
    

</template>

<script>
  import IndexRight from './IndexRight.vue'
  import Tutorial from './Tutorial.vue'
  export default {
    name: 'IndexContent',
    components:{IndexRight,Tutorial} ,
    data(){
            return {
                course:{
                    imageUrl:'https://file.learnerhub.net/crop-avatar-1652083511762/se.png',
                }
            }
        }
  }
</script>


<style scoped>
</style>
