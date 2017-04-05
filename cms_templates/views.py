from django.shortcuts import render
from cms_templates.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

# Create your views here.


def show_template(request):
    if request.user.is_authenticated():
        login = "Logged in as " + request.user.username + \
                ". <a href='/logout'>Logout</a><br><br>"
    else:
        login = "Not logged in. <a href='/login'>Login</a><br><br>"

    content = Pages.objects.all()
    response = "Contenido de la base de datos:<br>"
    for entry in content:
        response = response + entry.name + " => " + entry.page + "<br>"

    plantilla = get_template("miplantilla.html")
    contexto = Context({'title': login, 'content': response})

    return HttpResponse(plantilla.render(contexto))


def show(request):
    if request.user.is_authenticated():
        response = "Logged in as " + request.user.username + \
                   ". <a href='/logout'>Logout</a><br><br>"
    else:
        response = "Not logged in. <a href='/login'>Login</a><br><br>"

    content = Pages.objects.all()
    response += "Contenido de la base de datos:<br>"
    for entry in content:
        response = response + entry.name + " => " + entry.page + "<br>"

    return HttpResponse(response)


@csrf_exempt
def entry_template(request, identifier):

    if request.user.is_authenticated():
        user = True
        login = "Logged in as " + request.user.username + \
                ". <a href='/logout'>Logout</a><br><br>"
    else:
        user = False
        login = "Not logged in. <a href='/login'>Login</a><br><br>"

    if request.method == "POST":
        content = Pages(name=request.POST['nombre'],
                        page=request.POST['pagina'])
        content.save()
    elif request.method == "PUT":
        # Form of data in the body: name='<nombre>'&page='<pagina>'
        if user:
            body = request.body.decode('utf-8')
            [parsed_name, parsed_page] = body.split("&")
            content = Pages(id=identifier, name=parsed_name, page=parsed_page)
            content.save()

    try:
        entry = Pages.objects.get(id=identifier)
        response = "La pagina solicitada es:<br>" + entry.name + \
                   " => " + entry.page
    except Pages.DoesNotExist:
        if user:
            response = "No existe en la base de datos. Creala:<br><br>"
            response += "<form action='' method = 'POST'>Nombre:<br>" + \
                        "<input type='text' name='nombre'><br>Pagina:<br>" + \
                        "<input type='text' name='pagina'><br>" + \
                        "<br><input type='submit' value='Enviar'>"
        else:
            response = "No tienes permiso para añadir contenido. " + \
                       "Necesitas hacer login"

    plantilla = get_template("miplantilla.html")
    contexto = Context({'title': login, 'content': response})

    return HttpResponse(plantilla.render(contexto))


@csrf_exempt
def entry(request, identifier):

    if request.user.is_authenticated():
        user = True
        response = "Logged in as " + request.user.username + \
                   ". <a href='/logout'>Logout</a><br><br>"
    else:
        user = False
        response = "Not logged in. <a href='/login'>Login</a><br><br>"

    if request.method == "POST":
        content = Pages(name=request.POST['nombre'],
                        page=request.POST['pagina'])
        content.save()
    elif request.method == "PUT":
        # Form of data in the body: name='<nombre>'&page='<pagina>'
        if user:
            body = request.body.decode('utf-8')
            [parsed_name, parsed_page] = body.split("&")
            content = Pages(id=identifier, name=parsed_name, page=parsed_page)
            content.save()

    try:
        entry = Pages.objects.get(id=identifier)
        response += "La pagina solicitada es:<br>" + entry.name + \
                    " => " + entry.page
    except Pages.DoesNotExist:
        if user:
            response += "No existe en la base de datos. Creala:<br><br>"
            response += "<form action='' method = 'POST'>Nombre:<br>" + \
                        "<input type='text' name='nombre'><br>Pagina:<br>" + \
                        "<input type='text' name='pagina'><br>" + \
                        "<br><input type='submit' value='Enviar'>"
        else:
            response += "No tienes permiso para añadir contenido. " + \
                        "Necesitas hacer login"

    return HttpResponse(response)


def error_template(request):
    if request.user.is_authenticated():
        login = "Logged in as " + request.user.username + \
                   ". <a href='/logout'>Logout</a><br><br>"
    else:
        login = "Not logged in. <a href='/login'>Login</a><br><br>"

    response = "La pagina solicitada no se encuentra disponible"

    plantilla = get_template("miplantilla.html")
    contexto = Context({'title': login, 'content': response})

    return HttpResponse(plantilla.render(contexto))


def error(request):
    if request.user.is_authenticated():
        response = "Logged in as " + request.user.username + \
                   ". <a href='/logout'>Logout</a><br><br>"
    else:
        response = "Not logged in. <a href='/login'>Login</a><br><br>"

    response += "La pagina solicitada no se encuentra disponible"

    return HttpResponse(response)
