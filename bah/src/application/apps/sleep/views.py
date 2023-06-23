from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .models import Sleeper
from .tasks import sleeping_task

# Create your views here.
@login_required(login_url='login')
def sleeping_time(request):
    if request.method == 'POST':
        n = request.POST['sleep_number']
        sleeper = Sleeper.objects.create(
            input=int(n),
            time_asleep=0,
            status=Sleeper.STATUS_PENDING,
        )
        sleeping_task.delay(sleeper.id)
        return redirect('sleep:sleeping_list')
    
    return render(request, 'sleeping_time.html')


@login_required(login_url='login')
def sleeping_list(request):
    sleepers = Sleeper.objects.all()
    return render(request, 'sleeping_list.html', {'sleepers': sleepers})

