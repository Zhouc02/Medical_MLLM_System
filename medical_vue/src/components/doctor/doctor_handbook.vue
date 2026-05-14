<!--<template>-->
<!--  <div>-->
<!--    <el-row  style='position: absolute;bottom: 0;right: 0;top: 0;left: 0;'>-->
<!--      <el-col :span='24' style='height: calc(100vh - 75px)'>-->
<!--        <el-col :span='24' style='height: calc((100vh - 75px)*0.7/9);display: flex;align-items: center;justify-content: center;;border-bottom: 1px solid #ccc'>-->
<!--          <p style='font-size: 19px;font-weight: bold;font-family: 微软雅黑,serif'>医学多模态大语言辅助诊断系统操作手册</p>-->
<!--        </el-col>-->
<!--        <el-col :span='24' style='overflow: auto;height: calc((100vh - 75px)*7.3/9);display: flex;align-items: center;justify-content: center'>-->
<!--          辅助诊断：先输入患者姓名和身份证号，然后上传PNG格式的X光图片，即可跳转至辅助诊断页面<br>-->
<!--          在辅助诊断页面，可以放大预览X光图片，后端模型会自动生成病历报告文本，可以对病历报告进行编辑，也可以在右侧进行询诊，辅助诊断。对报告无异议后可上传<br>-->
<!--          历史记录：可以查询患者的过往病史记录，只有已生成病历报告的就诊记录才可以查看详细的病历报告<br>-->
<!--          医师互助：可以向同科室其他医师进行求助<br>-->
<!--          系统反馈：向管理员发送信息，报告系统问题，改进系统功能-->
<!--          -->
<!--        </el-col>-->
<!--      </el-col>-->
<!--    </el-row>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--export default {-->
<!--  data(){-->
<!--    return{-->
<!--    -->
<!--    }-->
<!--  },-->
<!--}-->
<!--</script>-->
<template>
  <div class="manual-container">
    <el-row class="full-height">
      <el-col :span="24" class="header">
        <p class="manual-title">医学多模态大语言辅助诊断系统操作手册</p>
      </el-col>
      <el-col :span="24" class="content" :style="{ height: 'calc((100vh - 75px)*7.3/9)' }">
        <el-col :span='24' style='display: flex;align-items: center;justify-content: center'>
          <div class="instruction">
            <p><span class="highlight">辅助诊断：</span>先输入患者姓名和身份证号，然后上传PNG格式的X光图片，即可跳转至辅助诊断页面。在辅助诊断页面，可以放大预览X光图片，后端模型会自动生成病历报告文本，可以对病历报告进行编辑，也可以在右侧进行询诊，辅助诊断。对报告无异议后可上传。</p>
          </div>
        </el-col>
        <el-col :span='24' style='display: flex;align-items: center;justify-content: center'>
          <div class="instruction">
            <p><span class="highlight">历史记录：</span>可以查询患者的过往病史记录，只有已生成病历报告的就诊记录才可以查看详细的病历报告。</p>
          </div>
        </el-col>
        <el-col :span='24' style='display: flex;align-items: center;justify-content: center'>
          <div class="instruction">
            <p><span class="highlight">医师互助：</span>可以向同科室其他医师进行求助。</p>
          </div>
        </el-col>
        <el-col :span='24' style='display: flex;align-items: center;justify-content: center'>
          <div class="instruction">
            <p><span class="highlight">系统反馈：</span>向管理员发送信息，报告系统问题，改进系统功能。</p>
          </div>
        </el-col>
        
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style scoped>
.manual-container {
  position: absolute;
  bottom: 0;
  right: 0;
  top: 0;
  left: 0;
}

.full-height {
  height: 100%;
}

.header {
  height: calc((100vh - 75px) * 0.7 / 9);
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ccc;
}

.manual-title {
  font-size: 19px;
  font-weight: bold;
  font-family: '微软雅黑', serif;
}

.content {
  overflow: auto;
}

.instruction {
  margin-bottom: 10px;
}

.highlight {
  font-weight: bold;
  color: #007bff; /* You can choose a color that fits your theme */
}
</style>
