<template>
  <div ref="pieChart" :style="{height:height,width:width}"></div>
</template>

<script>
  import echarts from 'echarts'
  export default {
    name: "Ring",
    props: {
        //title
        title: {
            type: String,
            default () {
                return ""
            }
        },
        //数据
        companies: {
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
            default: '250px'
        }
    },

    data () {
        return {
        }
    },
    methods: {
        updatePie(companies){
            const option = {
                title: {
                    text: this.title,
                    left: 'center',
                    textStyle:{
                        fontSize: 16,
                        textShadowColor:"#289DE7",
                        textShadowBlur:2,
                        color:"#ffffff"
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                // legend: {
                //     orient: 'vertical',
                //     left: 10,
                //     data: ['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎']
                // },
                series: [
                    {
                        name: '航司航班占比',
                        type: 'pie',
                        radius: ['50%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '16',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: companies
                    }
                ]
            }
            const chartObj = echarts.init(this.$refs.pieChart);
            chartObj.setOption(option)
        }
    }
  }
</script>
<style lang="scss" scoped>
</style>