from django.shortcuts import render
import pandas as pd 
from django.views.generic import TemplateView

class StudentView(TemplateView):
    template_name = 'home.html'