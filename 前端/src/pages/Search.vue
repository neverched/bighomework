<template>
    <el-main>
        <el-row>
		<el-col :span="20" :offset="2">	
			<el-card class="box-card">
				<template #header>
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

					<div class="card-header">
						<el-select 
							v-model="rankValue" 
							class="m-2" 
							placeholder="最多点赞"
						>
							<el-option
								v-for="item in rankOptions"
								:key="item.value"
								:label="item.label"
								:value="item.value"
							/>
						</el-select>
					</div>
					<div class="card-header">
						<el-select 
							v-model="type" 
							class="m-2" 
							placeholder="resources"
						>
							<el-option
								v-for="item in typeOptions"
								:key="item.value"
								:label="item.label"
								:value="item.value"
							/>
						</el-select>
					</div>
				</template>
				<div v-loading="isLoading" style="height:200px;" v-show="isLoading"></div>
				<MyItem
					v-for="r in result"
					:key="r.id"
					:item="r"
					:type="this.type"
				/>
			</el-card>
		</el-col>
	</el-row>
    </el-main>
</template>

<script>
	import MyItem from './space/MyItem'

    export default {
        name:'search',
		components:{MyItem},
        data() {
			return {
				rankValue:'最多点赞',
				rankOptions: [
					{value: '最近更新',label: '最近更新'},
					{value: '最多点赞',label: '最多点赞'},
					{value: '最近创建',label: '最近创建'},
					{value: '最多关注',label: '最多关注'}
				],
				type:'resources',
				typeOptions: [
					{value: 'resources',label: 'resources'},
					{value: 'questions',label: 'questions'},
					{value: 'exercises',label: 'exercises'},
				],
				isLoading:false,
				input:'',
				result:[]
			}
		},
		props:['firstInput'],
		methods:{
			search(){
				this.isLoading = true
				const formData = new FormData()
				formData.append('types', this.type)
				formData.append('text', this.input)
				formData.append('method', this.rankValue)
				this.$http.post('search',formData).then(
                    res => {
                        this.result = res.data.data
						this.result.forEach((value) => {
							value.create_time = value.create_time.slice(0, 10)
							value.last_update_time = value.last_update_time.slice(0, 10)
							value.user_name = value.creator_name
						})
						this.isLoading = false
                    },
                    err => {
                        console.log(err)
                    }
                )
			}
		},
		mounted() {
			this.input = this.firstInput
			this.isLoading = true
			const formData = new FormData()
			formData.append('types', 'resources')
			formData.append('text', this.input)
			formData.append('method', '最多点赞')
			this.$http.post('search',formData).then(
				res => {
					this.result = res.data.data
					console.log(res)
					this.result.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
						value.last_update_time = value.last_update_time.slice(0, 10)
						value.user_name = value.creator_name
					})
					this.isLoading = false
				},
				err => {
					console.log(err)
				}
			)
		}
    }
</script>

<style scoped>
	.header-input {
		width: 350px;
		height: 40px;
		margin-top: 10px;
	}
	.card-header {
		float: right;
		margin-top: 10px;
		width: 150px;
	}
</style>