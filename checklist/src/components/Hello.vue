<template>
  <div>
    <el-upload class="upload" drag action="/test" multiple ref="upload" style="text-align:center"
               list-type="file"
               :show-file-list="false"
               :http-request="httpRequest">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将待检测图片拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">上传成功后点击下面的检测按钮：</div>
    </el-upload>

    <el-row>
      <el-col :span="8"><div class="grid-content bg-purple"> </div></el-col>
      <el-col :span="16">
        <div class="grid-content bg-purple-light">
        <el-transfer
        filterable
        :filter-method="filterMethod"
        filter-placeholder="请输入城市拼音"
        v-model="value"
        :data="data">
      </el-transfer>
        </div>
      </el-col>
    </el-row>
  </div>


</template>

<script >
  import axios from 'axios';
  export default {
    name: 'Hello',
    data() {
      const generateData = _ => {
        const data = [];
        const cities = ['上海', '北京', '广州', '深圳', '南京', '西安', '成都'];
        const pinyin = ['shanghai', 'beijing', 'guangzhou', 'shenzhen', 'nanjing', 'xian', 'chengdu'];
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
        data: generateData(),
        value: [],
        filterMethod(query, item) {
          return item.pinyin.indexOf(query) > -1;
        }
      };
    },
    methods: {
      httpRequest(param) {
        console.log(param);
        let fileObj = param.file; // 相当于input里取得的files
        let data = new FormData(); // FormData 对象
        let extension = fileObj.name.substring(fileObj.name.lastIndexOf('.') + 1)
        let size = fileObj.size / 1024 / 1024

          data.append("file", fileObj); // 文件对象
          //data.append("name", this.regeditForm.name);
          //data.append("description", this.regeditForm.description);
          axios({
            method: 'POST',
            url: this.url,
            data: data,
            headers: {'Content-Type': 'multipart/form-data'}
          }).then(res => {
              this.$message.success("文件上传成功");
              this.picurl=res.data;
              console.log(this.acc_text)
              console.log(res);
            }).catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });

      },
    },
    components:{

    }
  }

</script>
<style>

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
  .bg-purple-light {
    background: #e5e9f2;
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
