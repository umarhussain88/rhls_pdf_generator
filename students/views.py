from django.views.generic import ListView
from .models import Student 
from django.db.models import Q 

class StudentView(ListView):
    template_name = 'home.html'
    context_object_name = 'student_list'
    model = Student

    def get_queryset(self): 
        # if not self.request.POST:
            # query = Student.objects.first().student_id
        # else:
        query = self.request.GET.get('student_id')
        print(query)
        return Student.objects.filter(
            Q(student_id=query) )