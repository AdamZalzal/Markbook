"""
Definition of urls for Markbook.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^login/$',
        LoginView.as_view(template_name="app/login.html", authentication_form = app.forms.BootstrapAuthenticationForm, extra_context = {
                'title': 'Log in',
                'year': datetime.now().year,
            }),
        name='login'),
    url(r'^logout$',
        LogoutView.as_view(next_page = '/'),
        
        name='logout'),
    url(r'^(?P<userid>\d+)/newbook$', app.views.newBook, name='newBook'),
    url(r'^(?P<userid>\d+)/booklist$', app.views.bookList, name='bookList'),
    url(r'^(?P<userid>\d+)/(?P<bookid>\d+)/viewbook$', app.views.viewBook, name='viewBook'),
    url(r'^(?P<userid>\d+)/(?P<bookid>\d+)/deletebook$', app.views.deleteBook, name='deleteBook'),
    url(r'^(?P<userid>\d+)/(?P<bookid>\d+)/addcourse$', app.views.addCourse, name='addCourse'),
    url(r'^(?P<userid>\d+)/(?P<bookid>\d+)/(?P<courseid>\d+)/viewcourse$', app.views.viewGrades, name='viewGrades'),
    url(r'^(?P<userid>\d+)/(?P<bookid>\d+)/(?P<courseid>\d+)/deletecourse$', app.views.deleteCourse, name='deleteCourse'),
    url(r'^(?P<userid>\d+)/(?P<bookid>\d+)/(?P<courseid>\d+)/(?P<itemid>\d+)/deleteitem$', app.views.deleteItem, name='deleteItem'),
    url(r'^createaccount$', app.views.createAccount, name='createAccount'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
