<template>
	<div class="all">
		<el-text class="mx-1 title" size="large">{{question.title}}</el-text>
		<el-text class="mx-1 right">
			<el-icon><Medal /></el-icon>
			{{question.thumbsUpNum}}
			<el-icon style="margin-left:10px;"><ChatSquare /></el-icon>
			{{question.disscussNum}}
		</el-text>
		<br>
		<el-text class="mx-1">
			<el-avatar style="margin-top:15px">  
				<el-icon><UserFilled /></el-icon>
			</el-avatar>
			{{question.user.userName}} - 创建于{{question.createDate}}
		</el-text>
		<el-text class="mx-1 right" style="margin-top:25px">
			更新于{{question.updateDate}}
		</el-text>
		<hr>
	</div>
</template>

<script>
	export default {
		name:'MyItem',
		props:['question']
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
		margin-top: 5px;
	}
	.all:hover {
		background-color: #d9ecff;
		cursor: pointer;
	}
</style>