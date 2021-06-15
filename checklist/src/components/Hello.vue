<template>
  <div>
    <el-drawer
      title="测试用例清单"
      :visible.sync="drawer"
    size="50%">
      <el-table :data="suiteData">
        <el-table-column property="test" label="类型" width="150"></el-table-column>
        <el-table-column property="name" label="名称" width="200"></el-table-column>
        <el-table-column property="capability" label="能力/功能"></el-table-column>
        <el-table-column property="description" label="描述"></el-table-column>
      </el-table>
    </el-drawer>
    <el-dialog title="测试用例详情" :visible.sync="dialogFormVisible">
      <el-form :model="suiteForm">
        <el-form-item label="类型" >
          <el-select v-model="suiteForm.type" placeholder="请选择">
            <el-option label="MFT" value="MFT"></el-option>
            <el-option label="INV" value="INV"></el-option>
            <el-option label="DIR" value="DIR"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="名称" >
          <el-input v-model="suiteForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="标签" >
          <el-input v-model="suiteForm.label" autocomplete="off" placeholder="请输入半角阿拉伯数字"></el-input>
        </el-form-item>
        <el-form-item label="功能" >
          <el-input v-model="suiteForm.capability" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="描述" >
          <el-input v-model="suiteForm.description" type="textarea" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="addTestSuite()">确 定</el-button>
      </div>
    </el-dialog>
    <el-row>

      <el-divider></el-divider>
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="模板">
          <el-input v-model="formInline.template" placeholder="请输入模板"></el-input>
        </el-form-item>
        <el-form-item label="生成数量">
          <el-input v-model="formInline.number" placeholder="10"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">生成模板</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getSuggestion">MASK建议</el-button>
        </el-form-item>
        <el-form-item style="float:right">
          <el-button type="primary" @click="drawer = true" >查看当前测试用例</el-button>
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
    <el-row>
      <el-form :inline="true"  class="demo-form-inline" style="float:right">
        <el-form-item>
          <el-button type="primary" @click="dialogFormVisible = true" >增加测试用例</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <div style="margin-bottom: 20px;">
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
          <el-form-item label="词汇表名称">
            <el-input v-model="lexiconForm.key"  placeholder="例:country"></el-input>
          </el-form-item>
          <el-form-item label="词汇表内容">
            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 8}" v-model="lexiconForm.lexiconList" placeholder='例: ["good","great"](英文标点符号、引号用双引号)'></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary"
                       @click="addLexicon">增加词汇表</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-tabs v-model="activeName" type="border-card" @tab-click="handleClick">
        <el-tab-pane v-for="(item,index) in lexicons" :key="item.key" :label="item.key">
          <div v-for="(item2,index2) in item">
            <div v-if="typeof item2 =='object'">
              {{item2}}
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
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

      const generateLexicons = _ => {
        const tempLexicon = [];
        axios({
          method:'post',
          url:'http://192.168.71.214:5000/loadLexicons',
        }).then((response)=>{
          console.log(response.data);
          for (var key in response.data){
            tempLexicon.push({
              key: key,
              words: response.data[key]
            })
          }
        })
          .catch((error)=>{
            console.log(error)
            this.$notify.warning({
              title: '警告',
              message: `输出异常`
            });
          })
        return tempLexicon;
      };

      return {
        drawer: false,
        dialogFormVisible: false,
        suiteData: [{
          name:'ste',
        }],
        url:"http://192.168.71.214:5000/",
        formInline:{
          template:'',
          number:'10',
        },
        lexiconForm:{
          key:'',
          lexiconList:'',
        },
        suiteForm:{
          type:'',
          name:'',
          label:'',
          description:'',
          capability:'',
        },
        data: generateData(),
        lexicons: generateLexicons(),
        activeNames: ['1'],
        value: [],
        count: 0,
        filterMethod(query, item) {
          return item.pinyin.indexOf(query) > -1;
        }
      };

    },
    methods: {
      getLexicons(){
        const tempLexicon=[]
        axios({
          method:'post',
          url:this.url+'loadLexicons',
        }).then((response)=>{
          for (var key in response.data){
            tempLexicon.push({
              key: key,
              words: response.data[key]
            })
          }
          this.lexicons=tempLexicon;
          this.$message.success("成功更新词汇表");
        })
          .catch((error)=>{
            console.log(error)
            this.$notify.warning({
              title: '警告',
              message: '输出异常'
            });
          })
      },
      handleClick(tab, event) {
        console.log(tab, event);
      },
      addLexicon() {
        const tempLexicon=[]
        axios({
          method:'post',
          url:this.url+'addLexicon',
          data: {'key': this.lexiconForm.key,
            'lexiconList': this.lexiconForm.lexiconList},
        }).then((response)=>{
          for (var key in response.data){
            tempLexicon.push({
              key: key,
              words: response.data[key]
            })
          }
          this.lexicons=tempLexicon;
          this.$message.success("成功添加词汇表");
        })
          .catch((error)=>{
            console.log(error)
            this.$notify.warning({
              title: '警告',
              message: '输出异常'
            });
          })
      },
      handleChange(val) {
        console.log(val);
      },
      addTestSuite(){
        console.log(this.data)
        console.log(this.value)
        //保留data[value],删除data未选中内容
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
        axios({
          method:'post',
          url:this.url+'addTestSuite',
          data: {'type': this.suiteForm.type,
            'name': this.suiteForm.name,
            'labels': this.suiteForm.label,
            'capability': this.suiteForm.capability,
          'description': this.suiteForm.description,
          'sentences': this.data,
          },
        }).then((response)=>{

          this.$message.success("成功添加测试");
        })
          .catch((error)=>{
            console.log(error)
            this.$notify.warning({
              title: '警告',
              message: '输出异常'
            });
          })
      },
      onSubmit(){
        console.log('submit');
        axios({
          method:'post',
          url:this.url+'template',
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
      getSuggestion(){
        console.log('submit');
        axios({
          method:'post',
          url:this.url+'getSuggestion',
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
