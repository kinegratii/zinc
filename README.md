# Zinc

![Host-Label](https://img.shields.io/badge/Host-pythonanywhere-blueviolet)

**线上部署： [https://zinc.pythonanywhere.com](https://zinc.pythonanywhere.com)**

这是一个 [django-echarts](https://github.com/kinegratii/django-echarts) 的示例项目，由下列主要python包构建:

```text
django~=3.2
pyecharts~=1.9
django-echarts~=0.5
```

## 功能特性

- 显示 pyecharts 图表（包括柱形图、折线图、时序图、地图和表格等）
- 选项设置
- 自定义geojson文件
- 不包含数据库

## 使用方法

安装依赖包

```shell
pip install -r requirements.txt
```

运行开发服务器

```shell
python manage.py runserver
```

