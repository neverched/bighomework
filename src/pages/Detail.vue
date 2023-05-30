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
                            <el-text class="pop-info user">
                                <el-avatar>  
                                    <el-icon><UserFilled /></el-icon>
                                </el-avatar>
                                {{info.user.userName}}
                            </el-text>
                            <el-button type="primary" class="right">关注</el-button>
                            <el-divider />

                            <el-row class="pop-info" justify="space-between">
                                <el-col :span="4">
                                    <el-text>资源</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>评论</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>习题</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>粉丝</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>获赞</el-text>
                                </el-col>
                            </el-row>
                            <el-row class="pop-info" justify="space-between">
                                <el-col :span="4">
                                    <el-text>{{info.user.resNum}}</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>{{info.user.comNum}}</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>{{info.user.exerNum}} </el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>{{info.user.fansNum}}</el-text>
                                </el-col>
                                <el-col :span="4">
                                    <el-text>{{info.user.thumbsUpNum}}</el-text>
                                </el-col>
                            </el-row>
                        </template>
                    </el-popover>

                    {{info.user.userName}} - 创建于{{info.createDate}}
                    <br>
                </el-text>
                <el-text class="title">
                    {{info.title}}
                    <br>
                </el-text>
                <el-text>
                    <br>
                    {{info.detail}}
                    <br>
                    <br>
                </el-text>
                <el-button type="primary" plain >点赞</el-button>
                <el-button type="primary" plain >收藏</el-button>
                <el-button type="primary" plain @click="isComment = !isComment">评论</el-button>
                <el-row v-show="isComment" style="margin-top:5px;">
                    <el-col :span="20">
                        <el-input
                            v-model="newComment"
                            :rows="2"
                            type="textarea"
                            placeholder="Please input"
                        />
                    </el-col>
                    <el-col :span="3">
                        <el-button type="primary" plain style="height:50px;">发布</el-button>
                    </el-col>
                </el-row>
			</el-card>
            <el-card class="box-card" style="margin-top: 20px">
				<template #header>
					<div class="card-header">
                        <el-text class="sum">共{{info.comments.length}}条评论</el-text>
						<el-select v-model="rankValue" class="m-2" placeholder="最新发布">
							<el-option
								v-for="item in rankOptions"
								:key="item.value"
								:label="item.label"
								:value="item.value"
							/>
						</el-select>
					</div>
				</template>
                
                <Comment 
                    v-for="c in  info.comments"
                    :key="c.id"
                    :comment="c"
                />
                
			</el-card>
		</el-col>
	</el-row>
</template>

<script>
    import Comment from '../components/Comment'

    export default {
        name:'Detail',
        components:{Comment},
        props:['id'],
        data() {
            return {
                info:{
                    id:'r0',title:'Python基于SQLite实现消息队列',
                    user:{userName:'张三',resNum:10,comNum:5,exerNum:3,fansNum:30,thumbsUpNum:101},
                    thumbsUpNum:0,createDate:'2022-10-01',updateDate:'2023-01-01',
                    detail:'从高内聚度角度考虑，将多个分析类合并为单个设计类会导致该设计类承担多个职责，因此这个设计类的内部逻辑会变得复杂，不利于代码的维护和扩展。相反，如果我们将每个分析类都进行精细的设计，使得每个设计类都只负责一项或几项职责，那么每个设计类的内部逻辑就会更加简洁明了，便于理解和修改，从而提高了代码的内聚度。',
                    comments:[
                        {id:'0', user:{name:'tom'}, date:'2002-09-01', content:'权限不足，无法修改'},
                        {id:'0', user:{name:'aas'}, date:'2002-09-01', content:'那这个APP岂不是要常驻后台？而且需要多个权限来打开传感器，会产生个人隐私和手机资源占用等问题。从高内聚度角度考虑，将多个分析类合并为单个设计类会导致该设计类承担多个职责，因此这个设计类的内部逻辑会变得复杂，不利于代码的维护和扩展。'},
                        {id:'0', user:{name:'qw'}, date:'2002-09-01', content:'aaa'},
                        {id:'0', user:{name:'eqw'}, date:'2002-09-01', content:'sss'},
                        {id:'0', user:{name:'asas'}, date:'2002-09-01', content:'bbb'},
                    ]
                },
                rankOptions: [
					{value: '最新发布',label: '最新发布'},
					{value: '最多点赞',label: '最多点赞'},
				],
                rankValue:'',
                newComment:'',
                isComment:false
            }
        },
        methods:{

        },
        // mounted(){
        //     this.$http.get(`/resource/${this.id}`).then(
        //         res => {
        //             this.info = res.data
        //         },
        //         err => {
        //             console.log(err)
        //         }
        //     )
        // }
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