# Zinc

![Host-Label](https://img.shields.io/badge/Host-pythonanywhere-blueviolet)

**线上部署： [https://zinc.pythonanywhere.com](https://zinc.pythonanywhere.com)**

这是一个 [django-echarts](https://github.com/kinegratii/django-echarts) 的示例项目，由下列主要python包构建:

```text
django~=3.2
pyecharts~=2.0
django-echarts~=0.6
```

## 功能特性

- 显示 pyecharts 图表
- 选项设置
- 不使用数据库



## 示例图表列表

| 序号 | 图表                               | 说明                                 |
| ---- | ---------------------------------- | ------------------------------------ |
| 1    | 森林覆盖率                         | 柱形图Bar                            |
| 2    | 福建人口总数                       | 折线图Line                           |
| 3    | 历年家庭结构                       | 时刻图Timeline                       |
| 4    | 福建省2021年GDP                    | 地图Map，使用pyecharts地图           |
| 5    | 就业人员构成                       | 扇形图Pie                            |
| 6    | 福建基础数据                       | 表格Table                            |
| 7    | 本站用户最多搜索关键字             | 词云图Wordcloud                      |
| 8    | 福建省2021年分行业固定资产投资情况 | 扇形图，自定义高度                   |
| 9    | 福建省各县市GDP                    | 地图Map，使用自定义geojson地图       |
| 10   | 旅行图                             | 地理坐标图Geo，使用自定义geojson地图 |
| 11   | 网络图示例                         | 网络图Graph                          |
| 12   | 福建省家庭户类型组成               | 参数化图表                           |
| 13   | 飞机座位布局（svg示例）            | 地理坐标图Geo，使用自定义svg底图     |



## 使用方法

安装依赖包

```shell
pip install -r requirements.txt
```

运行开发服务器

```shell
python manage.py runserver
```

