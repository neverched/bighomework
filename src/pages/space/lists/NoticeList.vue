<template>
	<el-row>
		<el-col :span="20" :offset="2">	
			<el-card class="box-card">
				<template #header>
					<div class="card-header">
						<el-button type="primary" plain id="create-ques">
							<span>发布公告</span>
							<el-icon><Plus /></el-icon>
						</el-button>
					</div>
				</template>

				<div v-loading="isLoading" style="height:200px;" v-show="isLoading"></div>
				<MyItem
					v-for="n in notices"
					:key="n.id"
					:item="n"
					type="notices"
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
				notices:[],
				isLoading:false,
				total:0,
				curPage:1
			}
		},
		methods:{
			pageChange(){
				const formData = new FormData()
				formData.append('page', this.curPage)

				this.$http.post('/spaces/1/notices', formData).then(
					res => {
						this.notices = res.data.list
						this.notices.forEach((value) => {
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

			this.$http.post('/spaces/1/notices', formData).then(
				res => {
					this.notices = res.data.list
					this.total = res.data.total
					this.notices.forEach((value) => {
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