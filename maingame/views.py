# -*- coding: utf-8 -*-

import json

from django.views import generic
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import TemplateArmyCreateForm, TemplateRobotCreateForm


from .models import AvailableMaps, TemplateArmy, TemplateRobot

class UserLoginView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserLoginView, self).dispatch(*args, **kwargs)


class AvailableMapListview(generic.ListView):
    model = AvailableMaps
    template_name = 'maingame/list_available_maps.html'

class AvailableMapsDetailview(generic.DetailView):
    model = AvailableMaps
    template_name = 'maingame/available_maps.html'


    def get_context_data(self, **kwargs):
        context = super(AvailableMapsDetailview, self).get_context_data(**kwargs)
        object = context['object']
        tab_map = []
        width = object.width
        tile_size = object.tile_size
        map = json.loads(object.data)
        print map
        while len(map) > 0:
            one_line = []
            for i in xrange(width):
                index = map.pop(0)
                x = ((index % 4) - 1) * tile_size
                y = (index / 4) * tile_size
                one_line.append((x,y))
            tab_map.append(one_line)
        context['map'] = tab_map
        return context


def index_view(request):
    if request.user.is_anonymous():
        return render_to_response('maingame/anonymous_index.html', {},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('maingame/user_index.html', {},
                                  context_instance=RequestContext(request))

class MyArmiesListView(generic.ListView, UserLoginView):
    model = TemplateArmy
    template_name = 'maingame/my_armies.html'

    def get_queryset(self):
        return TemplateArmy.objects.filter(owner=self.request.user).order_by('-finish')

    def get_finished_armies(self):
        return TemplateArmy.objects.filter(owner=self.request.user, finish=True)

    def get_unfinished_armies(self):
        return TemplateArmy.objects.filter(owner=self.request.user, finish=False)



class RobotCreateView(generic.CreateView, UserLoginView):
    model = TemplateRobot
    form_class = TemplateRobotCreateForm

    def get_success_url(self):
        return reverse('my_armies', kwargs={})


class ArmyCreateView(generic.CreateView, UserLoginView):
    model = TemplateArmy
    form_class = TemplateArmyCreateForm

    def get_success_url(self):
        return reverse('my_armies', kwargs={})


    def get_form_kwargs(self):
        kwargs = super(ArmyCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class ArmyDetailView(generic.DetailView, UserLoginView):
        model = TemplateArmy
        template_name = "maingame/one_army.html"


        def get(self, request, *args, **kwargs):
            self.object = self.get_object()
            if self.object.owner != self.request.user:
                raise PermissionDenied
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
