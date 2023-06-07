<template>
	<el-button type="danger" @click="getFileName('9')">下载</el-button>
</template>

<script>
    import { Editor } from '@bytemd/vue-next';
    import ResourceHeader from '../components/ResourceHeader.vue';
    import { ref, computed } from 'vue';
    import { storeToRefs } from 'pinia';
    import useEditor from '../store/useEditor';
    import useImageUpload from '../hooks/useImageUpload';
    import useArticleSave from '../hooks/useSave';
    import { getPlugins } from '../config';
    import api from '@/plugins/axiosInstance'
    import { h } from 'vue'
    import { ElNotification } from 'element-plus'
	export default {
		name: 'App',
        data(){
            return {
                fileName :'',
            }
        },
        methods:{
            getFileName(t){
                const formData = new FormData()
                formData.append('get_name','1')
                api.post(`api/file/${t}`,formData).then(
                    res => {
                    console.log(this)
                    this.fileName=res.data.name
                    this.getFile(t)
                },
                err => {
                    console.log(err)
                }
                )
                
            },
            getFile(resourceID){
                console.log(resourceID)
                const t = resourceID
                console.log(t)
                const formData2 = new FormData()
                api.post(`api/file/${t}`,formData2,{responseType: 'blob'}).then(
                res => {
                    console.log(res);
                    console.log(res.data.type);
                    let blob = new Blob([res.data], { type: res.data.type });
                    let url = window.URL.createObjectURL(blob);
                    console.log(url);
                    let link = document.createElement("a");
                    link.style.display = "none";
                    link.href = url;
                    link.setAttribute("download", this.fileName);//文件名后缀记得添加
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);//下载完成移除元素
                    window.URL.revokeObjectURL(url);//释放掉blob对象
                },
                err => {
                    console.log(err)
                }
                ) 
            }
        }


	}
</script>