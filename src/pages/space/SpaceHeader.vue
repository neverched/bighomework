<template>
    
    <el-row :gutter="30" style="margin-bottom:5px;">
        <el-col :span="3" :offset="2">
            <el-image :src="imageUrl" style="height:100px"/>
        </el-col>
        <el-col :span="13">
            <el-text class="mx-1 title" size="large">{{courseName}}</el-text>
            <br>
            <br>
            <el-text class="mx-1">{{info}}</el-text>
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
                imageUrl:'https://file.learnerhub.net/Fs1fJ_V2T8nUlsOCZ__T9xBnWhXu',
                courseName:'',
                info:''
            }
        },
        mounted(){
            this.$http.post('spaces/1').then(
                res => {
                    this.courseName = res.data.data.space_name
                    this.info =  res.data.data.space_introduction
                },
                err => {
                    console.log(err)
                }
            )
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