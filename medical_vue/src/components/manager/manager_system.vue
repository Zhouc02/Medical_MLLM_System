<template>
  <div>
    <el-row  style='position: absolute;bottom: 0;right: 0;top: 0;left: 0'>
      <!--左侧第一大列-->
      <el-col :span='12' style='height: calc((100vh - 75px));border-right: 2px solid #ccc;'>
        <el-col :span='24' style='height: 30px'>
        <!--第一栏系统运行指示灯-->
        </el-col>
        <el-col :span='24' style='height: 45px;text-align: left;'>
          <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>系统当前状态：
            <span :style="{color:(hdfs_c==1&&mysql_c==1&&redis_c==1)?'green':'red',fontWeight:'bold'}">{{(hdfs_c==1&&mysql_c==1&&redis_c==1)?'运行中':'有异常'}}</span></p>
        </el-col>
        <el-col :span='24' style='height: 60px;text-align: left;'>
          <el-col :span='8' style='height: 100%'>
            <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>HDFS状态：
              <span :style="{color:hdfs_c==1?'green':'red',fontWeight:'bold'}">{{hdfs_c==1?'运行中':'有异常'}}</span></p>
          </el-col>
          <el-col :span='8' style='height: 100%'>
            <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>MySQL状态：
              <span :style="{color:mysql_c==1?'green':'red',fontWeight:'bold'}">{{mysql_c==1?'运行中':'有异常'}}</span></p>
          </el-col>
          <el-col :span='8' style='height: 100%'>
            <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>Redis状态：
              <span :style="{color:redis_c==1?'green':'red',fontWeight:'bold'}">{{redis_c==1?'运行中':'有异常'}}</span></p>
          </el-col>
        </el-col>
        <!--第二栏系统详细占用情况-->
        <hr style='width: 95%;border-top: 1px solid #ccc;'/>
        <el-col :span='24' style='height: 45px;text-align: left;'>
          <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>当前Redis缓存对话列表数量：{{count}} 个</p>
        </el-col>
        <el-col :span='24' style='height: 45px;text-align: left;'>
          <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>当前模型占用GPU分配大小：{{top_allocated}} GB</p>
        </el-col>
        <el-col :span='24' style='height: 45px;text-align: left;'>
          <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>当前模型占用GPU缓存大小：{{top_cached}} GB</p>
        </el-col>
        <el-col :span='24' style='height: 45px;text-align: left;'>
          <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>当前系统占用内存大小：{{top_mem}} GB</p>
        </el-col>
        <el-col :span='24' style='height: 60px;text-align: left;'>
          <p style='margin-left: 50px;font-size: 15px;font-family: 微软雅黑,serif'>当前系统CPU使用率：{{top_cpu}} %</p>
        </el-col>
        <!--第三栏GPU可用空间饼图、GPU使用率饼图、内存可用空间饼图-->
        <hr style='width: 95%;border-top: 1px solid #ccc;'/>
        <el-col :span='24' style='height: 200px;text-align: left;'>
          <el-col :span='8' style='height: 100%;'>
            <div ref='gpu_mem_chart' style='height: 100%;width: 100%;'></div>
          </el-col>
          <el-col :span='8' style='height: 100%'>
            <div ref='gpu_used_chart' style='height: 100%;width: 100%;'></div>
          </el-col>
          <el-col :span='8' style='height: 100%'>
            <div ref='mem_used_chart' style='height: 100%;width: 100%;'></div>
          </el-col>
        </el-col>
        <!--第四栏功能按钮-->
        <hr style='width: 95%;border-top: 1px solid #ccc;'/>
        <el-col :span='24' style='height: 70px;'>
          <el-col :span='4' style='height: 100%;display: flex;justify-content: center;align-items:center;'>
            <el-button type='success' @click='clear_cached' style='height: 55px;width: 100px;text-align: center;font-size: 14px;padding: 0;font-family: 微软雅黑,serif'>清除GPU缓存</el-button>
          </el-col>
          <el-col :span='20' v-if=!is_clear_cached style='height: 100%;text-align: left;line-height: 70px;font-family: 微软雅黑,serif'>
            当前尚未清理GPU缓存
          </el-col>
          <el-col :span='20' v-if=is_clear_cached style='height: 100%;text-align: left;line-height: 70px;font-family: 微软雅黑,serif;color: green'>
            已清理GPU缓存 {{cached_gb}} GB，GPU分配 {{allocated_gb}} GB
          </el-col>
        </el-col>
        <el-col :span='24' style='height: 70px;z-index: 1'>
          <el-col :span='4' style='height: 100%;display: flex;justify-content: center;align-items:center;'>
            <el-button type='warning' @click='clear_redis' style='height: 55px;width: 100px;text-align: center;font-size: 14px;padding: 0;font-family: 微软雅黑,serif'>清除Redis缓存</el-button>
          </el-col>
          <el-col :span='20' v-if=!is_clear_redis style='height: 100%;text-align: left;line-height: 70px;font-family: 微软雅黑,serif;color: red'>
            *清除Redis缓存将清除所有未生成病历报告的模型对话的历史记录
          </el-col>
          <el-col :span='20' v-if=is_clear_redis style='height: 100%;text-align: left;line-height: 70px;font-family: 微软雅黑,serif;color: green'>
            已清理Redis缓存对话数 {{redis_count}} 个
          </el-col>
        </el-col>
        <el-col :span='24' style='height: 70px;z-index: 9999'>
          <el-col :span='4' style='height: 100%;display: flex;justify-content: center;align-items:center;'>
            <el-select v-model="selectedInterval" placeholder="选择间隔" style='width: 100px;'>
              <el-option label="每5秒" value="5"></el-option>
              <el-option label="每3秒" value="3"></el-option>
              <el-option label="每2秒" value="2"></el-option>
              <el-option label="每1秒" value="1"></el-option>
              <el-option label="每0.5秒" value="0.5"></el-option>
            </el-select>
          </el-col>
          <el-col :span='20' style='height: 100%;text-align: left;line-height: 70px;font-family: 微软雅黑,serif;'>
            调整实时监控时间间隔
          </el-col>
        </el-col>
      </el-col>
      
      <!--右侧第二大列-->
      <el-col :span='12' style='height: calc((100vh - 75px));'>
        <!--第一块图表-->
        <el-col :span='24' style='height: calc((100vh - 75px)/4);'>
          <div ref="chart_allocated" style="width: 100%;height: 100%"></div>
        </el-col>
        <!--第二块图表-->
        <el-col :span='24' style='height: calc((100vh - 75px)/4);'>
          <div ref="chart_cached" style="width: 100%;height: 100%"></div>
        </el-col>
        <!--第三块图表-->
        <el-col :span='24' style='height: calc((100vh - 75px)/4);'>
          <div ref="chart_mem" style="width: 100%;height: 100%"></div>
        </el-col>
        <!--第四块图表-->
        <el-col :span='24' style='height: calc((100vh - 75px)/4);'>
          <div ref='chart_cpu' style="width: 100%;height: 100%"></div>
        </el-col>
      </el-col>
    </el-row>
    
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data(){
    return{
      redis_c:1,
      mysql_c:1,
      hdfs_c:1,
      selectedInterval:'每1秒',
      intervalSecond:1,
      cached_gb:0,
      allocated_gb:0,
      redis_count:0,
      is_clear_cached: false,
      is_clear_redis: false,
      continueUpdateData: true,
      allocated: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      top_allocated: 0,
      cached: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      top_cached: 0,
      mem: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      top_mem: 0,
      cpu: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      top_cpu: 0,
      count: 0,
      date: [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
      timer: null,
      gpu_total:0,
      gpu_free:0,
      gpu_used:0,
      total_mem:0,
      avail_mem:0,
      allocated_option: {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: 'GPU分配占用', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: 'GB', max:"30", min:"0"},
        series:[{name: 'GPU分配占用', type: 'line', data: this.allocated}]
      },
      cached_option: {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: 'GPU缓存占用', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: 'GB', max:"80", min:"0"},
        series:[{name: 'GPU缓存占用', type: 'line', data: this.cached}]
      },
      mem_option:{
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: '内存占用', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: 'GB', max:"30", min:"0"},
        series:[{name: '内存占用', type: 'line', data: this.mem}]
      },
      cpu_option:{
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: 'CPU使用率', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: '%', max:"100", min:"0"},
        series:[{name: 'CPU使用率', type: 'line', data: this.cpu}]
      },
      gpu_mem_option:{
        title: {text: 'GPU显存使用情况(MB)',left: 'center',top: 'top',textStyle: {color: '#333',fontSize: 16}, },
        tooltip: {trigger: 'item'},
        series: [{ name: 'GPU显存使用情况(MB)', type: 'pie', radius: '55%', center: ['50%', '50%'], data: [
              { value: this.gpu_free, name: '可用空间' },
              { value: this.gpu_total - this.gpu_free, name: '已用空间' },
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)', }, },},],
      },
      gpu_used_option:{
        title: {text: 'GPU使用率(%)',left: 'center',top: 'top',textStyle: {color: '#333',fontSize: 16}, },
        tooltip: {trigger: 'item'},
        series: [{ name: 'GPU使用率(%)', type: 'pie', radius: '55%', center: ['50%', '50%'], data: [
            { value: this.gpu_used, name: '已使用' },
            { value: 100 - this.gpu_used, name: '空余算力' },
          ],
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)', }, },},],
      },
      mem_used_option:{
        title: {text: '内存使用情况(GB)',left: 'center',top: 'top',textStyle: {color: '#333',fontSize: 16}, },
        tooltip: {trigger: 'item'},
        series: [{ name: '内存使用情况(GB)', type: 'pie', radius: '55%', center: ['50%', '50%'], data: [
            { value: this.avail_mem, name: '可用空间' },
            { value: this.total_mem - this.avail_mem, name: '已用空间' },
          ],
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)', }, },},],
      },
    }
  },
  watch:{
    selectedInterval(second){
      this.intervalSecond = second;
    },
  },
  methods:{
    clear_redis(){
      axios.post('http://10.1.103.48:8426/hadoop/redis_clear/').then(res=>{
        this.redis_count = res.data.count;
      });
      this.is_clear_redis = true;
    },
    clear_cached(){
      axios.post('http://10.1.103.48:8426/model/cached_clear/').then(res=>{
        this.cached_gb = res.data.clear_cached.toFixed(3);
        this.allocated_gb = res.data.clear_alloc;
      });
      this.is_clear_cached = true;
    },
    fetchData(){
      if (!this.continueUpdateData) return;
      axios.post('http://10.1.103.48:8426/model/system_monitor/').then(res=>{
        const new_allocated = res.data.allocated;
        this.top_allocated = new_allocated.toFixed(3);
        const new_cached = res.data.cached;
        this.top_cached = new_cached.toFixed(3)
        const new_mem = res.data.mem;
        this.top_mem = new_mem.toFixed(3);
        const new_cpu = res.data.cpu;
        this.top_cpu = new_cpu;
        const new_count = res.data.count;
        this.allocated.push(new_allocated);
        this.cached.push(new_cached);
        this.mem.push(new_mem);
        this.cpu.push(new_cpu);
        this.count = new_count;
        this.date.push(this.getCurrentTime())
        this.gpu_used=res.data.gpu_used;
        this.gpu_total=res.data.gpu_total;
        this.gpu_free=res.data.gpu_free;
        this.avail_mem=res.data.avail_mem;
        this.total_mem=res.data.total_mem;
        this.redic_c=res.data.redic_c;
        this.hdfs_c=res.data.hdfs_c;
        this.mysql_c=res.data.mysql_c;
        if (this.allocated.length>25)
        {
          this.allocated.shift();
          this.cached.shift();
          this.mem.shift();
          this.cpu.shift();
          this.date.shift();
        }
      }).finally(()=>{
        setTimeout(()=>{
          this.updateChart();
          this.fetchData();
        }, this.intervalSecond*1000);
      })
    },
    updateChart(){
      if(!this.continueUpdateData) return;
      this.chart_allocated.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: 'GPU分配占用', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: 'GB', max:Math.floor(Math.max(...this.allocated))+10, min:"0"},
        series:[{name: 'GPU分配占用', type: 'line', data: this.allocated}]
      });
      this.chart_cached.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: 'GPU缓存占用', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: 'GB', max:Math.floor(Math.max(...this.cached))+20, min:"0"},
        series:[{name: 'GPU缓存占用', type: 'line', data: this.cached}]
      });
      this.chart_mem.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: '内存占用', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: 'GB', max:Math.floor(Math.max(...this.mem))+10, min:"0"},
        series:[{name: '内存占用', type: 'line', data: this.mem}]
      });
      this.chart_cpu.setOption({
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        title:{text: 'CPU使用率', left: 'center'},
        grid:{left: '5%', right: '5%', bottom: '11%', top: '15%',},
        xAxis:{type: 'category', name: '时间', data: this.date},
        yAxis:{type: 'value', name: '%', max:Math.floor(Math.max(...this.cpu))+10, min:"0"},
        series:[{name: 'CPU使用率', type: 'line', data: this.cpu}]
      });
      this.gpu_mem_chart.setOption({
        title: {text: 'GPU显存使用情况(MB)',left: 'center',top: 'top',textStyle: {color: '#333',fontSize: 16}, },
        tooltip: {trigger: 'item'},
        series: [{ name: 'GPU显存使用情况(MB)', type: 'pie', radius: '55%', center: ['50%', '50%'], data: [
            { value: this.gpu_free, name: '可用空间' },
            { value: this.gpu_total - this.gpu_free, name: '已用空间' },
          ],
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)', }, },},],
      });
      this.gpu_used_chart.setOption({
        title: {text: 'GPU使用率(%)',left: 'center',top: 'top',textStyle: {color: '#333',fontSize: 16}, },
        tooltip: {trigger: 'item'},
        series: [{ name: 'GPU使用率(%)', type: 'pie', radius: '55%', center: ['50%', '50%'], data: [
            { value: this.gpu_used, name: '已使用' },
            { value: 100 - this.gpu_used, name: '空余算力' },
          ],
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)', }, },},],
      });
      this.mem_used_chart.setOption({
        title: {text: '内存使用情况(GB)',left: 'center',top: 'top',textStyle: {color: '#333',fontSize: 16}, },
        tooltip: {trigger: 'item'},
        series: [{ name: '内存使用情况(GB)', type: 'pie', radius: '55%', center: ['50%', '50%'], data: [
            { value: this.avail_mem, name: '可用空间' },
            { value: this.total_mem - this.avail_mem, name: '已用空间' },
          ],
          itemStyle: {
            emphasis: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)', }, },},],
      });
    },
    initChart(){
      this.chart_allocated = this.$echarts.init(this.$refs.chart_allocated);
      this.chart_allocated.setOption(this.allocated_option);
      this.chart_cached = this.$echarts.init(this.$refs.chart_cached);
      this.chart_cached.setOption(this.cached_option);
      this.chart_mem = this.$echarts.init(this.$refs.chart_mem);
      this.chart_mem.setOption(this.mem_option);
      this.chart_cpu = this.$echarts.init(this.$refs.chart_cpu);
      this.chart_cpu.setOption(this.cpu_option);
      this.gpu_mem_chart = this.$echarts.init(this.$refs.gpu_mem_chart);
      this.gpu_mem_chart.setOption(this.gpu_mem_option);
      this.gpu_used_chart = this.$echarts.init(this.$refs.gpu_used_chart);
      this.gpu_used_chart.setOption(this.gpu_used_option);
      this.mem_used_chart = this.$echarts.init(this.$refs.mem_used_chart);
      this.mem_used_chart.setOption(this.mem_used_option);
    },
    getCurrentTime() {
      const now = new Date();
      const hours = now.getHours().toString().padStart(2, '0');
      const minutes = now.getMinutes().toString().padStart(2, '0');
      const seconds = now.getSeconds().toString().padStart(2, '0');
      return `${hours}:${minutes}:${seconds}`;
    },
  },
  mounted(){
    setTimeout(() => {
      this.initChart();
      this.fetchData();
    }, 300);
  },
  beforeRouteLeave(to, from, next) {
    this.continueUpdateData=false;
    clearInterval(this.timer);
    next();
  },
  beforeDestroy() {
    this.continueUpdateData=false;
    clearTimeout(this.timer);
  }
}
</script>

<style>

</style>