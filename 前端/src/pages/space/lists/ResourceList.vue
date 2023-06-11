<template>
	<div>
		<el-row>
			<el-col :span="20" :offset="2">
				<el-card class="box-card">
					<template #header>
						<div class="card-header">
							<el-select v-model="rankValue" class="m-2" placeholder="最近更新" @change="rankChange">
								<el-option v-for="item in rankOptions" :key="item.value" :label="item.label" :value="item.value" />
							</el-select>

							<el-button type="primary" plain id="create-ques" style="margin-left: 20px;" @click="toUpload">
								<span>上传文件</span>
								<el-icon>
									<Plus />
								</el-icon>
							</el-button>
							<el-button type="primary" plain id="create-ques" style="margin-left: 20px;" @click="toEdit">
								<span>在线编辑</span>
								<el-icon>
									<Plus />
								</el-icon>
							</el-button>
						</div>
					</template>

					<div v-loading="isLoading" style="height:200px;" v-show="isLoading"></div>
					<MyItem v-for="r in resources" :key="r.id" :item="r" type="resources" />
					<el-pagination background layout="prev, pager, next" :total="total" @current-change="pageChange"
						v-show="!isLoading" v-model:current-page="curPage" />

				</el-card>
			</el-col>
		</el-row>
	</div>
</template>

<script>
import MyItem from '../MyItem'

export default {
	name: 'QuestionList',
	components: { MyItem },
	data() {
		return {
			rankValue: '最近更新',
			rankOptions: [
				{ value: '最近更新', label: '最近更新' },
				{ value: '最多点赞', label: '最多点赞' },
				{ value: '资源标题', label: '资源标题' },
			],
			resources: [],
			isLoading: false,
			total: 0,
			curPage: 1
		}
	},
	methods: {
		pageChange() {
			const formData = new FormData()
			formData.append('page', this.curPage)
			formData.append('sort', this.rankValue)

			this.$http.post('/spaces/1/resources', formData).then(
				res => {
					this.resources = res.data.list
					this.resources.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
						value.last_update_time = value.last_update_time.slice(0, 10)
					})
				},
				err => {
					console.log(err)
				}
			)
		},
		rankChange() {
			this.curPage = 1
			const formData = new FormData()
			formData.append('page', this.curPage)
			formData.append('sort', this.rankValue)

			this.$http.post('/spaces/1/resources', formData).then(
				res => {
					this.resources = res.data.list
					this.resources.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
						value.last_update_time = value.last_update_time.slice(0, 10)
					})
				},
				err => {
					console.log(err)
				}
			)
		},
		toUpload() {
			this.$router.push({
				name: 'upload'
			})
		},
		toEdit() {
			this.$router.push({
				name: 'ResourceEdit'
			})
		}
	},
	mounted() {
		this.isLoading = true
		const formData = new FormData()
		formData.append('page', this.curPage)
		formData.append('sort', this.rankValue)

		this.$http.post('/spaces/1/resources', formData).then(
			res => {
				this.resources = res.data.list
				this.total = res.data.total
				this.resources.forEach((value) => {
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
.content {
	height: 540px;
	/* 容器高度 */
	width: 100%;
	/* 容器宽度 */
	padding: 10px;
	/* 可选。内容与容器的内边距 */
	box-sizing: border-box;
	/* 可选。将内边距纳入容器宽高计算 */
	overflow: auto;
	/* 让内容超出容器尺寸时出现滚动条 */
}
</style>