<template>
  <div :id="id" :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
export default {
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    id: {
      type: String,
      default: 'chart'
    },
    data: {
        type: Array,
        default () {
            return []
        }
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '400px'
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart(flight_flow) {
      this.chart = echarts.init(document.getElementById(this.id))
      const xData = (function() {
        const data = []
        for (let i = 0; i < 24; i++) {
          data.push(i)
        }
        return data
      }())
      this.chart.setOption({
        title: {
            text: '今日航班流量变化',
            x: '20',
            top: '20',
            textStyle:{
                fontSize: 20,
                textShadowColor:"#289DE7",
                textShadowBlur:2,
                color:"#ffffff"
            },
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            textStyle: {
              color: '#fff'
            }
          }
        },
        grid: {
          left: '10%',
          right: '5%',
          borderWidth: 0,
          top: 70,
          bottom: 95,
          textStyle: {
            color: '#fff'
          }
        },
        calculable: true,
        xAxis: [{
          type: 'category',
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          splitLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          splitArea: {
            show: false
          },
          axisLabel: {
            interval: 0
          },
          data: xData
        }],
        yAxis: [{
          type: 'value',
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            interval: 0
          },
          splitArea: {
            show: false
          }
        }],
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [
            0
          ],
          bottom: 30,
          start: 10,
          end: 80,
          handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
          handleSize: '110%',
          handleStyle: {
            color: '#d3dee5'
          },
          textStyle: {
            color: '#fff' },
          borderColor: '#90979c'
        }, {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 35
        }],
        series: [
        {
          name: '航班量',
          type: 'bar',
          itemStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(
                    0, 0, 0, 1,       //4个参数用于配置渐变色的起止位置, 这4个参数依次对应右/下/左/上四个方位. 而0 0 0 1则代表渐变色从正上方开始
                    [
                        {offset: 0, color: 'rgba(252,230,48,1)'},
                        {offset: 1, color: 'rgba(0,191,183,1)'}
                    ]
                ),
            //   color: 'rgba(0,191,183,1)',
              barBorderRadius: 0,
            //   label: {
            //     show: true,
            //     position: 'top',
            //     formatter(p) {
            //       return p.value > 0 ? p.value : ''
            //     }
            //   }
            }
          },
          data: flight_flow
        }, {
          name: '航班量',
          type: 'line',
          symbolSize: 10,
          symbol: 'circle',
          itemStyle: {
            normal: {
              color: '#FF9800',
              barBorderRadius: 0,
              label: {
                show: true,
                position: 'top',
                formatter(p) {
                  return p.value > 0 ? p.value : ''
                }
              }
            }
          },
          data: flight_flow
        }
        ]
      })
    }
  }
}
</script>