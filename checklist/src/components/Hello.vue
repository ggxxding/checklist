<template>
  <div>
    <el-drawer
      title="测试用例清单"
      :visible.sync="drawer"
    size="50%">
      <el-button type='primary' @click="downloadSuite"  style="margin-left:4%;margin-right:4%">导出并下载</el-button>
      <el-collapse v-model="activeNames" style="margin-left:4%;margin-right:4%">
        <el-collapse-item  v-for="(suite,index) in suiteData" :key="index" :title="suite.name" :name="index">
          <div>类型:{{suite.type}}</div>
          <div>功能:{{suite.capability}}</div>
          <div>描述:{{suite.description}}</div>
          <div>标签:{{suite.labels}}</div>
          <div>数据:{{suite.data}}</div>
        </el-collapse-item>
      </el-collapse>
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
        <el-form-item v-show="suiteForm.type=='MFT'" label="标签" >
          <el-input v-model="suiteForm.label" autocomplete="off" placeholder="请输入半角阿拉伯数字"></el-input>
        </el-form-item>
        <el-form-item label="变化方向" v-show="suiteForm.type=='DIR'" >
          <el-select v-model="suiteForm.direction" placeholder="请选择">
            <el-option label="正向" value="increasing"></el-option>
            <el-option label="负向" value="decreasing"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="变化阈值" v-show="suiteForm.type=='DIR'" >
          <el-input v-model="suiteForm.tolerance" ></el-input>
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
    <el-dialog title="模板查询(请勿在构建测试用例中途修改语句数)" :visible.sync="templateFormVisible">
      <el-form  :model="templateForm" label-width="100px" class="demo-dynamic">
        <el-form-item  label="模板">
          <el-input v-model="templateForm.template"></el-input>
        </el-form-item>
        <el-form-item  v-for="(template, index) in templateForm.templates"
                       :label="'模板' + (Number(index)+2)"
                       :key="template.key">
          <el-input v-model="template.value"></el-input><el-button @click.prevent="removeTemplate(template)">删除</el-button>
        </el-form-item>
        <el-form-item label="数量">
          <el-input v-model="templateForm.number"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit()">查询模板</el-button>
          <el-button type="primary" @click="getSuggestion()">MASK建议</el-button>
          <el-button @click="addTemplate()">增加模板</el-button>
          <el-button @click="resetTemplateForm()">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-row>

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
        :data="data"
        @mouseover.native="transferAddTitle">
          <el-button class="transfer-footer" slot="left-footer" size="middle" @click="templateFormVisible = true">增加数据</el-button>
          <el-button class="transfer-footer" slot="right-footer" size="middle" @click="clearTemplates">清空数据</el-button>
      </el-transfer>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-form :inline="true"  class="demo-form-inline" style="float:right">
        <el-form-item>
          <el-button type="primary" @click="clearTemplates" >清空</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="dialogFormVisible = true" >增加测试用例</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="drawer = true" >查看测试用例</el-button>
        </el-form-item>
      </el-form>
    </el-row>
    <el-divider></el-divider>
    <el-row>
      <div style="margin-bottom: 20px;">
        <el-form :inline="true" :model="lexiconForm" class="demo-form-inline">
          <el-form-item label="词汇表名称">
            <el-input v-model="lexiconForm.key"  placeholder="例:country"></el-input>
          </el-form-item>
          <el-form-item label="词汇表内容">
            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 8}" v-model="lexiconForm.lexiconList" placeholder='例: [good,great](英文逗号)'></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary"
                       @click="addLexicon">增加词汇表</el-button>
          </el-form-item>
        </el-form>
      </div>
      <el-tabs v-model="lexiconsActiveName" type="border-card" @tab-click="handleClick">
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
        templateFormVisible: false,
        dialogFormVisible: false,
        suiteData: {},
        url:"http://192.168.71.214:5000/",
        templateForm:{
          template:'',
          templates: [],
          number:'10',
        },
        lexiconForm:{
          key:'',
          lexiconList:'',
        },
        suiteForm:{
          type:'',
          direction:'',
          tolerance:'0.1',
          name:'',
          label:'',
          description:'',
          capability:'',
        },
        data: generateData(),
        value: [],
        count: 0,
        filterMethod(query, item) {
          return item.sentence.indexOf(query) > -1;
        },
        lexicons: generateLexicons(),
        lexiconsActiveName:'0',
        activeNames: ['1'],
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
      addTemplate() {
        this.templateForm.templates.push({
          value: '',
          key: Date.now()
        });
      },
      resetTemplateForm(){

      },
      removeTemplate(item) {
        var index = this.templateForm.templates.indexOf(item)
        if (index !== -1) {
          this.templateForm.templates.splice(index, 1)
        }
      },
      handleClick(tab, event) {
        console.log(tab, event);
      },
      clearTemplates(){
        
        this.templateForm={
          template:'',
          templates:[],
            number:'10',
        }
        this.data=[]
        this.value=[]
        this.count=0
      },
      transferAddTitle(e){
        let dom = e.target;
        if (dom.title) return;
        dom.title = dom.innerText;
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
        }).catch((error)=>{
            console.log(error)
            this.$notify.warning({
              title: '警告',
              message: '输出异常'
            });
          })
      },
      addTestSuite(){
        console.log(this.data)
        console.log(this.value)
        console.log(this.suiteData)
        for (var a in this.suiteData){
          console.log(a,typeof(a))
          console.log(this.suiteData[a])
          console.log(this.suiteData.a)
        }
        //保留data[value],删除data未选中内容
        axios({
          method:'post',
          url:this.url+'addTestSuite',
          data: {'type': this.suiteForm.type,
            'direction': this.suiteForm.direction,
            'tolerance': this.suiteForm.tolerance,
            'name': this.suiteForm.name,
            'labels': this.suiteForm.label,
            'capability': this.suiteForm.capability,
          'description': this.suiteForm.description,
          'sentences': this.data,
            'value': this.value,
            'number': this.templateForm.templates.length+1,
          },
        }).then((response)=>{
          this.$message.success("成功添加测试，可以点击”查看当前测试用例“按钮查看");
          console.log(response.data);
          this.suiteData=response.data;
          this.suiteForm={
            type:'',
            name:'',
            label:'',
            description:'',
            capability:'',
          };
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
        axios({
          method:'post',
          url:this.url+'template',
          data: {'template': this.templateForm.template,
            'templates': this.templateForm.templates,
          'number': this.templateForm.number},
        })
        .then((response)=>{
          console.log(response.data)
          console.log(this.templateForm.templates.length)
          console.log(typeof(response.data[0]))
          if (this.templateForm.templates.length==0) {
            for (var i = this.data.length - 1; i >= 0; i -= 1) {
              var flag = 0;
              for (var j = this.value.length - 1; j >= 0; j -= 1) {
                if (this.value[j] == this.data[i].key) {
                  console.log(this.value[j], ' ', this.data[i].key)
                  flag = 1;
                  break;
                }
              }
              if (flag == 0) {
                console.log('del:', i)
                this.data.splice(i, 1);
              }
            }
            console.log(response.data)
            for (var i in response.data) {
              this.data.push({
                label: this.count.toString()+":"+response.data[i],
                key: this.count,
                sentence: response.data[i],
              })
              this.count += 1
            }
            console.log(this.count)
          }else{
            for (var i = this.data.length - 1; i >= 0; i -= 1) {
              var flag = 0;
              for (var j = this.value.length - 1; j >= 0; j -= 1) {
                if (this.value[j] == this.data[i].key) {
                  console.log(this.value[j], ' ', this.data[i].key)
                  flag = 1;
                  break;
                }
              }
              if (flag == 0) {
                console.log('del:', i)
                this.data.splice(i, 1);
              }
            }
            for (var i in response.data) {
              for (var j=0;j<=this.templateForm.templates.length;j+=1) {
                this.data.push({
                  label: (this.count-j).toString() + ":" + response.data[i][j],
                  key: this.count,
                  sentence: response.data[i][j],
                })
                this.count += 1
              }

            }
          }
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
          data: {'template': this.templateForm.template,
            'number': this.templateForm.number},
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
                label:this.count.toString()+':'+response.data[i],
                key:this.count,
                sentence:response.data[i],
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
      downloadSuite(){
        axios({
          method:'post',
          url:this.url+'downloadSuite',
        })
          .then((response)=>{
            if (response.status === 200) {
              let blob = new Blob([response.data], {
                type: response.headers['content-type']
              });
              const fileName = response.headers['content-disposition'];
              const title = fileName && (fileName.indexOf('filename=') !== -1) ? fileName.split('=')[1] : 'download';
              require('script-loader!file-saver');
              saveAs(blob, title);
            }
          }).catch((error)=>{
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
