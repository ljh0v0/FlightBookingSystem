<template>
  <div ref="myGraph" :style="{height:height,width:width}"></div>
</template>

<script>
  import echarts from 'echarts'
  export default {
    name: "Graph",
    props: {
        //节点数据
        nodes: {
            type: Array,
            default () {
            return []
            }
        },
        //节点关系
        links: {
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
            default: '380px'
        }
    },
    data () {
      return {
         color: ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3']
      }
    },
    methods: {
        updateGraph(){
            const option = {
            title: {
                text: '航班工作人员',
                left: 'center',
                textStyle: {
                    fontSize: 16
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: function (params) {
                    return params.data.info == null ? '':
                        params.data.is_flight ?  `<div><span style="margin-right:5px;display:inline-block;width:10px;height:10px;border-radius:5px;background-color:${params.color};"></span>航班号：${params.data.info}</div>`
                        : `<div><span style="margin-right:5px;display:inline-block;width:10px;height:10px;border-radius:5px;background-color:${params.color};"></span>工作人员信息 </br> 职务：${params.data.info.job}
                                </br> 入职时间：${params.data.info.employ_time} </br> 工作时间：${params.data.info.work_time}</div>`; 
                }
            },
            animationDurationUpdate: 1500,
            animationEasingUpdate: 'quinticInOut',
            series : [
                {
                    name: 'node',
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 50,
                    data: this.nodes,
                    links: this.links,
                    roam: true,
                    draggable: true,
                    focusNodeAdjacency: true,
                    label: {
                        show: true
                    },
                    itemStyle: {
                        normal: {
                            color: function (params) {
                                var color=['#c23531','#2f4554', '#61a0a8','#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3']
                                return color[(params.dataIndex)%(color.length)]
                            },
                        },
                    },
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 10],
                    edgeLabel: {
                        fontSize: 14,
                        normal:{
                        show:true,
                        formatter:function(params){
                            return params.data.relation?params.data.relation:''
                        }
                        }
                    },
                    force: {
                        repulsion : 120,//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                        gravity : 0.02,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                        edgeLength :120,//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
                        layoutAnimation : true
                    },
                    lineStyle: {
                        color: 'target',
                        opacity: 0.9,
                        width: 1,
                        curveness: 0.2
                    },
                    emphasis: {
                        lineStyle: {
                            width: 3
                        }
                    }
                }
            ]
        };
            const chartObj = echarts.init(this.$refs.myGraph);
            chartObj.setOption(option)
        }
    }
  }
</script>