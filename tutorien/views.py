# encoding: utf-8
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import inlineformset_factory
from tutorien.models import Tut, TutDate, Attendance, TutUser, TutorSuggestion
from tutorien.forms import LoginForm, CreateTutForm, TutorSuggestionForm
from django_auth_ldap import *
from django.core.mail import send_mail
from datetime import datetime
import logging

def index(request):
    title = "Startseite"
    divid = "startseite"
    c = RequestContext(request,{"title":title, "divid":divid })
    return render(request,'tutorien/index.html', c, context_instance=RequestContext(request))


def GetTuts(request):
    title       = "Tutorienuebersicht"
    pagetitle   = "Tutorien"
    divid       = "tutorien"
    status      = ""
    statuscls   = ""
    attendances = ""
    teaching    = ""
    attendants  = ""

    # Einlesen der Parameter
    tut         = int(request.GET.get('id',0))
    action      = request.GET.get('a','')

    # überprüft ob der Benutzer eingeloggt ist
    if( request.user.is_authenticated() ):
        current_user = request.user
        
        # holt alle Tutorien, an denen der aktuelle Benutzer teilnimmt
        attendances = Attendance.objects.filter(user=current_user).values_list('tut',flat=True)
        # holt alle Tutorien, bei denen der Tutor unterrichtet
        teaching = Tut.objects.filter(tutor=current_user)
        # hollt alle anmeldungen
        attendants = Attendance.objects.all();
        print attendants


        # wenn die beiden Parameter übergeben werden
        if(tut and action):
            # kein .get, da sonst bei leerem Ergebnis eine Exception entsteht
            attendance = Attendance.objects.filter(user=current_user,tut=tut)
            # Zwischenspeichern des aktuellen Tutoriums
            current_tut = Tut.objects.get(id=tut)
            # Zwischenspeichern des Namen des Tutoriums
            tutname = Tut.objects.get(id=request.GET.get('id','')).name
            # Liste der Tutorien, die der Benutzer hält

            # falls der Benutzer beim Tut angemeldet werden soll
            if( action == "reg" ):
                # wenn bereits eine Anmeldung vorliegt
                if(attendance):
                    # nicht anmelden, nur hinweisen
                    status = u'Du bist bereits für das Tutorium "'+ tutname +'"" angemeldet!'
                    statuscls = "red"
                else:
                    # ansonten anmelden und Mail verschicken
                    Attendance(user=current_user, tut=current_tut).save();
                    status = u'Du bist nun für das Tutorium "'+ tutname +'"" angemeldet!'
                    statuscls = "blue"
                    #TO-DO: Texte
                    send_mail('Du bist nun beim Tutorium "'+tutname+'" angemeldet!', 
                        u'Hey '+current_user.first_name+u',\n\nDu bist nun für das Tutorium "'+tutname+'" angemeldet. \n\nViele Gruesse\nDeine SVG', 'neptunslawa@googlemail.com',[current_user.email], fail_silently=False)
            # analog zu oben, falls der Benutzer abgemeldet werden soll
            if( action == "rem" ):
                if(attendance):
                    Attendance.objects.get(user=current_user, tut=current_tut).delete()
                    status = u'Du hast dich nun vom Tutorium "'+tutname+'" abgemeldet.'
                    statuscls = "blue"
                    #TO-DO: Texte
                    send_mail('Du bist nun beim Tutorium "'+tutname+'" angemeldet!', 
                        u'Hey '+current_user.first_name+u',\n\nDu bist nun vom Tutorium "'+tutname+'" abgemeldet. \n\nViele Gruesse\nDeine SVG', 'neptunslawa@googlemail.com',[current_user.email], fail_silently=False)
                else:
                    # sollte im Normalfall nicht aufrufbar sein, aber wenn doch
                    status = u'Du bist nicht für dieses Tutorium angemeldet.'
                    statuscls = "red"

    # wenn keine Parameter übergeben werden, soll der Benutzer eine Übersicht aller Tutorien erhalten
    tutorien = Tut.objects.all().order_by('name')
  
    c = RequestContext(request, {'title':title, 'divid':divid, 'pagetitle':pagetitle, 'tutorien':tutorien, 'status':status, 'statuscls':statuscls, 'attendances':attendances, 'teaching':teaching, 'attendants':attendants})
    return render(request, 'tutorien/tuts.html',c,context_instance=RequestContext(request))

