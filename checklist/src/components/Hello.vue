<template>
  <div>
    <el-row>
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="模板">
          <el-input v-model="formInline.template" placeholder="请输入模板"></el-input>
        </el-form-item>
        <el-form-item label="生成数量">
          <el-input v-model="formInline.number" placeholder="10"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">生成</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-row>
      <el-col :span="24">
        <div class="grid-content bg-purple-light">
        <el-transfer
        filterable
        :filter-method="filterMethod"
        filter-placeholder="请输入搜索内容"
        :titles="['待选用例','测试用例']"
        v-model="value"
        :data="data">
      </el-transfer>
        </div>
      </el-col>
    </el-row>
  </div>


</template>

<script>
  import axios from 'axios';
  export default {
    name: 'Hello',
    data() {
      const generateData = _ => {
        const data = [];
        const cities = [];
        const pinyin = [];
        cities.forEach((city, index) => {
          data.push({
            label: city,
            key: index,
            pinyin: pinyin[index]
          });
        });
        return data;
      };
      return {
        url:"http://192.168.71.214:5000/template",
        formInline:{
          template:'',
          number:'10',
        },
        data: generateData(),
        value: [],
        count: 0,
        filterMethod(query, item) {
          return item.pinyin.indexOf(query) > -1;
        }
      };
    },
    methods: {
      onSubmit(){
        console.log('submit');
        axios({
          method:'post',
          url:this.url,
          data: {'template': this.formInline.template,
          'number': this.formInline.number},
        })
        .then((response)=>{
          for (var i=this.data.length-1; i>=0; i-=1){
            var flag=0;
            for (var j=this.value.length-1; j>=0; j-=1){
              if (this.value[j]==this.data[i].key){
                console.log(this.value[j],' ',this.data[i].key)
                flag=1;
                break;
              }
            }
            if (flag==0){
              console.log('del:',i)
              this.data.splice(i,1);
            }
          }

          console.log(response.data)
          for (var i in response.data){
            this.data.push({
              label:response.data[i],
              key:this.count,
              pinyin:response.data[i],
            })
            this.count+=1
          }
          console.log(this.count)
        })
        .catch((error)=>{
          console.log(error)
          this.$notify.warning({
            title: '警告',
            message: `输出异常`
          });
        })
      },
    },
    components:{

    }
  }

</script>
<style>
  .el-transfer-panel{
    width:40%;
  }
  .el-transfer__buttons{
    width:15%;
    text-align:center;
  }
  .el-row {
    margin-bottom: 20px;
  &:last-child {
     margin-bottom:   0;
   }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }

  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
