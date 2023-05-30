<template>
	<div class="all" @click="toDetail">
		<el-text class="mx-1 title" size="large">{{item.title}}</el-text>
		<el-text class="mx-1 right">
			<el-icon><Medal /></el-icon>
			{{item.thumbsUpNum}}
			<el-icon style="margin-left:10px;"><ChatSquare /></el-icon>
			{{item.disscussNum}}
		</el-text>
		<br>
		<el-text class="mx-1">
			<el-avatar style="margin-top:15px">  
				<el-icon><UserFilled /></el-icon>
			</el-avatar>
			{{item.user.userName}} - 创建于{{item.createDate}}
		</el-text>
		<el-text class="mx-1 right" style="margin-top:25px">
			更新于{{item.updateDate}}
		</el-text>
		<el-divider />
	</div>
</template>

<script>
	export default {
		name:'MyItem',
		props:['item'],
		methods:{
			toDetail(){
				this.$router.push({
					name:'detail',
					params:{
						id:this.item.id
					}
				})
			}
		}
	}
</script>

<style scoped>
	.title {
		font-weight: bold;
	}
	.right {
		float: right;
	}
	.all {
		padding: 5px;
		border-radius: 20px;
	}
	.all:hover {
		background-color: #d9ecff;
		cursor: pointer;
	}
</style>