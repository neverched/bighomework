<script setup>
  import { watch } from 'vue';
  import { storeToRefs } from 'pinia';
  import useEditor from '@/store/useEditor';
  import router from '@/router';
  const emit = defineEmits(['save', 'setting', 'openList', 'export']);

  const state = useEditor();
  const { setTitle } = state;
  const { articleTitle } = storeToRefs(state);
  watch(articleTitle, setTitle);
  const shoutOut = function(){
    const t = "markdown";
    emit('export', t);
  }
  const jumpToBack=function(){
    router.push('/resource');
  }
</script>

<template>
  <header class="page-header">
    <el-button type="primary" @click="shoutOut">保存修改</el-button>
    <el-button @click="jumpToBack">取消</el-button>
  </header>
</template>

<style lang="less" scoped>
  .page-header {
    width: 100vw;
    height: 60px;
    display: flex;
    align-items: center;
    padding: 0 16px;
    .title {
      height: 40px;
      flex: 1;
      font-size: 18px;
      --el-input-border-color: transparent;
      --el-input-transparent-border: none;
      --el-input-border-radius: 0;
      --el-input-hover-border-color: transparent;
      --el-input-focus-border-color: transparent;
    }
  }
</style>
