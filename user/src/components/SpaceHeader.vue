<template>
    
    <el-row :gutter="30">
        <el-col :span="3" :offset="2">
            <el-image :src="course.imageUrl" :fit="fit" />
        </el-col>
        <el-col :span="13">
            <el-text class="mx-1 title" size="large">{{course.courseName}}</el-text>
            <br>
            <br>
            <el-text class="mx-1">{{course.info}}</el-text>
        </el-col>
        <el-col :span="5">
            <el-button type="primary" class="center">
                <el-icon><Medal /></el-icon>
                <span>点赞</span>
            </el-button>
            <el-button type="primary" class="center">
                <el-icon><View /></el-icon>
                <span>关注</span>
            </el-button>
        </el-col>
    </el-row>
    
</template>

<script>
    export default {
        name:'SpaceHeader',
        data(){
            return {
                course:{
                    imageUrl:'https://file.learnerhub.net/Fs1fJ_V2T8nUlsOCZ__T9xBnWhXu',
                    courseName:'软件工程（北京航空航天大学）',
                    info:'围绕软件工程课程综合实践，针对综合实践中的需求分析、软件设计、系统建模、编码测试、软件维护等方面的内容，讨论问题，分享成果，交流经验，共享资源'
                }
            }
        }
    }
</script>

<style>
    .title {
		font-weight: 1000;
	}
	.center {
		margin-top: 30px;
		margin-left: 20px;
	}
</style>