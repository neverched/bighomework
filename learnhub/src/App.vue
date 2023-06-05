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
				<IndexContent/>
			</el-main>
		</el-container>
    </el-container>
	<div>
  </div>
</template>

<script>
	import MyHeader from './components/MyHeader.vue'
	import SpaceHeader from './components/SpaceHeader.vue'
	import MyAside from './components/MyAside.vue'
	import IndexContent from './components/IndexContent.vue'
	export default {
		name: 'App',
		components:{MyHeader, SpaceHeader, MyAside,IndexContent}

	}
</script>