# nur vom SU aufrufbar
@user_passes_test(lambda u: u.is_superuser)
def CreateTut(request):
    pagetitle = "Tutorium Erstellen"   
    name = ''

    # wenn ein POST vorliegt
    if request.method == 'POST':
        # erstelle die nötigen Formulare


        if 'add_tutDate' in request.POST:
            extra = extra+1
            print(extra)
            TutFormSet = inlineformset_factory(Tut, TutDate, extra=extra)
            form = CreateTutForm(request.POST) # Formular zum Erstellen eines Tutoriums
            formset = TutFormSet(request.POST) # InlineFormular für TutDates

            return render(request, 'tutorien/createTut.html', {'form':form, 'formset':formset, 'pagetitle':pagetitle, 'status':'Tutorium "'+name+'"" wurde erfolgreich erstellt!'})



        elif 'submit' in request.POST:
            TutFormSet = inlineformset_factory(Tut, TutDate, extra=extra)
            form = CreateTutForm(request.POST) # Formular zum Erstellen eines Tutoriums
            formset = TutFormSet(request.POST) # InlineFormular für TutDates
            
            if form.is_valid() and formset.is_valid():
                # speichere das Tut ab, das ModelForm übernimmt das Mapping der Formular-Felder auf die Tutorium-Felder
                tutorium = form.save()
                name = tutorium.name
                
                # Überprüfen der Subforms
                for subform in formset:
                    if(subform.is_valid):
                        # speichere das InlineFormular, aber noch kein Commit,
                        # da wir noch den Tutorium PK setzen müssen
                        tutdate = subform.save(commit=False)
                        # Setzen der Tutorium-Refernz und abspeichern
                        tutdate.tutorium = tutorium
                        tutdate.save()
                        # nach commit_False immer save_m2m aufrufen
                        subform.save_m2m()
                #cleanup, da _noch_ alle 3 Subforms angelegt werden, selbst wenn die Werte leer sind. Daraus entstehen leere TutDates, die in diesem Schritt gelöscht werden
                TutDate.objects.filter(date=None).delete()
                
                return render(request, 'tutorien/createTut.html', {'form':form, 'formset':formset, 'pagetitle':pagetitle, 'status':'Tutorium "'+name+'"" wurde erfolgreich erstellt!'})
    else:
        TutFormSet = inlineformset_factory(Tut, TutDate, extra=1)
        form = CreateTutForm()
        formset = TutFormSet()

    
    context = { 'form':form, 'pagetitle':pagetitle, 'formset':formset }
    return render(request, 'tutorien/createTut.html', context, context_instance=RequestContext(request))

def CreateTut2(request, tut_id=2):
    pagetitle = "CreateTut2"

    tut = Tut.objects.get(pk=tut_id)
    DateInlineFormSet = inlineformset_factory(Tut, TutDate, extra=0)
    if request.method == "POST":
        formset = DateInlineFormSet(request.POST, request.FILES, instance=tut)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(tut.get_absolute_url())
    else:
        formset = DateInlineFormSet(instance=tut)
    return render_to_response("tutorien/createTut2.html", {
        "formset": formset,
    })

