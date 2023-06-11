<template>
	<el-container style="height: 710px; overflow: auto;">
		<el-header>
			<MyHeader :msg="articleList" v-if="reFresh" @changMsg="changMsg"/>
		</el-header>
		<el-container>
			<router-view></router-view>
		</el-container>
	</el-container>
</template>

<script>
import MyHeader from './components/MyHeader.vue'
import { useStore } from 'vuex' // 引入useStore 方法
export default {
	name: 'App',
	components: { MyHeader },
	data() {
    return {
      msg: '阿离王',
	  reFresh:true,
    }
  	},
  	methods:{
      changMsg(msg) {
          this.msg = msg
		  this.reFresh=false
		  console.log(this.reFresh)
		  this.reFresh=true
		  console.log(this.reFresh)
		  console.log('信息改变了')
      }
  	},
}

</script>

<style>
el-text {
	font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
		'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>
