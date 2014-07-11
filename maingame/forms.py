# -*- coding: utf-8 -*-


#from django import forms
import floppyforms as forms

from .models import TemplateArmy, TemplateRobot

class TemplateArmyCreateForm(forms.ModelForm):

    class Meta:
        model = TemplateArmy
        fields = ['name', 'army_class']


    def __init__(self, owner, *args, **kwargs):
        super(TemplateArmyCreateForm, self).__init__(*args, **kwargs)
        self.owner = owner

    def save(self, commit=True):
        instance = super(TemplateArmyCreateForm, self).save(commit=False)
        instance.owner = self.owner
        instance.finish = False
        return instance.save(commit)


class TemplateRobotCreateForm(forms.ModelForm):

    class Meta:
        model = TemplateRobot
