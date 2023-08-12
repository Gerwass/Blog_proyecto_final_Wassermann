from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from perfiles.models import CanalMensaje, CanalUsuario, Canal
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import DetailView
from django.core.exceptions import PermissionDenied
from .forms import FormMensaje
from django.views.generic.edit import FormMixin



from perfiles.forms import UserRegisterForm, UserUpdateForm


from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from perfiles.forms import UserRegisterForm,AvatarFormulario

def registro(request):
   if request.method == "POST":
       formulario = UserRegisterForm(request.POST)

       if formulario.is_valid():
           formulario.save()  # Esto lo puedo usar porque es un model form
           url_exitosa = reverse('inicio')
           return redirect(url_exitosa)
   else:  # GET
       formulario = UserRegisterForm()
   return render(
       request=request,
       template_name='perfiles/registro.html',
       context={'form': formulario},
   )



def login_view(request):
   next_url = request.GET.get('next')
   if request.method == "POST":
       form = AuthenticationForm(request, data=request.POST)

       if form.is_valid():
           data = form.cleaned_data
           usuario = data.get('username')
           password = data.get('password')
           user = authenticate(username=usuario, password=password)
           # user puede ser un usuario o None
           if user:
               login(request=request, user=user)
               if next_url:
                   return redirect(next_url)
               url_exitosa = reverse('inicio')
               return redirect(url_exitosa)
   else:  # GET
       form = AuthenticationForm()
   return render(
       request=request,
       template_name='perfiles/login.html',
       context={'form': form},
   )



class CustomLogoutView(LogoutView):
   template_name = 'perfiles/logout.html'


class MiPerfilUpdateView(LoginRequiredMixin, UpdateView):
   form_class = UserUpdateForm
   success_url = reverse_lazy('inicio')
   template_name = 'perfiles/formulario_perfil.html'

   def get_object(self, queryset=None):
       return self.request.user
   


def agregar_avatar(request):
    if request.method == "POST":
        formulario = AvatarFormulario(request.POST, request.FILES) 

        if formulario.is_valid():
            avatar = formulario.save()
            avatar.user = request.user
            avatar.save()
            url_exitosa = reverse('inicio')
            return redirect(url_exitosa)
    else:  # GET
        formulario = AvatarFormulario()
    return render(
        request=request,
        template_name="perfiles/formulario_avatar.html",
        context={'form': formulario},
    )


def about(request):
    return render(
        request=request,
        template_name="perfiles/about.html"
    )



class CanalFormMixin(FormMixin):
    form_class = FormMensaje
    
    def get_success_url(self):
        return self.request.path

    def post(self,request, *args, **kwagrs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        
        form = self.get_form()
        if form.is_valid():
            canal = self.get_object()
            usuario = self.request.user
            mensaje = form.cleaned_data.get("mensaje")
            canal_obj = CanalMensaje.objects.create(canal = canal, usuario=usuario, texto = mensaje)
            
            if request.is_ajax():
                return JsonResponse({
                    
                    'mensaje':canal_obj.texto,
                    'username' : canal_obj.usuario.username
                    }, status = 201 )

            
            return super().form_valid(form)
        else:
            if request.is_ajax():
                return JsonResponse({"Error": form.errors}, status=400)

            return super().form_invalid(form)

class CanalDetailView(LoginRequiredMixin,CanalFormMixin,DetailView):
    model = Canal
    template_name = 'perfiles/canal_detail.html'
    query_set = Canal.objects.all()


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        obj = context['object']
        print(obj)

    #    if self.request.user not in obj.usuarios.all():
    #        raise PermissionDenied
        context['si_canal_miembro']  = self.request.user in obj.usuarios.all()

        return context

    #def get_queryset(self):

    #    usuario = self.request.user
    #    username = usuario.username
    #    qs = Canal.objects.all().filtrar_por_username(username)
    #    return qs


class DetailsMs(LoginRequiredMixin,DetailView):

    template_name = 'perfiles/canal_detail.html'

    def get_object(self,*args,**kwars):
        username = self.kwargs.get("username")
        mi_username = self.request.user.username
        canal, _ = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)

        if username ==  mi_username:
            mi_canal, _ = Canal.objects.obtener_o_crear_canal_usuario_actual(self.request.user)

            return mi_canal

        if canal == None:
            raise Http404

        return canal


def mensajes_privados(request, username, *args, **kwargs):

    if not request.user.is_authenticated:
        return HttpResponse("Prohibido")
    
    mi_username = request.user.username


    canal, created = Canal.objects.obtener_o_crear_canal_ms(mi_username, username)
    if created:
        print("si, fue creadeo")
    
        
    Usuarios_Canal=canal.canalusuario_set.all().values("usuario__username")
    print(Usuarios_Canal)
    mensaje_canal = canal.canalmensaje_set.all()
    print(mensaje_canal.values("texto"))



    return HttpResponse(f"Nuestro ID del Canal - {canal.id}")