<template>
  <div class="root">
    <el-row class="top">
      <el-col :span="24" >
            <div>
              <router-link to="/">
                <img src="../assets/logo2.png" alt="logo" style="position: relative;width: 65%; float:left;margin-top: 0px">
                <img src="../assets/sstl.png" style="width:20%;margin:10px;float:right">
              </router-link>
            </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
name: "boldHeader"
}
</script>

<style scoped>
.root{
  background-image: url("../assets/background.svg");
  background-repeat: no-repeat;
}
.top{
  box-shadow: 0px 1px 2px 2px #f5f6f6;
}
.header{
  background: #ffffff;
  border: black;
}

</style>
