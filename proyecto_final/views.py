

from datetime import datetime

from django.shortcuts import render

from blog.models import Posteo



def inicio(request):
    posteos = Posteo.objects.all()
    
    http_response = render (
        request=request,
        template_name="inicio.html",
        context = { "posteos" : posteos
                    }    
    )
    return http_response