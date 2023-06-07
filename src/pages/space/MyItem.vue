<template>
	<div class="all" @click="toDetail">
		<el-text class="mx-1 title" size="large" truncated>{{item.title}}</el-text>
		<el-text class="mx-1 right" v-show="type != 'notices'">
			<el-icon><Medal /></el-icon>
			{{item.likes}}
			<el-icon style="margin-left:10px;"><Star /></el-icon>
			{{item.follows}}
		</el-text>
		<br>
		<el-text class="mx-1">
			<el-avatar style="margin-top:15px">  
				<el-icon><UserFilled /></el-icon>
			</el-avatar>
			{{item.user_name}} - 创建于{{item.create_time}}
		</el-text>
		<el-text class="mx-1 right" style="margin-top:25px">
			更新于{{item.last_update_time}}
		</el-text>
		<el-divider />
	</div>
</template>

<script>
	export default {
		name:'MyItem',
		props:['item','type'],
		methods:{
			toDetail(){
				this.$router.push({
					name:'detail',
					query:{
						id:this.item.id,
						type:this.type
					}
				})
			}
		},
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
		margin-bottom: 5px;
	}
	.all:hover {
		background-color: #d9ecff;
		cursor: pointer;
	}
</style>