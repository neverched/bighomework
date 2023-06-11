<script setup>
import { Editor } from '@bytemd/vue-next';
import IndexHeader from '../components/IndexHeader.vue';
import { ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import useEditor from '../store/useEditor';
import useImageUpload from '../hooks/useImageUpload';
import useArticleSave from '../hooks/useSave';
import { getPlugins } from '../config';
import api from '@/plugins/axiosInstance';
import router from '@/router';
const EditorStore = useEditor();
const { setValue } = EditorStore;
const { uploadImages } = useImageUpload();
const { saveArticle } = useArticleSave();

const {
  maxLength,
  placeholder,
  previewDebounce,
  value = '',
  locale,
  articleTitle
} = storeToRefs(EditorStore);

// 如果plugins也放在store内部的话，会引起第二次加载plugins失败，导致toolbar点击失效;
const plugins = getPlugins();

/**
 * 保存按钮点击；
 */
const onSaveClick = saveArticle;

const onSettingClick = () => { };


const onExportClick = type => {
  switch (type) {
    case 'markdown':
      giveOut();
      break;
    default:
      break;
  }
};
const giveOut = function () {
  console.log(value.value);
  console.log('准备保存')
  const formData = new FormData()
  formData.append('is_edit', 1)
  formData.append('new_content', value.value)
  api.post('spaces/1', formData).then(
    res => {
      console.log('保存中')
      console.log(res)
      console.log('保存完成')
      router.push('/')
    },
    err => {
      console.log(err)
    }
  )
}

const dialogVisible = ref(false);

const sanitize = schema => {
  schema.attributes['*'].push('style');
  return schema;
};
</script>

<template>
  <el-row>
    <el-text tag="mark">（选择项最右侧进入全屏编辑）</el-text>
  </el-row>
  <el-row>
    <el-col :span="23" :offset="0">
      <div id="app-content" class="markdown-body" style="height: 450px;">
        <Editor v-model:value="value" :plugins="plugins" :locale="locale" :upload-images="uploadImages"
          :preview-debounce="previewDebounce" :placeholder="placeholder" :max-length="maxLength" :sanitize="sanitize"
          class="mkd-editor" @change="setValue" />
      </div>
    </el-col>

  </el-row>
  <el-cow>
    <IndexHeader @save="onSaveClick" @setting="onSettingClick" @open-list="dialogVisible = true"
      @export="onExportClick" />
  </el-cow>
</template>
