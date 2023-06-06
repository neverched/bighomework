<template lang="">
  <div class="container">
    {{ recentWrites[0].id }}
    <!-- <el-space direction="vertical">
      <el-card class="box-card fans-view">
        <div></div>
        <div></div>
        <div></div>
      </el-card>
      <el-card v-show="recentWrites.length" class="box-card">
        <template #header>
          <div>
            最近创作
          </div>
        </template>
        <div v-for="item in recentWrites" :key="item.id" class="item" @click="handleItemClick(item)">{{ item.content }}</div>
      </el-card>
    </el-space> -->
  </div>
</template>
<script setup>
import { reactive } from 'vue'

let recentWrites = reactive([
  {
    id: 1,
    content: '最近创作1'
  },
  {
    id: 2,
    content: '最近创作2'
  },
  {
    id: 3,
    content: '最近创作3'
  },
])

/* const handleItemClick = (item) => {
  // 这里应该实现跳转到文章详情页
  console.log('item click', item.id)
} */
</script>
<style scoped>
.container {
  width: 270px;
  border-radius: 8px;
  background-color: yellow;
}

.box-card {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.fans-view {
  height: 90px;
  display: flex;
}

.fans-view :nth-child(1) {
  width: 89px;
  height: 90px;
  border-radius: 8px 0 0 8px;
  border-right: 1px solid #ebebeb;
}

.fans-view :nth-child(2) {
  width: 90px;
  height: 90px;
  border-radius: 8px 0 0 8px;
}

.fans-view :nth-child(3) {
  width: 89px;
  height: 90px;
  border-radius: 0 8px 8px 0;
  border-left: 1px solid #ebebeb;
}

.item {
  margin-bottom: 10px;
  background-color: beige;
}
</style>