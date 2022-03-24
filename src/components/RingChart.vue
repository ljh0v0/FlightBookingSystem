<template>

  <div ref="ringChart" class="ringChart" :style="{height:height,width:width}"></div>
</template>

<script>
  import echarts from 'echarts'
  export default {
    name: "Ring",
    props: {
        //颜色
        color: {
            type: String,
            default () {
                return 'red'
            }
        },
        //数据
        data: {
            type: Object,
            default () {
                return {}
            }
        },
        width: {
            type: String,
            default: '100%'
        },
        height: {
            type: String,
            default: '250px'
        }
    },
    data () {
        return {
        }
    },
    methods: {
        updateRing(ontime){
            const option = {
                title: [{
                    text: "历史准点率",
                    left: 'center',
                    textStyle:{
                        fontSize: 16,
                        textShadowColor:"#289DE7",
                        textShadowBlur:2,
                        color:"#ffffff"
                    }
                },
                {
                    text: `${parseFloat(ontime).toFixed(2)}%`,
                    left: 'center',
                    top: '45%',
                    textStyle:{
                    fontSize: 18,
                    color:this.color
                    }
                }
                ],
                angleAxis: {
                    max: 100,
                    show: false,
                },
                radiusAxis: {
                    type: 'category',
                    show: true,
                    axisLabel: {
                        show: false,
                    },
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                },
                polar: {
                    radius: '100%',
                    center: ['50%', '50%'],
                },
                series: [{
                    type: 'bar',
                    // 圆角
                    // roundCap: true,
                    barWidth: 20,
                    showBackground: true,
                    backgroundStyle: {
                        color: "rgba(219,219,219,0.3)"
                    },
                    data: [parseFloat(ontime)],
                    coordinateSystem: 'polar',
                    name: `${parseFloat(ontime)}`,
                    label: {
                        show: true,
                    },
                    itemStyle: {
                        normal: {
                            opacity: 1,
                            color: this.color,
                        }
                    },
                }],
            }
            const chartObj = echarts.init(this.$refs.ringChart);
            chartObj.setOption(option)
        }
    }
  }
</script>
<style lang="scss" scoped>
</style>