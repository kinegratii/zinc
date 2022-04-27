import os
from borax.datasets.fetch import fetch
from django.conf import settings
from django_echarts.datatools.helpers import ceil_n
from django_echarts.entities import (
    Copyright, ValuesPanel, ValueItem, NamedCharts, WidgetCollection,
    bootstrap_table_class, LinkItem, RowContainer, Jumbotron
)
from django_echarts.geojson import use_geojson, geojson_url
from django_echarts.starter import DJESite, SiteOpts, DJESiteBackendView
from django_echarts.stores.entity_factory import factory
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Map, Pie, WordCloud, Line, Geo
from pyecharts.components import Table
from pyecharts.globals import ThemeType, ChartType, SymbolType

from ccs.fake_data import FJ_DATA, FJ_DATA_FIELDS, FJ_GDP2021_DATA, FJ_SX_GDP_DATA, fake_long_text

__all__ = ['site_obj']

site_obj = DJESite(
    site_title='福建统计',
    opts=SiteOpts(list_layout='list', nav_shown_pages=['home', 'list', 'settings'], nav_top_fixed=False)
)

site_obj.add_widgets(
    copyright_=Copyright(start_year=2022, powered_by='Zinc'),
    jumbotron=Jumbotron('福建统计', main_text='数据来源：福建统计局', small_text='2022年2月'),
    # values_panel='home1_panel',
    # jumbotron_chart='search_word_cloud'
)

site_obj.add_footer_link(
    LinkItem(text='福建统计年鉴2021', url='https://tjj.fujian.gov.cn/tongjinianjian/dz2021/index.htm', new_page=True)

).add_footer_link(
    LinkItem(text='网站源码', url='https://github.com/kinegratii/zinc', new_page=True)
).add_left_link(LinkItem(text='控制板', url='/dashboard/'))


# add_footer_link(
#     LinkItem(text='2021年福建省国民经济和社会发展统计公报', url='https://tjj.fj.gov.cn/xxgk/tjgb/202203/t20220308_5854870.htm',
#              new_page=True)

@site_obj.register_chart(title='森林覆盖率',
                         description='截止2020年底，福建省土地面积1240.29万公顷，占我国国土总面积1.3%。全省森林面积811.58万公顷，森林覆盖率为66.8%，连续42年位居全国首位。',
                         catalog='基本信息', top=1)
def fujian_forest_coverage():
    cities, coverages = fetch(FJ_DATA, 0, 8, getter=lambda item, key: item[key])
    bar = Bar().add_xaxis(
        cities).add_yaxis(
        '森林覆盖率', coverages
    ).set_global_opts(
        title_opts=opts.TitleOpts(title="福建省各地市森林覆盖率", subtitle="单位：%"),
        visualmap_opts=opts.VisualMapOpts(is_show=True, max_=100, min_=0)).set_series_opts(
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(y=66.8, name="全省"),
            ]
        )
    )
    return bar


@site_obj.register_chart(title='福建人口总数', catalog='人口与就业', description='本图描述了自1953年以来历次人口普查的数据。', tags=['历年'])
def fj_total_population():
    years = ['1953年', '1964年', '1982年', '1990年', '2000年', '2010年', '2020年']
    male_population = [662, 869, 1331, 1543, 1757, 1898, 2147]
    female_population = [623, 807, 1256, 1462, 1653, 1791, 2007]
    bar = Line().add_xaxis(years).add_yaxis(
        '男性', male_population,
    ).add_yaxis('女性', female_population).set_global_opts(
        title_opts=opts.TitleOpts(title="福建人口总体趋势", subtitle='单位：万人'))
    return bar


@site_obj.register_chart(title='历年家庭结构', catalog='人口与就业', description='统计各种家庭类型（从单人户到十人以上户）的占比以及历年趋势', tags=['历年'])
def fj_family_type():
    family_types = [
        '一人户', '二人户', '三人户', '四人户', '五人户', '六人户', '七人户', '八人户', '九人户', '十人及其以上'
    ]
    data = [
        [1982, 7.7, 8.2, 12.2, 17.1, 18.4, 14.7, 10.1, 11.6, 0, 0],
        [1990, 5.8, 8.6, 16.8, 23.6, 21.4, 11.8, 5.9, 2.9, 1.4, 1.8],
        [2000, 9.1, 15.5, 25.4, 24.7, 15.8, 5.9, 2.2, 0.8, 0.3, 0.3],
        [2010, 12.1, 17.2, 24.3, 21.7, 13.7, 6.4, 2.6, 1.1, 0.5, 0.4],
        [2020, 27.3, 26.3, 19.4, 14.2, 6.9, 4, 1.1, 0.4, 0.2, 0.2]
    ]
    tl = Timeline()
    for item in data:
        year = item[0]
        bar = (
            Bar()
                .add_xaxis(family_types).add_yaxis('百分比(%)', item[1:])
                .set_global_opts(title_opts=opts.TitleOpts("福建省历年家庭户类型构成-{}年".format(year)))
        )
        tl.add(bar, "{}年".format(year))
    return tl


