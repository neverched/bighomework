<template>
	<el-container>
		<el-header>
      		<MyHeader/>
		</el-header>
		<el-container>
			<router-view></router-view>
		</el-container>
    </el-container>
	
</template>

<script>
	import MyHeader from './components/MyHeader.vue'

	export default {
		name: 'App',
		components:{MyHeader},
	}
</script>

<style>
	el-text {
		font-family:'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  					'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
	}
	
</style>
