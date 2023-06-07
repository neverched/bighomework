<template>
	<el-aside :width="asideWidth">
        <MyAside :getIsCollapse="getIsCollapse"/>
    </el-aside>
    <el-main>
        <SpaceHeader/>
        <router-view></router-view>
    </el-main>
</template>

<script>
	import SpaceHeader from './space/SpaceHeader.vue'
	import MyAside from './space/MyAside.vue'
	
	export default {
		name: 'App',
		components:{SpaceHeader, MyAside},
		data() {
			return {
				asideWidth:'200'
			}
		},
		methods:{
			getIsCollapse(isCollapse){
				if(isCollapse) this.asideWidth = '120'
				else this.asideWidth = '200'
			}
		}
	}
</script>

<style>
	
</style>