gdp_description = """福州超泉州全省第一；厦门突破7000亿；宁德升至第5，可望进入全国百强；漳州继续保持第4的位置，不过发展速度已经变缓，对比于2020年负增长，在2021年漳州已经有所好转。
"""
gdp_body = fake_long_text(total=6000)


@site_obj.register_chart(name='fj-map-gdp', title='福建省2021年GDP', description=gdp_description, body=gdp_body, top=1,
                         tags=['地图', '文章', '表格'])
def fj_map_gdp():
    nc = NamedCharts(page_title='福建省2021年GDP', is_combine=False)
    data = [(item[1], item[2]) for item in FJ_GDP2021_DATA]
    max_v = ceil_n(max([v[1] for v in data]))
    map1 = (
        Map()
            .add("GDP", data, "福建")
            .set_global_opts(title_opts=opts.TitleOpts(title="福建省2021年GDP", subtitle='单位：亿元'),
                             visualmap_opts=opts.VisualMapOpts(is_show=True, max_=max_v))
    )
    nc.add_widget(map1, height='350px')

    table = Table()
    fields = ['位次', '城市', 'GDP(万亿)', '同比增长(%)']
    table.add(fields, FJ_GDP2021_DATA,
              attributes={'class': bootstrap_table_class(border=True, striped=True)})
    nc.add_widget(table)
    return nc


@site_obj.register_chart(title='就业人员构成', catalog='人口与就业', description='历年就业人员第一、二、三产业人数及其比例。', tags=['历年', '就业'])
def employment_percentage():
    catalogs = ['第一产业', '第二产业', '第三产业']
    data = [
        ['2000年', 840, 439, 515],
        ['2005年', 723, 600, 600],
        ['2010年', 600, 774, 740],
        ['2020年', 323, 719, 1164]
    ]
    centers = [["20%", "30%"], ["55%", "30%"], ["20%", "70%"], ["55%", "70%"]]
    pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    for i, item in enumerate(data):
        pie.add(item[0], [list(z) for z in zip(catalogs, item[1:])], center=centers[i], radius=[60, 80])
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="就业人员构成"),
        legend_opts=opts.LegendOpts(
            type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
        )
    )
    return pie


@site_obj.register_chart(title='福建基础数据', catalog='基本信息', description='本表包含了福建省各地市的面积、经纬度（百度地图）。', top=4,
                         nav_after_separator=True)
def fj_data_table():
    table = Table()
    table.add(FJ_DATA_FIELDS, FJ_DATA, attributes={'class': bootstrap_table_class(border=True, striped=True)})
    return table


@site_obj.register_html_widget
def home1_panel():
    number_p = ValuesPanel()
    number_p.add(str(factory.chart_info_manager.count()), '图表总数', '个', catalog='danger')
    # number_p.add('42142', '网站访问量', '人次')
    number_p.add_widget(ValueItem('42142', '网站访问量', '人次'))
    number_p.add('8.0', '福建省2021年GDP增长率', '%', catalog='info')
    number_p.add('89.00', '中国联通5G套餐费用', '元', catalog='success')
    number_p.set_spans(6)
    return number_p


