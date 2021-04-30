<template>
  <div class="demo-image__placeholder">
    <div class="block">
      <span class="demonstration"></span>
      <el-image :src="src" style="width: 35%; height: 35%" :fit="contain">
        <div slot="placeholder" class="image-slot">
          加载中<span class="dot">...</span>
        </div>
      </el-image>
    </div>
  </div>
</template>

<script>
  export default {
    props: [
      'geturl'
    ],
    data() {
      return {
        src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
      }
    },
    watch:{     //监听value的变化，进行相应的操作即可
      "geturl": {
        immediate:false,
        handler:function(newValue, oldValue) {
          let tempStr = newValue;
          this.src = 'data:image/png;base64,' + tempStr;
          //console.log(typeof newValue)
        },
      }
    }
  }
</script>

<style scoped>

</style>
