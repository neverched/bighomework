<template lang="">
  <div>
    <div class="side-container">
      <div class="box-card fans-view">
        <div class="box-card-son">
          <div class="box-card-son-data can-click">{{ boxData.fans }}</div>
          <div class="box-card-son-title">粉丝</div>
        </div>
        <div class="box-card-son">
          <div class="box-card-son-data can-click">{{ boxData.follows }}</div>
          <div class="box-card-son-title">关注</div>
        </div>
        <div class="box-card-son">
          <div class="box-card-son-data">{{ boxData.likes }}</div>
          <div class="box-card-son-title">获赞</div>
        </div>
      </div>

      <div v-show="recentWrites.length" class="box-card write-box">
        <div class="write-title">
          最近创作
        </div>
        <div v-for="item in recentWrites" :key="item.id" class="item">{{ item.content }}</div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, defineEmits, onMounted } from 'vue'
import api from '@/plugins/axiosInstance'

const emit = defineEmits(['changeUserMainTabs'])

let recentWrites = reactive(new Array())

let boxData = reactive({
  fans: 1,
  follows: 2,
  likes: 12
})

const handleClickFans = () => {
  emit('changeUserMainTabs', 'follows')
  // _this.$router.push({
  //   name: 'following',
  //   params: {
  //     type: 'follows'
  //   }
  // })
}

const handleClickFollowing = () => {
  emit('changeUserMainTabs', 'following')
  // _this.$router.push({
  //   name: 'following',
  //   params: {
  //     type: 'following'
  //   }
  // })
}

let userid = -1;

onMounted(() => {
  api.get('give').then(res => {
    if (res.data.error == 1) {
      userid = res.data.data;
    } else {
      return;
    }
    api.get('user/' + userid.toString()).then(res => {
      if (res.data.error == 1) {
        const data = res.data;
        boxData.fans = data.followers;
        boxData.follows = data.followings;
        boxData.likes = data.like;
      } else {
        return;
      }
    }).catch(err => {
      console.log(err);
    })
    api.get('user/' + userid.toString() + '/resent').then(res => {
      if (res.data.error == 1) {
        const datas = res.data.data;
        let cnt = 0;
        for (let data of datas) {
          cnt += 1;
          recentWrites.push({
            id: cnt,
            content: data.title
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
})


/* const handleItemClick = (item) => {
  // 这里应该实现跳转到文章详情页
  console.log('item click', item.id)
} */
</script>
<style scoped>
.side-container {
  width: 270px;
  border-radius: 8px;
  /* background-color: yellow; */
  display: flex;
  flex-direction: column;
}

.side-container>div {
  margin-bottom: 10px;
}

.box-card {
  width: 100%;
  height: auto;
  border-radius: 8px;
  background-color: #fff;
}

.fans-view {
  height: 90px;
  display: flex;
}

.fans-view :nth-child(1) {
  width: 89px;
  height: 90px;
  border-radius: 8px 0 0 8px;
  border-right: 1px solid #ebebeb;
}

.fans-view :nth-child(2) {
  width: 90px;
  height: 90px;
  border-radius: 8px 0 0 8px;
}

.fans-view :nth-child(3) {
  width: 89px;
  height: 90px;
  border-radius: 0 8px 8px 0;
  border-left: 1px solid #ebebeb;
}

.box-card-son {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.box-card-son :nth-child(1) {
  font-size: large;
  font-weight: bolder;
}

.box-card-son-data {
  display: flex;
  justify-content: center;
  align-items: end;
}

.box-card-son-title {
  display: flex;
  justify-content: center;
  align-items: start;
}

/* .can-click:hover {
  color: #409EFF;
  cursor: pointer;
} */

.write-box {
  padding: 10px;
  box-sizing: border-box;
}

.write-title {
  font-size: larger;
  font-weight: bold;
  margin-bottom: 5px;
  padding-left: 5px;
}

.item {
  margin-bottom: 10px;
  /* background-color: beige; */
  box-sizing: border-box;
  padding: 5px;
}

.item:hover {
  background-color: #f6f6f6;
  cursor: pointer;
}
</style>