<template>
    <el-row>
        <el-col :span="6">
            <el-text>
                <el-avatar>  
                    <el-icon><UserFilled /></el-icon>
                </el-avatar>
                {{comment.user.name}} - 评论于 {{comment.date}}
            </el-text>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="22" :offset="1">
            <br>
            <el-text class="spacing">
                {{comment.content}}
            </el-text>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="4" :offset="20">
            <el-button type="primary" style="margin-top:10px;">点赞</el-button>
        </el-col>
    </el-row>
    <el-divider />
</template>

<script>
    export default {
        name:'Comment',
        props:['comment']
    }
</script>

<style>
</style>