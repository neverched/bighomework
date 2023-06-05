<template>
	<el-container>
		<el-header>
      		<MyHeader/>
          <h>1</h>
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
    <h>1</h>
  </div>
</template>

<script>
	import MyHeader from '../components/MyHeader.vue'
	import SpaceHeader from '../components/SpaceHeader.vue'
	import MyAside from '../components/MyAside.vue'
	import IndexContent from '../components/IndexContent.vue'
	export default {
		name: 'App',
		components:{MyHeader, SpaceHeader, MyAside,IndexContent}

	}
</script>
