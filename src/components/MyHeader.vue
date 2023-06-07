<template>
	<el-menu
		default-active="/"
		class="el-menu-demo"
		mode="horizontal"
		:ellipsis="false"
		:router="true"
	>
		<el-menu-item index="/">学习空间</el-menu-item>
		<el-input
			v-model="input"
			class="header-input w-50 m-2"
			size="small"
			placeholder="搜索资源、问题、用户"
		>
			<template #prefix>
				<el-icon class="el-input__icon"><Search /></el-icon>
			</template>
		</el-input>
		<el-button type="primary" style="margin-top: 10px;height: 40px;" @click="search">搜索</el-button>

		<div class="flex-grow" />

		

		<el-sub-menu index="2">
			<template #title>
				<el-icon><User /></el-icon>
			</template>
			<el-menu-item :index="userPath">个人主页</el-menu-item>
			<el-menu-item index="/changePassword">修改密码</el-menu-item>
			<el-menu-item index="2-3">退出登录</el-menu-item>
		</el-sub-menu>
		
			<el-button type="primary" plain 
				@click="login" 
				class="login">
			登录</el-button>
		
	</el-menu>
</template>

<script>
	export default {
		name: 'MyHeader',
		data() {
			return {
				input:'',
				user:{id:'123'},
			}
		},
		computed:{
			userPath(){
				return '/user/'+this.user.id
			}
		},
		methods:{
			login(){
                const formData = new FormData()
				formData.append('email', '66555@qq.com')
                formData.append('password', 'wsedrf')
                this.$http.post('login',formData).then(
                    res => {
                        console.log(res)
                    },
                    err => {
                        console.log(err)
                    }
                )
            },
			search(){
				this.$router.push({
					name:'search',
					query:{
						input:this.input
					}
				})
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
	.login {
		margin-top: 10px;
	}
</style>
