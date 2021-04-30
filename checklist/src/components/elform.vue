<template>
  <el-form :inline="true" :model="formInline" class="demo-form-inline">
    <el-form-item label=图片为真实人脸的概率：>
      <el-input v-model="form.accuracy" :disabled=true  placeholder="请上传图片后点击检测"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit"> 检测</el-button>
    </el-form-item>


  </el-form>
</template>

<script>
  import axios from 'axios';
    export default {
      name: "eleform",
      props: [
        "geturl"
      ],
      data() {
        return {
          showAcc: true,
          inputAnswer: false,
          url:"http://192.168.71.214:5000/face_forgery",
          useLarge: false,
          form: {
            picurl:'',
            accuracy:'',
          }
        }
      },
      methods: {
        agreeChange:function(val){
          this.inputAnswer=(val=='1')?false:true;
        },
        onSubmit() {
          if(this.form.picurl==''||this.form.picurl==null||this.form.picurl==undefined){
            console.log('empty')
            this.$notify.warning({
              title: '警告',
              message: '未上传图片'
            });
          }else{
            this.$message.success("提交成功,请耐心等待输出结果,一般等待时间不超过10秒");
            let data = new FormData(); // FormData 对象
            data.append("picurl", this.form.picurl);
            axios({
              method: 'post',
              url: this.url,
              data: data,
              headers: {'Content-Type': 'multipart/form-data'}
            }).then(res => {
              console.log(res);
              this.form.accuracy = res.data.probability;
            }).catch((error) => {
              // eslint-disable-next-line
              this.temp1 = "输出异常，可能是输入格式错误，请仔细核对格式说明并点击清空或刷新页面重试。"
              this.ans = '';
              this.temp2 = '';
              this.acc = '';
              this.showAns = true;
              console.error(error);
            });
          }
        },
        onClear() {
          this.form.article='';
          this.form.mask='';
          this.form.options='';
          this.form.answers='';
          this.showAns=false;
        }
      },
      watch:{     //监听value的变化，进行相应的操作即可

        "geturl": {
          immediate: false,
          handler:function(newValue, oldValue) {
            let tempStr = newValue;
            this.form.picurl = tempStr;
            this.form.accuracy = '上传成功，请点击检测按钮';
            //console.log(typeof newValue)
          },
        }
      }
    }
</script>

<style >
  .el-row {
    margin-top:18px;
    margin-bottom: 20px;
  &:last-child {
     margin-bottom: 0;
   }
  }
</style>
