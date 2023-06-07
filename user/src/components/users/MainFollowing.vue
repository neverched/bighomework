<template lang="">
  <div>
    <div class="main-container">
      <el-tabs v-model="activeName" class="demo-tabs main-header">
        <el-tab-pane label="我的粉丝" name="follows"></el-tab-pane>
        <el-tab-pane label="我关注的人" name="following"></el-tab-pane>
      </el-tabs>
      <div class="main-body">
        <div v-if="activeName == 'follows'">
          <div class="main-body-item" v-for="fans in followsList" :key="fans.uid">
            <el-row>
              <el-col :span="12">
                <el-row style="flex-wrap: wrap;">
                  <el-text class="fans-title" size="large" tag="b">
                    <el-icon><Avatar /></el-icon>
                    {{ fans.username }}
                  </el-text>
                  <el-tag style="margin-left: 5px" type="info" class="mx-1" effect="light" round>
                    <el-icon class="info-cion" v-if="fans.gender == 0" color="#409EFC">
                      <Male />
                    </el-icon>
                    <el-icon class="info-cion" v-else color="#F56C6C">
                      <Female />
                    </el-icon>
                    {{ gender2Chinese(fans.gender) }}
                  </el-tag>
                  <el-tag style="margin-left: 5px" v-if="fans.address" type="info" class="mx-1" effect="light" round>
                    <el-icon class="info-cion" color="#f8e3c5">
                      <Location />
                    </el-icon>
                    {{ fans.address }}
                  </el-tag>
                </el-row>
                <el-row>
                  <el-text type="info">{{fans.likes}}获赞-{{fans.follows}}粉丝</el-text>
                </el-row>
              </el-col>
              <el-col :span="12" style="display: flex; justify-content: end; align-items: center;">
                <el-button :type="fans.buttonType" @click="handleClickFollowBtn(fans)">
                  {{getButtonContent(fans.buttonType)}}
                </el-button>
              </el-col>
            </el-row>
          </div>
        </div>
        <div v-else>
          <div class="main-body-item" v-for="up in followingList" :key="up.uid">
            <el-row>
              <el-col :span="12">
                <el-row style="flex-wrap: wrap;">
                  <el-text class="fans-title" size="large" tag="b">
                    <el-icon><Avatar /></el-icon>
                    {{ up.username }}
                  </el-text>
                  <el-tag style="margin-left: 5px" type="info" class="mx-1" effect="light" round>
                    <el-icon class="info-cion" v-if="up.gender == 0" color="#409EFC">
                      <Male />
                    </el-icon>
                    <el-icon class="info-cion" v-else color="#F56C6C">
                      <Female />
                    </el-icon>
                    {{ gender2Chinese(up.gender) }}
                  </el-tag>
                  <el-tag style="margin-left: 5px" v-if="up.address" type="info" class="mx-1" effect="light" round>
                    <el-icon class="info-cion" color="#f8e3c5">
                      <Location />
                    </el-icon>
                    {{ up.address }}
                  </el-tag>
                </el-row>
                <el-row>
                  <el-text type="info">{{up.likes}}获赞-{{up.follows}}粉丝</el-text>
                </el-row>
              </el-col>
              <el-col :span="12" style="display: flex; justify-content: end; align-items: center;">
                <el-button :type="up.buttonType" @click="handleClickFollowBtn(up)">
                  {{getButtonContent(up.buttonType)}}
                </el-button>
              </el-col>
            </el-row>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref, onMounted, computed, getCurrentInstance, watch } from 'vue';
import api from '@/plugins/axiosInstance'

const instance = getCurrentInstance();

let _this = null

if (instance != null) {
  _this = instance.appContext.config.globalProperties //vue3获取当前this
}

let activeName = ref('follows')

let followsList = reactive(new Array())

let followingList = reactive(new Array())

const gender2Chinese = computed(() => (gender) => {
  return gender == 0 ? '男' : '女';
})

const getButtonContent = computed(() => (btnType) => {
  return btnType == 'primary' ? '+关注' : '已关注'
})

const handleClickFollowBtn = (fans) => {
  //表示现在已经是关注
  if (fans.buttonType == 'info') {
    fans.buttonType = 'primary'
    api.post('user/' + fans.uid.toString() + '/follow').catch(err => {
      console.log('取消关注失败', err)
    })
  } else {
    fans.buttonType = 'info'
    api.post('user/' + fans.uid.toString() + '/follow').catch(err => {
      console.log('关注失败', err)
    })
  }
}

watch(
  () => _this.$route.params.type,
  (newType) => {
    if (newType == 'follows' || newType == 'following') {
      activeName.value = newType;
    }
  }
)

let userid = -1;

onMounted(() => {
  api.get('give').then(res => {
    if (res.data.error == 1) {
      userid = res.data.data;
    } else {
      return;
    }
    api.get('user/' + userid.toString() + '/followings').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          followsList.push({
            uid: data.uid,
            username: data.username,
            likes: data.like_cnt,
            follows: data.fans_cnt,
            gender: data.gender,
            address: data.address,
            buttonType: 'primary'
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('user/' + userid.toString() + '/fans').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        for (let data of datas) {
          followingList.push({
            uid: data.uid,
            username: data.username,
            likes: data.like_cnt,
            follows: data.fans_cnt,
            gender: data.gender,
            address: data.address,
            buttonType: 'info'
          })
        }
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
  }).catch(err => {
    console.log(err);
  })
  activeName.value = _this.$route.params.type;
})

</script>

<style scoped>
.main-container {
  width: 100%;
  background-color: #fff;
}

.main-header {
  height: 50px;
  margin-left: 20px;
  margin-right: 20px;
  font-size: larger;
  font-weight: bolder;
  /* border-bottom: 1px solid #ebebeb; */
}

.main-body-item {
  padding: 20px;
  border-bottom: 1px solid #ebebeb;
}

.item-content {
  font-size: larger;
  font-weight: bolder;
}

.item-content:hover {
  color: #409eff;
  cursor: pointer;
}

.fans-title:hover {
  text-decoration: underline;
  cursor: pointer;
}

.space:hover {
  text-decoration: underline;
  cursor: pointer;
}

.info-cion {
  pointer-events: none;
}
</style>
