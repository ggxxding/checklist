<template>
  <div>
  <boldHeader></boldHeader>
    <el-drawer
      title="测试用例清单"
      :visible.sync="drawer"
    size="50%">
      <el-button type='primary' @click="downloadSuite"  style="margin-left:4%;margin-right:1%">导出并下载</el-button>
      <el-button type='primary' @click="uploadSuiteVisible=true"  >上传测试用例</el-button>
      <el-button type='primary' @click="uploadPredVisible=true"  >上传模型预测</el-button>
      <el-collapse v-model="activeNames" style="margin-left:4%;margin-right:4%">
        <el-collapse-item  v-for="(suite,index) in suiteData" :key="index" :title="suite.name" :name="index">
          <el-row>
            <el-col :span="19"><div>类型:{{suite.type}}</div></el-col>
            <el-col :span="4">
              <el-button  type="primary" size="small" style="float:right" @click="loadSentences(suite.name)">载入</el-button>
              <el-button  type="primary" size="small" style="float:right" @click="deleteSuite(suite.name)">删除</el-button>
            </el-col>
          </el-row>
          <el-row>
          <div>功能:{{suite.capability}}</div>
          </el-row>
          <el-row>
          <div>描述:{{suite.description}}</div>
          </el-row>
          <el-row>
          <div>标签:{{suite.labels}}</div>
          </el-row>
          <el-row>
          <div>数据:{{suite.data}}</div>
          </el-row>
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

        <el-form :inline="true"  v-show="suiteForm.type=='INV'" class="demo-form-inline">
          <el-form-item label="扰乱方式">
            <el-select v-model="suiteForm.perturbType" placeholder="请选择">
              <el-option label="增加乱码" value="addRandomStr"></el-option>
              <el-option label="句末标点（用例请以中文句号或问号结尾）" value="punctuation"></el-option>
              <el-option label="生成同音字" value="homophone"></el-option>
              <el-option label="替换地名" value="change_location"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="同音字数量" v-show="suiteForm.perturbType=='homophone'">
            <el-input v-model="suiteForm.homoNum"></el-input>
          </el-form-item>
          <el-form-item label="用例数量" v-show="suiteForm.perturbType=='homophone'">
            <el-input v-model="suiteForm.generateNum"></el-input>
          </el-form-item>
        </el-form>



        <el-form-item v-show="suiteForm.perturbType== 'addRandomStr'" label="增加数量" >
          <el-input v-model="suiteForm.addRandomStrNumber" ></el-input>
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
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-dialog title="上传测试用例" :visible.sync="uploadSuiteVisible">
      <el-upload class="upload" drag action="/uploadSuite" multiple ref="upload"
                 list-type="file"
                 :show-file-list="false"
                 :http-request="uploadSuite"
      style="text-align:center">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">推荐以上传文件形式上传，将.pkl格式的套件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip"></div>
      </el-upload>

    </el-dialog>
    <el-dialog title="上传模型预测" :visible.sync="uploadPredVisible">
      <el-upload class="upload" drag action="/uploadPred" multiple ref="upload"
                 list-type="file"
                 :show-file-list="false"
                 :http-request="uploadPred"
                 style="text-align:center">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">推荐以上传文件形式上传，将模型预测结果拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip"></div>
      </el-upload>
      <div style="white-space: pre-line">{{summary}}</div>

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
        @change="transferChange"
        @mouseover.native="transferAddTitle">
          <el-button class="transfer-footer" slot="left-footer" size="middle" @click="templateFormVisible = true">增加数据</el-button>
          <el-button class="transfer-footer" slot="right-footer" size="middle" @click="clearTemplates">清空数据</el-button>
          <el-button class="transfer-footer" slot="right-footer" size="middle" @click="addToLexicon">加入词汇表</el-button>
      </el-transfer>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-form :inline="true"  class="demo-form-inline" style="float:right">
        <el-form-item>
          <el-button type="primary" @click="dialogFormVisible = true" >增加测试用例</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="drawer = true" >管理测试用例</el-button>
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
            <el-input type="textarea" :autosize="{ minRows: 1, maxRows: 8}" v-model="lexiconForm.lexiconList" placeholder='例:北京 上海(空格分隔)'></el-input>
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
  import boldHeader from './boldHeader';
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
        uploadSuiteVisible:false,
        uploadPredVisible:false,
        summary:'',
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
          perturbType:'',
          addRandomStrNumber: '5',
          tolerance:'0.1',
          name:'',
          label:'',
          description:'',
          capability:'',
          homoNum:1,
          generateNum:3,
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
        if(this.data.length>0){
          this.$notify.warning({
            title: '警告',
            message: '请清空待选用例后再改变模板数量'
          });
        }else{
          this.templateForm.templates.push({
            value: '',
            key: Date.now()
          });
        }
      },
      resetTemplateForm(){

      },
      removeTemplate(item) {
        if(this.data.length>0){
          this.$notify.warning({
            title: '警告',
            message: '请清空待选用例后再改变模板数量'
          });
        }else{
          var index = this.templateForm.templates.indexOf(item)
          if (index !== -1) {
            this.templateForm.templates.splice(index, 1)
          }
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
      addToLexicon(){
        if(this.value.length==0){
          this.$notify.warning({
            title: '警告',
            message: '测试用例为空，添加失败。'
          });
        }else {
          var words = [];
          for (var i in this.value) {
            for (var j in this.data) {
              if (this.data[j].key == this.value[i]) {
                words.push(this.data[j].sentence);
              }
            }
          }
          console.log(words);
          this.lexiconForm.lexiconList = words.join(' ')
          this.$message.success("加入成功,请查看下方词汇表内容");
        }
      },
      transferChange(value, direction, movedKeys){
        console.log(value, direction, movedKeys);
        if (direction=='right'){
          for(var i in movedKeys){
            for(var j in this.data){
              if(this.data[j].key==movedKeys[i]){
                console.log('equal')
                for(var k=1; k<=this.templateForm.templates.length; k++){
                  if(this.data[Number(j)+k]!=undefined && this.data[Number(j)+k].label.split(':',2)[0]==this.data[j].label.split(':',2)[0]){
                    if(!this.value.includes(Number(movedKeys[i])+k)) {
                      this.value.push(Number(movedKeys[i]) + k)
                    }
                    console.log(this.value)
                  }
                  if(this.data[Number(j)-k]!=undefined && this.data[Number(j)-k].label.split(':',2)[0]==this.data[j].label.split(':',2)[0]){
                    if(!this.value.includes(Number(movedKeys[i])-k)) {
                      this.value.push(Number(movedKeys[i]) - k)
                    }
                    console.log(this.value)
                  }
                }
              }
            }
          }
        }else{
          console.log('left')
          for(var i in movedKeys){//遍历movedKey
            for(var j in this.data){
              if(this.data[j].key==movedKeys[i]){//data中找到和movedKey对应的data[j]
                for(var k=1; k<=this.templateForm.templates.length; k++){
                  if(this.data[Number(j)+k]!=undefined && this.data[Number(j)+k].label.split(':',2)[0]==this.data[j].label.split(':',2)[0]){
                    for(var l in this.value){
                      if(this.value[l]==this.data[Number(j)+k].key){
                        this.value.splice(l,1)
                        break
                      }
                    }
                  }
                  if(this.data[Number(j)-k]!=undefined && this.data[Number(j)-k].label.split(':',2)[0]==this.data[j].label.split(':',2)[0]){
                    for(var l in this.value){
                      if(this.value[l]==this.data[Number(j)-k].key){
                        this.value.splice(l,1)
                        break
                      }
                    }
                  }
                }
              }
            }
          }

        }
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
            'perturbType': this.suiteForm.perturbType,
            'addRandomStrNumber': this.suiteForm.addRandomStrNumber,
            'labels': this.suiteForm.label,
            'capability': this.suiteForm.capability,
          'description': this.suiteForm.description,
          'sentences': this.data,
            'value': this.value,
            'number': this.templateForm.templates.length+1,
            'homoNum': this.suiteForm.homoNum,
            'generateNum': this.suiteForm.generateNum,
          },
        }).then((response)=>{
          this.$message.success("成功添加测试，可以点击”查看当前测试用例“按钮查看");
          console.log(response.data);
          this.suiteData=response.data;
          this.suiteForm={
            type:'',
              direction:'',
            perturbType: '',
              addRandomStrNumber: '5',
              tolerance:'0.1',
              name:'',
              label:'',
              description:'',
              capability:'',
            homoNum:1,
            generateNum:3,
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
          responseType:'blob',
          headers:{'Content-Type':'application/json;application/octet-stream'},
        })
          .then((response)=>{
            console.log(response);
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
      uploadSuite(param){
        let fileObj = param.file; // 相当于input里取得的files
        let data = new FormData(); // FormData 对象
        let extension = fileObj.name.substring(fileObj.name.lastIndexOf('.') + 1)
        let size = fileObj.size / 1024 / 1024
        if (extension !== 'pkl') {
          this.$notify.warning({
            title: '警告',
            message: `只能上传后缀是.pkl的文件`
          });
        } else if(size > 200) {
          this.$notify.warning({
            title: '警告',
            message: `文件大小不得超过10M`
          });
        } else {
          data.append("file", fileObj); // 文件对象
          //data.append("name", this.regeditForm.name);
          //data.append("description", this.regeditForm.description);
          axios({
            method: 'POST',
            url: this.url+'uploadSuite',
            data: data,
            headers: {'Content-Type': 'multipart/form-data'}
          }).then(response => {
            this.$message.success("文件上传成功");
            this.suiteData=response.data;
            this.suiteForm={
              type:'',
                direction:'',
              perturbType: '',
                addRandomStrNumber: '5',
                tolerance:'0.1',
                name:'',
                label:'',
                description:'',
                capability:'',
              homoNum:1,
              generateNum:3,
            };
          }).catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
        }
      },
      uploadPred(param){

        let fileObj = param.file; // 相当于input里取得的files
        let data = new FormData(); // FormData 对象
        let extension = fileObj.name.substring(fileObj.name.lastIndexOf('.') + 1)
        let size = fileObj.size / 1024 / 1024
        if(size > 20) {
          this.$notify.warning({
            title: '警告',
            message: `文件大小不得超过10M`
          });
        } else {
          data.append("file", fileObj); // 文件对象
          //data.append("name", this.regeditForm.name);
          //data.append("description", this.regeditForm.description);
          axios({
            method: 'POST',
            url: this.url+'uploadPred',
            data: data,
            headers: {'Content-Type': 'multipart/form-data'}
          }).then(response => {
            this.$message.success("文件上传成功");
            console.log(response.data);
            this.summary=response.data;

          }).catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
        }
      },
      loadSentences(suiteName){
        console.log(suiteName)
        console.log(this.suiteData[suiteName])
        this.clearTemplates()
        if(this.suiteData[suiteName].isPair == '0'){
          for (var i in this.suiteData[suiteName].data) {
            this.data.push({
              label: this.count.toString()+":"+this.suiteData[suiteName].data[i],
              key: this.count,
              sentence: this.suiteData[suiteName].data[i],
            })
            this.count += 1
          }
        }else{
          for (var i in this.suiteData[suiteName].data) {
            console.log(this.suiteData[suiteName].data[i])
            for (var j=0;j<this.suiteData[suiteName].data[i].length;j+=1) {

              this.data.push({
                label: (this.count-j).toString() + ":" + this.suiteData[suiteName].data[i][j],
                key: this.count,
                sentence: this.suiteData[suiteName].data[i][j],
              })
              this.count += 1
            }

          }
        }
      },
      deleteSuite(suiteName){
        console.log(suiteName)
        console.log(this.suiteData[suiteName])
        axios({
          method: 'POST',
          url: this.url+'deleteSuite',
          data: {'suiteName': suiteName},
        }).then(response => {
          this.$message.success("删除成功");
          this.suiteData=response.data;
          this.suiteForm={
            type:'',
              direction:'',
            perturbType: '',
              addRandomStrNumber: '5',
              tolerance:'0.1',
              name:'',
              label:'',
              description:'',
              capability:'',
            homoNum:1,
            generateNum:3,
          };

        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      },
    },
    components:{
      boldHeader,

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
