from typing import Any

from django_echarts.entities import (
    Container, RowContainer, ValuesPanel, Title
)
from django_echarts.stores.entity_factory import factory
from django_echarts.views import PageTemplateView


class MyDashboardView(PageTemplateView):
    template_name = 'dashboard.html'

    def get_container_obj(self) -> Any:
        container = Container(div_class='container-fluid')
        mrc = RowContainer()
        container.add_widget(mrc)
        rc1 = RowContainer()

        mrc.add_widget(rc1)

        number_p = ValuesPanel()
        number_p.add('8.0', '福建省2021年GDP增长率', '%', catalog='info')
        number_p.add('89.00', '中国联通5G套餐费用', '元', catalog='success')
        rc1.add_widget(number_p, span=12)

        rc2 = RowContainer()
        rc2.add_widget(Title('福建疫情', small_text='2022年3月'))
        rc22 = RowContainer()
        rc22.add_widget(factory.get_widget_by_name('my_geojson_demo'), height='600px')
        rc2.add_widget(rc22, span=12)

        mrc.add_widget(rc2)

        rc3 = RowContainer()
        mrc.add_widget(rc3)
        return container
