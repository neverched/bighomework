<template>
	<el-container>
		<el-header>
      		<MyHeader/>
		</el-header>
		<el-container>
			<el-aside width="200px">
				<MyAside/>
			</el-aside>
			<el-main>
				<SpaceHeader/>
				<router-view></router-view>
			</el-main>
		</el-container>
    </el-container>
	
</template>

<script>
	import MyHeader from './components/MyHeader.vue'
	import SpaceHeader from './components/SpaceHeader.vue'
	import MyAside from './components/MyAside.vue'
	
	export default {
		name: 'App',
		components:{MyHeader, SpaceHeader, MyAside}

	}
</script>

<style>
	el-text {
		font-family:'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  					'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
	}
	
</style>
