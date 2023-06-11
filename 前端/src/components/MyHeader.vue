<template>
	<el-menu default-active="/" class="el-menu-demo" mode="horizontal" :ellipsis="false" :router="true">
		<el-menu-item index="/">学习空间</el-menu-item>
		<el-input v-model="input" class="header-input w-50 m-2" size="small" placeholder="搜索资源、问题、习题">
			<template #prefix>
				<el-icon class="el-input__icon">
					<Search />
				</el-icon>
			</template>
		</el-input>
		<el-button type="primary" style="margin-top: 10px;height: 40px;" @click="search">搜索</el-button>

		<div class="flex-grow" />



		<el-sub-menu index="2">
			<template #title>
				<el-icon>
					<User />
				</el-icon>
			</template>
			<el-menu-item :index="userPath">个人主页</el-menu-item>
			<el-menu-item index="/changePassword">修改密码</el-menu-item>
			<el-menu-item @click="logout">退出登录</el-menu-item>
		</el-sub-menu>

		<el-button type="primary" plain @click="changeLog" class="login" :key = "buttonText">{{ buttonText }}</el-button>

	</el-menu>
</template>

<script>
export default {
	name: 'MyHeader',
	data() {
		return {
			input: '',
			user: { id: '123' },
			isLogin: false,
			buttonText: ''
		}
	},
	computed: {
		userPath() {
			if(!this.isLogin) return '/users/sign_in'
			return '/users/' + this.user.id
		}
	},
	methods: {
		login() {
			this.$router.push({
				name: 'sign_in'
			})
		},
		search() {
			this.$router.push({
				name: 'search',
				query: {
					input: this.input
				}
			})
		},
		logout(){
			this.$http.post('logout').then(
				res => {
					console.log(res)
					this.$message('退出登录成功')
					this.isLogin = false
					this.buttonText = '登录/注册'
				},
				err => {
					console.log(err)
					this.$message('尚未登录，请先登录')
				}
			)
			this.$router.push({
				name:'house',
				query:{
					input:this.input
				}
			})
		},
		changeLog(){
			this.$emit('changMsg', this.isLogin)
			if(this.isLogin) this.logout()
			else this.login()
		}
	},
	mounted(){
		this.$http.get('give').then(
			res => {
				/* console.log(res) */
				if(res.data.msg == '没有登录') {
					this.isLogin = false
					this.buttonText = '登录/注册'
					console.log('目前还未登录')
					console.log(this.isLogin)
					console.log(this.buttonText)
				}
				else 
					{
						this.isLogin = true
						this.buttonText = '退出登录'
						console.log('目前已经是登陆状态啦')
						console.log(this.isLogin)
						console.log(this.buttonText)
					}
			},
			err => {
				console.log(err)
			}
		)
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