@site_obj.register_chart(description='本站用户最多搜索关键字。', title='搜索关键字词云', catalog='网站统计', nav_parent_name='none')
def search_word_cloud():
    data = [
        ("全省", "987"), ("福建", "534"), ("福州", "888"), ("房价", "777"), ("最大", "688"), ("面积", "388"),
        ("厦门", "823"), ("今年", "845"), ("去年", "515"), ("2021", "883"), ("GDP", "462"), ("城乡建设", "449"),
        ("社会保障", "407"), ("铁路", "406"), ("公交", "406"), ("就业", "386"), ("人口", "385"), ("地图", "775"),
        ("年鉴", "123"), ("上涨", "643"), ("三人户", "793"), ('莆田', '645'), ('宁德', '456'), ('漳州', '823'),
        ('泉州', '703'), ('南平', '498'), ('龙岩', '578'), ('三明', '630'), ('最新', '342'), ('下半年', '523'),
        ('饼图', '783'), ('历年', '547'), ('全国', '634'), ('世界', '232'), ('闽南', '437'), ('时间线', '562'),
        ("2020", "483"), ('第三产业', '647'), ('人均GDP', '423'), ('海西', '42'), ('劳动', '731'), ('交通', '103')

    ]
    wordcloud = (
        WordCloud()
            .add(series_name="搜索关键字", data_pair=data, word_size_range=[6, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="搜索关键字分析", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wordcloud


ia_description = """
全年固定资产投资19083.28亿元，比上年增长6.0%。第一产业投资357.77亿元,增长17.1%；第二产业投资6186.17亿元，增长11.6%，其中，工业投资6183.26亿元，增长11.6%；第三产业投资12539.34亿元，增长3.2%。
"""


@site_obj.register_chart(description=ia_description, title='福建省2021年分行业固定资产投资情况',
                         nav_parent_name='none')
def investment_amount():
    data = [
        ['农、林、牧、渔业', 410.89, 20.7],
        ['采矿业', 90.02, 47.6],
        ['制造业', 5322.07, 13.9],
        ['电力、热力、燃气及水生产和供应业', 771.17, -4.8],
        ['建筑业', 7.54, 44.5],
        ['批发和零售业', 142.69, 0.7],
        ['交通运输、仓储和邮政业', 1462.56, 3.6],
        ['住宿和餐饮业', 124.38, -21.6],
        ['信息传输、软件和信息技术服务业', 168.96, -4.0],
        ['金融业', 16.53, -6.1],
        ['房地产业', 6584.19, 1.1],
        ['租赁和商务服务业', 258.33, 26.1],
        ['科学研究和技术服务业', 73.18, 122.9],
        ['水利、环境和公共设施管理业', 2325.81, 6.1],
        ['居民服务、修理和其他服务业', 36.05, -12.8],
        ['教育', 450.92, 10.3],
        ['卫生和社会工作', 304.68, 5.4],
        ['文化、体育和娱乐业', 457.38, -0.1],
        ['公共管理、社会保障和社会组织', 75.94, 23.7]]

    pie = Pie()
    pie.add("", [(item[0], item[1]) for item in data])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="分行业固定资产投资情况(亿元)"),
                        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"), )
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.height = '800px'
    return pie


@site_obj.register_chart(title='福建省各县市GDP', top=1)
def my_geojson_demo():
    map1 = (
        Map().add(
            "2020年", FJ_SX_GDP_DATA, maptype="福建市县"
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="福建省2020年各县市GDP", subtitle='数据来源:福建统计年鉴2021;单位:亿元'),
            visualmap_opts=opts.VisualMapOpts(max_=2500)
        )
    )
    map1.height = '800px'

    use_geojson(map1, map_name='福建市县', url=geojson_url('fujian.geojson'))
    return map1


@site_obj.register_chart
def travel_map():
    lines_data = [
        ("福州站", "永泰站"), ("永泰站", "福州站"), ("福州站", "漳州站"), ("漳州站", "福州站"), ("漳州站", "厦门北站"),
        ("福州站", "三明北站"), ("三明北站", "泰宁站"), ("泰宁站", "福州站"), ("福州站", "连江站"), ("福州站", "福鼎站"),
        ("福鼎站", "福州站"), ("福州站", "延平站"), ("延平站", "福州站"), ("厦门北站", "福州南站"), ("福州南站", "福州站"),
        ("福州南站", "平潭站"), ("平潭站", "福州站"), ("永泰站", "三明北站"), ("武夷山北站", "福州站"),
        ("延平站", "武夷山北站"), ("永泰站", "晋江站"), ("晋江站", "厦门站"), ("厦门站", "厦门北站")
    ]
    mark_dic = {}
    for d in lines_data:
        for xd in d:
            if xd not in mark_dic:
                mark_dic[xd] = 1
            else:
                mark_dic[xd] += 1
    geo_map = Geo()
    geo_map.add_coordinate_json(os.path.join(settings.BASE_DIR, 'static', 'sc.json'))
    geo_map.add_schema(
        maptype="福建市县",
        itemstyle_opts=opts.ItemStyleOpts(color="#5C94BD", border_color="#F2ED7B"),
    ).add(
        "",
        [(k, v * 100) for k, v in mark_dic.items()],
        type_=ChartType.EFFECT_SCATTER,
        color="#73d973",
    ).add(
        "geo",
        lines_data,
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="blue"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
    ).set_series_opts(label_opts=opts.LabelOpts(is_show=False)).set_global_opts(
        title_opts=opts.TitleOpts(title="Geo-Lines-background"))
    geo_map.height = '800px'
    use_geojson(geo_map, map_name='福建市县', url=geojson_url('fujian.geojson'))
    return geo_map


@site_obj.register_collection(title='合辑01', catalog='合辑')
def my_collection():
    collection = WidgetCollection(name='test1', title='Test1', layout='s8')
    collection.add_html_widget(['home1_panel'])
    collection.add_chart_widget('search_word_cloud')
    collection.add_chart_widget('employment_percentage')
    collection.add_chart_widget('fj_family_type')
    return collection


class DemoView(DJESiteBackendView):
    template_name = 'demo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rc = RowContainer()
        c1 = factory.get_chart_widget('search_word_cloud')
        rc.add_widget(c1)

        rc2 = RowContainer()
        ni = ValueItem('8.0', '福建省2021年GDP增长率', '%', catalog='info')
        rc2.add_widget(ni, span=12)
        ni2 = ValueItem('42142', '网站访问量', '人次')
        rc2.add_widget(ni2, span=12)
        ni3 = ValueItem('89.00', '中国联通5G套餐费用', '元', catalog='success')
        rc2.add_widget(ni3, span=12)

        rc.add_widget(rc2)
        c2 = factory.get_chart_widget('fj_total_population')
        rc.add_widget(c2)

        context['rc'] = rc
        return context


site_obj.register_view('dje_about', DemoView)
