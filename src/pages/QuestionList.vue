<template>
	<el-row>
		<el-col :span="20" :offset="2">	
			<el-card class="box-card">
				<template #header>
					<div class="card-header">
						<el-select v-model="rankValue" class="m-2" placeholder="最新发布">
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
				
				<MyItem
					v-for="q in questions"
					:key="q.id"
					:item="q"
				/>

				
				<el-pagination background layout="prev, pager, next" :total="100"/>
				
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
				isAllValue:'',
				rankValue:'',
				rankOptions: [
					{value: '最新发布',label: '最新发布'},
					{value: '最多点赞',label: '最多点赞'},
					{value: '最多讨论',label: '最多讨论'},
				],
				questions: [
					{id:'q0',title:'代码重用时获取代码的途径',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'q1',title:'代码重用时获取代码的途径',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'q2',title:'代码重用时获取代码的途径',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'q3',title:'代码重用时获取代码的途径',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
					{id:'q4',title:'代码重用时获取代码的途径',user:{userName:'张三'},thumbsUpNum:0,disscussNum:10,createDate:'2022-10-01',updateDate:'2023-01-01'},
				],
			}
		}
	}
</script>

<style scoped>
	
</style>