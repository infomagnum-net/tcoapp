from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.

def index(request):
	return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')



def Testing(request):
    return render(request, 'home.html')


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response    


