<template>
    <el-image :src="course.imageUrl" :fit="fit" />
    <el-row>
      <el-col :span="22">
        <h1>学习空间</h1>
      </el-col>
      <el-col :span="1">
        <button index = '/about'>编辑</button>
      </el-col>
    </el-row>
    <div class="markdown-body">
      <p>123<br>456</p>
        <h1>1</h1>
        <h2>2</h2>
        <h3>3</h3>
        <h4>4</h4><!--21-->
    </div>
</template>

<script>
export default {
  name: 'Tutorial',
  data(){
            return {
                course:{
                    imageUrl:'https://file.learnerhub.net/crop-avatar-1652083511762/se.png',
                }
            }
        },
  methods:{
    jumpToEdit:function(e){
      console.log(e);
  }

  }
}
</script>

<style scoped>
  image{
    width:100fx;
  }
</style>
