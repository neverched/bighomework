<template>
    
    <el-radio-group v-model="isCollapse" id="choose">
        <el-radio-button :label="false">展开</el-radio-button>
        <el-radio-button :label="true">折叠</el-radio-button>
    </el-radio-group>
    <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        :collapse="isCollapse"
    >
        <el-menu-item index="1">
            <el-icon><House /></el-icon>
            <template #title>主页</template>
        </el-menu-item>
        <el-menu-item index="2">
            <el-icon><Document /></el-icon>
            <template #title>资源</template>
        </el-menu-item>
        <el-menu-item index="3">
            <el-icon><Connection /></el-icon>
            <template #title>讨论</template>
        </el-menu-item>
        <el-menu-item index="4">
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