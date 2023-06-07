<template>
    <el-row>
		<el-col :span="20" :offset="2">	
			<el-card class="box-card">
				<el-text>
                    <el-popover
                        :width="300"
                        popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;"
                    >
                        <template #reference>
                            <el-avatar>  
                                <el-icon><UserFilled /></el-icon>
                            </el-avatar>
                        </template>
                        <template #default>
                            <el-text class="pop-info user" @click="toUser">
                                <el-avatar>  
                                    <el-icon><UserFilled /></el-icon>
                                </el-avatar>
                                {{info.creator.username}}
                            </el-text>
                            <el-button type="primary" class="right">关注</el-button>
                            <el-divider />

                            <el-row class="pop-info" justify="space-between">
                                <el-col :span="6">
                                    <el-text>关注</el-text>
                                </el-col>
                                <el-col :span="6">
                                    <el-text>粉丝</el-text>
                                </el-col>
                                <el-col :span="6">
                                    <el-text>获赞</el-text>
                                </el-col>
                            </el-row>
                            <el-row class="pop-info" justify="space-between">
                                <el-col :span="6">
                                    <el-text>{{info.creator.followings}}</el-text>
                                </el-col>
                                <el-col :span="6">
                                    <el-text>{{info.creator.followers}}</el-text>
                                </el-col>
                                <el-col :span="6">
                                    <el-text>{{info.creator.like}} </el-text>
                                </el-col>
                            </el-row>
                        </template>
                    </el-popover>

                    {{info.creator.username}} - 创建于{{info.create_time}}
                    <br>
                </el-text>
                <el-text class="title">
                    {{info.title}}
                    <br>
                </el-text>
                <el-text>
                    <br>
                    {{info.content}}
                    <br>
                    <br>
                </el-text>
                <el-button type="primary" plain 
                    v-show="type == 'exercises'" 
                    @click="isShowAnswer = !isShowAnswer"
                    style="margin-bottom:5px;"
                >查看答案</el-button>

                <el-row v-if="isShowAnswer">
                    <el-col :span="22">
                        <el-card class="box-card" style="margin-bottom:5px;">
                            <el-text>
                                {{info.answer}}
                                <br>
                            </el-text>
                        </el-card>
                    </el-col>
                </el-row>

                <div v-show="this.type != 'notices'">
                    <el-button type="primary" plain 
                        @click="like" 
                        v-if="!info.ele_liked"
                    >点赞 {{info.likes}} </el-button>
                    <el-button type="primary" plain 
                        @click="like" 
                        v-else
                    >取消点赞 {{info.likes}} </el-button>

                    <el-button type="primary" plain 
                        @click="follow"
                        v-if="!info.ele_followed"
                    >收藏 {{info.follows}} </el-button>
                    <el-button type="primary" plain 
                        @click="follow"
                        v-else
                    >取消收藏 {{info.follows}} </el-button>

                    <el-button type="primary" plain 
                        @click="isComment = !isComment" 
                        v-show="this.type != 'notices'"
                    >评论</el-button>
               </div>
                
                <el-row v-show="isComment" style="margin-top:5px;">
                    <el-col :span="20">
                        <el-input
                            v-model="newComment"
                            :rows="4"
                            type="textarea"
                            placeholder="Please input"
                        />
                    </el-col>
                    <el-col :span="3">
                        <el-button type="primary" plain style="height:90px;" @click="addComment">发布</el-button>
                    </el-col>
                </el-row>
			</el-card>
            <el-card class="box-card" style="margin-top: 20px">
				<template #header>
					<div class="card-header">
                        <el-text class="sum">共{{comments.length}}条评论</el-text>
					</div>
				</template>
                
                <Comment 
                    v-for="c in comments"
                    :key="c.id"
                    :comment="c"
                />
                
			</el-card>
		</el-col>
	</el-row>
</template>

<script>
    import Comment from './Comment'

    export default {
        name:'Detail',
        components:{Comment},
        props:['id','type'],
        data() {
            return {
                info:{
                    creator:{}
                },
                newComment:'',
                isComment:false,
                comments:[],
                isShowAnswer:false,
            }
        },
        methods:{
            toUser(){
                this.$router.push({
					name:'user',
					params:{
						id:this.info.user.id
					}
				})
            },
            addComment(){
                if(!this.newComment.trim()) {
                    this.$message('评论不能为空')
                    return
                }
                const formData = new FormData()
				formData.append('is_comment', 1)
                formData.append('content', this.newComment)
                this.$http.post(`spaces/1/${this.type}/${this.id}`,formData).then(
                    res => {
                        if(res.data.msg == '评论成功') {
                            this.$message('评论成功')
                            this.newComment = ''
                            this.$http.post(`spaces/1/${this.type}/${this.id}`).then(
                                res => {
                                    this.comments = res.data.comments_list
                                    this.comments.forEach((value) => {
                                        value.create_time = value.create_time.slice(0, 10)
                                    })
                                },
                                err => {
                                    console.log(err)
                                }
                            )
                        } else {
                            this.$message('尚未登录，请先登录')
                        }
                    },
                    err => {
                        console.log(err)
                    }
                )
            },
            
            like(){
                const formData = new FormData()
				formData.append('is_like_element', '1')
                this.$http.post(`spaces/1/${this.type}/${this.id}`,formData).then(
                    res => {
                        console.log(res)
                        this.info = res.data.element
                        if(res.data.msg == '点赞/取消点赞元素成功') {
                            if(this.info.ele_liked) {
                                this.$message('点赞成功')
                                this.info.likes++
                            }
                            else {
                                this.$message('取消点赞成功')
                                this.info.likes--
                            }
                        }
                        else this.$message('尚未登录，请先登录')
                    },
                    err => {
                        console.log(err)
                    }
                )
            },

            follow(){
                const formData = new FormData()
				formData.append('is_follow_element', '1')
                this.$http.post(`spaces/1/${this.type}/${this.id}`,formData).then(
                    res => {
                        console.log(res)
                        this.info = res.data.element
                        if(res.data.msg == '收藏/取消收藏元素成功') {
                            if(this.info.ele_followed) {
                                this.$message('收藏成功')
                                this.info.follows++
                            }
                            else {
                                this.$message('取消收藏成功')
                                this.info.follows--
                            }
                        }
                        else this.$message('尚未登录，请先登录')
                    },
                    err => {
                        console.log(err)
                    }
                )
            }
        },
        mounted(){
            this.$http.post(`spaces/1/${this.type}/${this.id}`).then(
                res => {
                    console.log(res)
                    this.info = res.data.element
                    if(res.data.comments_list != null) this.comments = res.data.comments_list
                    this.comments.forEach((value) => {
						value.create_time = value.create_time.slice(0, 10)
					})
                    this.info.create_time = this.info.create_time.slice(0, 10)
                },
                err => {
                    console.log(err)
                }
            )
        }
    }
</script>

<style scoped>
    .title {
        font-size: 30px;
        font-weight: bold;
    }
    .sum {
        font-weight: bold;
        margin-right: 10px;
    }
    .right {
        float: right;
    }
    .pop-info {
        font-weight: bold;
        font-size: 15px;
    }
    .user:hover {
        cursor: pointer;
    }
</style>