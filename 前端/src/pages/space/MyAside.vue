<template>
    
    <el-radio-group v-model="isCollapse" id="choose">
        <el-radio-button :label="false">展开</el-radio-button>
        <el-radio-button :label="true">折叠</el-radio-button>
    </el-radio-group>
    <el-menu
        default-active="/"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
        :router="true"
    >
        <el-menu-item index="/" style="height:50px;">
            <el-icon><House /></el-icon>
            <template #title>主页</template>
        </el-menu-item>
        <el-menu-item index="resource">
            <el-icon><Document /></el-icon>
            <template #title style="font-size = 40px;">资源</template>
        </el-menu-item>
        <el-menu-item index="question">
            <el-icon><Connection /></el-icon>
            <template #title>讨论</template>
        </el-menu-item>
        <el-menu-item index="exercise">
            <el-icon><EditPen /></el-icon>
            <template #title>习题</template>
        </el-menu-item>
        <el-menu-item index="notice">
            <el-icon><Notification /></el-icon>
            <template #title>公告</template>
        </el-menu-item>
    </el-menu>
    
</template>

<script>
    export default {
        name:'MyAside',
        data(){
			return {
				isCollapse:false
			}
		},
        props:['getIsCollapse'],
        watch:{
            isCollapse(newValue){
                this.getIsCollapse(newValue)
            }
        }
    }
</script>

<style>
    .el-menu-vertical-demo:not(.el-menu--collapse) {
		width: 200px;
		min-height: 400px;
	}
    #choose {
        margin-bottom: 20px;
        margin-top: 20px;
    }
</style>