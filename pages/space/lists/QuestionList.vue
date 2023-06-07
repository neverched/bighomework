<template>
	<el-row>
		<el-col :span="20" :offset="2">	
			<el-card class="box-card">
				<template #header>
					<div class="card-header">
						<el-select 
							v-model="rankValue" 
							class="m-2" 
							placeholder="最新发布"
							@change="rankChange"
						>
							<el-option
								v-for="item in rankOptions"
								:key="item.value"
								:label="item.label"
								:value="item.value"
							/>
						</el-select>
						<el-button type="primary" plain id="create-ques" style="margin-left: 20px;">
							<span>创建讨论</span>
							<el-icon><Plus /></el-icon>
						</el-button>
					</div>
				</template>

				<div v-loading="isLoading" style="height:200px;" v-show="isLoading"></div>
				<MyItem
					v-for="q in questions"
					:key="q.id"
					:item="q"
					type="questions"
				/>
				<el-pagination 
					background 
					layout="prev, pager, next" 
					:total="total"
					@current-change="pageChange"
					v-show="!isLoading"
					v-model:current-page="curPage"
				/>
				
			</el-card>
		</el-col>
	</el-row>
</template>

<script>
	import MyItem from '../MyItem'

	export default {
		name:'QuestionList',
		components:{MyItem},
        data() {
			return {
				rankValue:'最新创建',
				rankOptions: [
					{value: '最新创建',label: '最新创建'},
					{value: '最近更新',label: '最近更新'},
					{value: '最多点赞',label: '最多点赞'},
					{value: '最多讨论',label: '最多讨论'},
				],
				questions:[],
				isLoading:false,
				total:0,
				curPage:1
			}
		},
		methods:{
			pageChange(){
				const formData = new FormData()
				formData.append('page', this.curPage)
				formData.append('sort', this.rankValue)

				this.$http.post('/spaces/1/questions', formData).then(
					res => {
						this.questions = res.data.list
						this.questions.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
						value.last_update_time = value.last_update_time.slice(0, 10)
					})
					},
					err => {
						console.log(err)
					}	
				)
			},
			rankChange(){
				this.curPage = 1
				const formData = new FormData()
				formData.append('page', this.curPage)
				formData.append('sort', this.rankValue)

				this.$http.post('/spaces/1/questions', formData).then(
					res => {
						this.questions = res.data.list
						this.questions.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
						value.last_update_time = value.last_update_time.slice(0, 10)
					})
					},
					err => {
						console.log(err)
					}	
				)
			},
		},
		mounted() {
			this.isLoading = true
			const formData = new FormData()
			formData.append('page', this.curPage)
			formData.append('sort', this.rankValue)

			this.$http.post('/spaces/1/questions', formData).then(
				res => {
					this.questions = res.data.list
					this.total = res.data.total
					this.questions.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
						value.last_update_time = value.last_update_time.slice(0, 10)
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
	
</style>