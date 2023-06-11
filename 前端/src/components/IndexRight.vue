<template>  
  <el-card class="card-box" style="width: 200px;">
    <template #header>
      <div class="card-header">
        <span>最新资源</span>
      </div>
    </template>
    <div v-for="o in 4" :key="o" class="text item">
      <el-text size = "large" tag="b" @click = "jumpToQuestion" class="resource">
        <el-icon><Document /></el-icon>
        问题标题
      </el-text>
    </div>
  </el-card>

  <el-card class="card-box" style="width: 200px;">
    <template #header>
      <div class="card-header">
        <span>最新问题</span>
      </div>
    </template>
    <div v-for="o in 4" :key="o" class="text item">
      <el-text size = "large" tag="b" class="issue">
        <el-icon><QuestionFilled /></el-icon>
        问题标题
      </el-text>
    </div>
  </el-card>
</template>

<script>
import router from '@/router';

export default {
  name: 'IndexRight',
  methods:{
    jumpToQuestion(){
      router.push('/');
    }
  }
}
</script>

<style scoped>
  .card-box {
    margin-bottom: 10px;
  }
 
  .issue:hover{
    color:blue;
    cursor:pointer
  }

  .resource:hover{
    color:blue;
    cursor:pointer
  }
</style>
