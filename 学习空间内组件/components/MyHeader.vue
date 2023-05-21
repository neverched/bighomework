<template>
	<el-menu
		:default-active="activeIndex"
		class="el-menu-demo"
		mode="horizontal"
		:ellipsis="false"
	>
		<el-menu-item index="0">学习空间</el-menu-item>
		<el-input
			v-model="input"
			class="header-input w-50 m-2"
			size="small"
			placeholder="搜索空间、资源、问题、用户"
		>
			<template #suffix>
				<el-icon class="el-input__icon"><Search /></el-icon>
			</template>
		</el-input>
		<div class="flex-grow" />

		<el-menu-item index="1">消息</el-menu-item>

		<el-sub-menu index="2">
			<template #title>
				<el-icon><User /></el-icon>
			</template>
			<el-menu-item index="2-1">个人主页</el-menu-item>
			<el-menu-item index="2-2">修改密码</el-menu-item>
			<el-menu-item index="2-3">退出登录</el-menu-item>
		</el-sub-menu>
	</el-menu>
</template>

<script>
	export default {
		name: 'MyHeader',
		data() {
			return {
				input:'',
			}
		}
	}
</script>

<style scoped>
	.flex-grow {
		flex-grow: 1;
	}
	.header-input {
		width: 350px;
		height: 40px;
		margin-left: 400px;
		margin-top: 10px;
	}
</style>
