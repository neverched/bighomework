<template>
  <el-card class="card-box" style="width: 200px;">
    <template #header>
      <div class="card-header">
        <span>管理团队</span>
      </div>
    </template>
    <div v-for="o in 4" :key="o" class="text item">
      {{ 'List item ' + o }}
    </div>
  </el-card>
   
  <el-card class="card-box" style="width: 200px;">
    <template #header>
      <div class="card-header">
        <span>最新资源</span>
      </div>
    </template>
    <div v-for="o in 4" :key="o" class="text item">
      {{ 'List item ' + o }}
    </div>
  </el-card>

  <el-card class="card-box" style="width: 200px;">
    <template #header>
      <div class="card-header">
        <span>最新问题</span>
      </div>
    </template>
    <div v-for="o in 4" :key="o" class="text item">
      {{ 'List item ' + o }}
    </div>
  </el-card>
</template>

<script>
export default {
  name: 'IndexRight',
}
</script>

<style scoped>
  .card-box {
    margin-bottom: 10px;
  }
 

</style>
