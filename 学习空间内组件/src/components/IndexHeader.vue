<script setup>
  import { watch } from 'vue';
  import { storeToRefs } from 'pinia';
  import useEditor from '@/store/useEditor';
  import useClipboard from 'vue-clipboard3';
  import router from '@/router';
  import api from '@/plugins/axiosInstance'
  const emit = defineEmits(['save', 'setting', 'openList', 'export']);

  const state = useEditor();
  const { setTitle } = state;
  const { articleTitle } = storeToRefs(state);
  watch(articleTitle, setTitle);
  var originalContent
  const getContent=function(){
    const formData = new FormData();
    api.post('/api/spaces/1',formData).then(
      res => {
        console.log(res)
        originalContent = res.data.data.space_index;
        copy(res.data.data.space_index);
      },
      err => {
        console.log(err)
      }
    )
  }
  const shoutOut = function(){
    const t = "markdown";
    emit('export', t);
    router.push('/')
  }
  const { toClipboard } = useClipboard()
  const copy = async (msg) => {
      try {
        await toClipboard(msg)
        alert('复制成功')
      } catch (e) {
        alert('复制失败，原文为空')
      }
  }

</script>

<template>
  <header class="page-header">
    <el-button type="primary" @click="shoutOut">保存修改</el-button>
    <el-button type="primary" @click="getContent">复制原文内容</el-button>
    <el-button>取消</el-button>
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
