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
							<span>上传资源</span>
							<el-icon><Plus /></el-icon>
						</el-button>
					</div>
				</template>
				
				<MyItem
					v-for="r in resources"
					:key="r.id"
					:item="r"
				/>
				<el-pagination 
					background 
					layout="prev, pager, next" 
					:total="100"
					@current-change="pageChange"
				/>
				
			</el-card>
		</el-col>
	</el-row>
</template>

<script>
	import MyItem from './MyItem'

	export default {
		name:'QuestionList',
		components:{MyItem},
        data() {
			return {
				rankValue:'',
				rankOptions: [
					{value: '最新发布',label: '最新发布'},
					{value: '最多点赞',label: '最多点赞'},
					{value: '最多讨论',label: '最多讨论'},
				],
				resources: [
					{id:'r0',title:'Python基于SQLite实现消息队列',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'r1',title:'Python基于SQLite实现消息队列',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'r2',title:'Python基于SQLite实现消息队列',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'r3',title:'Python基于SQLite实现消息队列',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'r4',title:'Python基于SQLite实现消息队列',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
				],
			}
		},
		methods:{
			pageChange(curPage){
				this.$http.get('http://127.0.0.1:8000/', {
					params: {
						page: curPage,
						rank: this.rankValue
					}
				}).then(
					res => {
						this.resources = res.data
					},
					err => {
						console.log(err)
					}	
				)
			},
			rankChange(){
				this.$http.get('/resource', {
					params: {
						page: 1,
						rank: this.rankValue
					}
				}).then(
					res => {
						this.resources = res.data
					},
					err => {
						console.log(err)
					}	
				)
			}
		},
		// mounted() {
		// 	this.$http.get('/resource', {
		// 		params: {
		// 			page: 1,
		// 			rank: '最新发布'
		// 		}
		// 	}).then(
		// 		res => {
		// 			this.resources = res.data
		// 		},
		// 		err => {
		// 			console.log(err)
		// 		}	
		// 	)
		// }
	}
</script>

<style scoped>
	
</style>