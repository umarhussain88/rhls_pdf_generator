from django.views.generic import ListView
from .models import Student 
from django.db.models import Q 
import pandas as pd 

class StudentView(ListView):
    template_name = 'home.html'
    context_object_name = 'student_list'
    model = Student

    # df = pd.DataFrame({'date' : pd.date_range('01 Sep 2021', '01 Apr 2022',freq='W-MON')})
    df = pd.read_csv('sql/rhls_2021_cal.csv')

    d =  df.set_index([df.index % 20, df.groupby((df.index) // 2).cumcount()])
    cal = [y['date'].tolist() for x,y in d.groupby(level=0)]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["calendar"] =  self.cal
        
        return context
    

    def get_queryset(self): 
        # if not self.request.POST:
            # query = Student.objects.first().student_id
        # else:
        query = self.request.GET.get('student_id')
        print(query)
        return Student.objects.filter(
            Q(student_id=query) )