# nur mit Login aufrufbar
@login_required
def CreateTutorSuggestion(request):
    title = "Bewerben"
    pagetitle = "Bewerben"
    status = ""

    # sollte im Normalfall nicht aufrufbar sein, da du @login-required bereits abgedeckt, falls aber ein Redirect erfolgen muss
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    # Wenn ein POST vorliegt
    if request.method == 'POST':
        # erstelle neues SuggestionForm
        form = TutorSuggestionForm(request.POST)
        # Validierung
        if form.is_valid():
            tutor = request.user
            faculty = request.user.faculty
            tutname = form.cleaned_data['tutname']
            text = form.cleaned_data['text']
            # liegt ein Vorschlag von diesem Benutzer für dieses Tutorium bereits vor?
            suggestion = TutorSuggestion.objects.filter(tutor=tutor, tutname=tutname)
            # wenn ja, nur hinweisen
            if(suggestion):
                status = u'Du hast dich für dieses Tutorium bereits beworben!'
                return render(request, 'tutorien/tutorSuggestion.html', {'form':form, 'title':title, 'pagetitle':pagetitle, 'status':status})
            # ansonsten Vorschlag einsenden
            else:
                TutorSuggestion(tutor=tutor, faculty=faculty, tutname=tutname, text=text).save()
                status = u'Deine Bewerbung für das Tutorium '+tutname+' wurde angenommen!'
                return render(request, 'tutorien/tutorSuggestion.html', {'form':form, 'title':title, 'pagetitle':pagetitle, 'status':status})
        # wenn Formular fehlerhaft    
        else:
            return render(request, 'tutorien/tutorSuggestion.html', {'form':form, 'title':title, 'pagetitle':pagetitle})
    # wenn kein POST vorliegt, Formular anzeigen
    else:
        form = TutorSuggestionForm()
        context = {'form':form}
        return render(request, 'tutorien/tutorSuggestion.html',{'form':form, 'title':title, 'pagetitle':pagetitle })

# nur für SU
@user_passes_test(lambda u: u.is_superuser)
def manageUsers(request):
    title = "Benutzerverwaltung"
    pagetitle = "Benutzerverwaltung"
    users = TutUser.objects.all().order_by('-groups','last_name')
    uid = request.GET.get('uid','')
    action = request.GET.get('a','')
    # wenn beide Parameter übergeben werden
    if(uid and action):
        uid = int(uid)
        # wenn der Benutzer zum Tutor gemacht werden soll
        if(action == "add"):
            TutUser.objects.get(id=uid).groups.add(Group.objects.get(name='Tutor'))
            print TutUser.objects.get(id=uid).groups.all()
        # wenn der Tutor wieder Benutzer werden soll
        if(action == "rem"):
            TutUser.objects.get(id=uid).groups.remove(Group.objects.get(name='Tutor'))
            print TutUser.objects.get(id=uid).groups.all()

    # für jeden Benutzer abfragen, ob er Tutor ist (wird im template verwendet) 
    for u in users:
        u.is_tutor = u.groups.filter(name='Tutor')
    c = {'title':title, 'pagetitle':pagetitle, 'users':users}
    return render(request, 'tutorien/manageUsers.html', c)

@user_passes_test(lambda u: u.is_superuser)
def getSuggestions(request):
    title = "Bewerbungen"
    pagetitle = "Bewerbungen"
    suggestions = TutorSuggestion.objects.all().order_by('tutor')
    c = {'title':title, 'pagetitle':pagetitle, 'suggestions':suggestions}
    return render(request, 'tutorien/bewerbungen.html', c)

def MyData(request):
    title = "Meine Daten"
    pagetitle = "Meine Daten"
    c = {'title':title, 'pagetitle':pagetitle}
    return render(request, 'tutorien/meineDaten.html', c)

@csrf_exempt
def LoginRequest(request):
    # sollte nicht aufrufbar sein, aber falls jemand die URL direkt aufruft und eingeloggt ist, einfach zum Index leiten
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next','/'))
            else:
                status = 'Dein Benutzername oder Passwort ist falsch!'
                return render(request, 'tutorien/index.html', {'form':form, 'status':status}, context_instance=RequestContext(request))
        else:
            return render(request, form.POST['next'], {'form':form}, context_instance=RequestContext(request)) 
    else:
        form = LoginForm()
        context = {'form':form}
        return render(request, 'tutorien/index.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
    logout(request)
    print request
    return HttpResponseRedirect(request.GET.get('next'),'/')    

# wird nur in der Production-Version verwendet, wenn DEBUG off ist.
def NotFound(request):
    return render_to_response('tutorien/404.html',{})