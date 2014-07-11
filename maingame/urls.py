# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url



from .views import (AvailableMapListview, AvailableMapsDetailview,
                    index_view, MyArmiesListView, ArmyCreateView,
                    ArmyDetailView, RobotCreateView)


urlpatterns = patterns('',
    url(r'maingame/maps$',  AvailableMapListview.as_view(), name='list_available_maps'),
    url(r'maingame/map/(?P<pk>\d+)$', AvailableMapsDetailview.as_view(), name="available_map_detail" ),
    url(r'maingame/my_armies$',  MyArmiesListView.as_view(), name='my_armies'),
    url(r'maingame/army/(?P<pk>\d+)$', ArmyDetailView.as_view(), name="army_detail" ),
    url(r'maingame/create_armies$', ArmyCreateView.as_view(), name='add_army'),
    url(r'maingame/create_robot$', RobotCreateView.as_view(), name='add_robot_to_army'),
    url(r'^$', index_view, name="index"),
)
