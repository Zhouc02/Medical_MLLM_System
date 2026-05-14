<template>
  <div>
    <el-row style='position: absolute;bottom: 0;right: 0;top: 0;left: 0;'>
      <!--左侧输入信息和上传图片区域-->
      <el-col :span='8' style='height: calc((100vh - 75px));border-right: 2px solid #ccc;'>
        <el-col :span='24' style='border-bottom: 1px solid #ccc;display: flex; align-items: center;justify-content: center;height: 80px;font-weight: bold;font-size: 25px;font-family: 微软雅黑,serif'>
          患者信息输入
        </el-col>
        <!-- 输入患者信息 -->
        <el-col :span='24' style='text-align: center;margin-top: 50px'>
          <el-form label-position="top" label-width="80px">
            <el-form-item label="患者姓名">
              <el-input v-model="name" placeholder="请输入患者姓名" style='width: 300px'></el-input>
            </el-form-item>
            <el-form-item label="身份证号">
              <el-input v-model="self_id" placeholder="请输入患者身份证号" style='width: 300px'></el-input>
            </el-form-item>
            <el-form-item label="患者主诉">
              <el-input :rows='6' type='textarea' v-model="complaint" placeholder="请输入患者主诉" style='width: 400px;resize: none;'></el-input>
            </el-form-item>
          </el-form>
        </el-col>
        <!--图片上传区域-->
        <el-col :span='24' style='text-align: center;margin-top: 50px'>
          <el-upload
            class="upload-demo"
            :action='uploadApi'
            :show-file-list="false"
            :before-upload="beforeUpload"
            name='image'
            :data='uploadData'
            :on-success="onUploadSuccess"
          >
            <el-button size="small" type="primary">点击上传图片</el-button>
            <div slot="tip" class="el-upload__tip">只能上传png文件</div>
          </el-upload>
        </el-col>
      </el-col>
      <!--右侧图片预览区域-->
      <el-col :span='16' style='height: calc(100vh - 75px);'>
        <el-col :span='24' style='border-bottom: 1px solid #ccc;display: flex; align-items: center;justify-content: center;height: 80px;font-weight: bold;font-size: 25px;font-family: 微软雅黑,serif'>
          X光图片预览
        </el-col>
        <!--图片预览区域-->
        <el-col :span='24' style='border-bottom: 1px #ccc solid;display: flex;align-items: center;justify-content: center;height:70vh'>
          <img v-if="imageURL" :src="imageURL" alt='预览图片' style='width: 400px;height: auto'>
          <img v-if='!imageURL' src='../../images/doctor/preview_xray.svg' alt='请上传图片' style='height: 30vh;width: 30vh'>
        </el-col>
        <!--跳转按钮-->
        <el-col :span='24' style='height: calc(100vh - 75px - 80px - 70vh);display: flex;align-items: center;justify-content: center;'>
          <el-button v-if='imageURL' type='success' @click='transformToLLM'>转至辅助诊断页面</el-button>
        </el-col>
      </el-col>
    </el-row>
  </div>
</template>

<script>

export default {
  data() {
    return {
      name: '',
      self_id: '',
      imageURL:'',
      complaint:'',
    };
  },
  created() {
    window.sessionStorage.setItem('token', '');
    window.sessionStorage.setItem('patient', '');
    window.sessionStorage.setItem('imageURL', '');
    window.sessionStorage.setItem('self_id', '');
    window.sessionStorage.setItem('complaint', '')
  },
  computed: {
    // 计算属性，拼接上传图片的 API 地址
    uploadApi() {
      return `http://10.1.103.48:8426/hadoop/patient_pic/`;
    },
    uploadData() {
      const formData = new FormData();
      formData.append('name', this.name);
      formData.append('self_id', this.self_id);
      const objectData = {};
      formData.forEach((value, key) => {
        objectData[key] = value;
      });
      return objectData;
    },
  },
  methods: {
    beforeUpload(file) {
      // 验证文件类型，只允许上传 PNG 图片
      if(!this.name||this.self_id.length<18||!this.complaint)
      {
        this.$message.error("请输入正确的患者信息");
        return false;
      }
      const isPNG = file.type === 'image/png';
      if (!isPNG) {
        this.$message.error('只能上传PNG格式的图片!');
      }
      return isPNG;
    },
    onUploadSuccess(response, file, fileList) {
      // 上传成功后，处理后端返回的患者 token 参数
      this.imageURL = URL.createObjectURL(file.raw);
      window.sessionStorage.setItem('imageURL', this.imageURL);
      window.sessionStorage.setItem('token', response.token);
      window.sessionStorage.setItem('patient', this.name);
      window.sessionStorage.setItem('self_id', this.self_id);
      window.sessionStorage.setItem('complaint', this.complaint);
      this.$message.success("上传成功");
    },
    transformToLLM()
    {
      if(window.sessionStorage.getItem('token'))
      {
        this.$message.success('正在跳转至辅助诊断页面');
        this.$router.push('/doctor_LLM');
      }
      else
      {
        this.$message.error('请先上传图片');
      }
    },
  },
};
</script>

<style scoped>

</style>
