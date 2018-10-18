"""
Definition of views.
"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import BookForm, CourseForm, GradeFormSet, GradeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from app.models import *

@login_required(login_url='/login/')
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'userid' : request.user.id,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Adam Zalzal',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Welcome to Markbook, an interactive tool for setting academic goals and tracking your progress.',
            'year':datetime.now().year,
        }
    )
@login_required(login_url='/login/')
def newBook(request,userid):
    if userid != None:
        safe = Authentication(request.user.id, userid)
        if not safe:
            return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            temp = form.save()
            temp.user = User.objects.get( id = userid)
            temp.num_courses = 0
            temp.save()
            print('here')
            return HttpResponseRedirect('/'+userid+'/booklist')
        return HttpResponseRedirect('/'+userid+'/newbook')
    else:
        assert isinstance(request, HttpRequest)
        form= BookForm()
        print(request.method)
        return render(request, 'app/newbook.html',{'form':form})
   


@login_required(login_url='/login/')
def bookList(request,userid):
    
    assert isinstance(request, HttpRequest)
    thisUser = User.objects.get( id = userid)
    if userid != None:
        safe = Authentication(request.user.id, userid)
        print(safe)
        if safe == False:
            return HttpResponseRedirect('/')

    books = Book.objects.filter(user = thisUser)
    bookstotal = Book.objects.all()
    length2 = len(bookstotal)
    length = len(books)
    return render(request, 'app/booklist.html',{'books':books, 'length':length, 'length2':length2,'userid':userid})

@login_required(login_url='/login/')
def viewBook(request,userid,bookid):
    assert isinstance(request, HttpRequest)
    safe = Authentication(request.user.id, userid)
    if not safe:
        return HttpResponseRedirect('/')
    thisBook = Book.objects.get(id = bookid)
    courses = Course.objects.filter(book = thisBook)
    return render(request,'app/viewbook.html', {'userid':userid,'bookid':bookid,'courses':courses,'thisBook':thisBook})

@login_required(login_url='/login/')
def addCourse(request,userid,bookid):
    safe = Authentication(request.user.id, userid)
    if not safe:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
       form = CourseForm(request.POST)
       thisBook = Book.objects.get( id = bookid)
       if form.is_valid():
           thisBook.num_courses +=1
           thisBook.save()
           temp = form.save()
           temp.book = Book.objects.get( id = bookid)
           temp.num_items = 0
           temp.completion = 0.0
           temp.save()
       return HttpResponseRedirect('/'+userid+'/' + bookid +'/viewbook')
    else:
       assert isinstance(request, HttpRequest)
       form= CourseForm()
       return render(request, 'app/newcourse.html',{'form':form})

@login_required(login_url='/login/')
def viewGrades(request,userid,bookid,courseid):
    safe = Authentication(request.user.id, userid)
    if not safe:
        return HttpResponseRedirect('/')
    if request.method == 'POST' and 'update' in request.POST:
       thisCourse = Course.objects.get(id = courseid)
       form1 = CourseForm( request.POST, instance = thisCourse)
       form1.name = thisCourse.name
       print('check')
       if form1.is_valid():
           print('here')
           form1.save()
       else:
           print(form1.errors)
       return HttpResponseRedirect('/'+userid+'/' + bookid +'/'+ courseid+'/viewcourse')

    elif request.method=='POST':
       thisCourse = Course.objects.get(id = courseid)
       form = GradeFormSet(request.POST,queryset = Item.objects.filter(course = thisCourse))
       completion = 0.0
       thisCourse.completion = 0.0
       items = []
       for forms in form:
           if forms.is_valid():
               if forms.cleaned_data != {}:
                   forms.clean()
                   completion = completion + forms.cleaned_data['weight']
           else:
               return HttpResponseRedirect('/'+userid+'/' + bookid +'/'+ courseid+'/viewcourse')
       if completion> 100:
           error = 'Weight of items is greater than 100%'
           return HttpResponseRedirect('/'+userid+'/' + bookid +'/'+ courseid+'/viewcourse')
       
       for forms in form:
           if forms.is_valid():
               if forms.cleaned_data!={}:
                   temp = forms.save()
                   temp.course = thisCourse
                   temp.save()
                   thisCourse.completion = completion
                   thisCourse.save()
           else:
               error = 'Validation Error'
               break
           


               
               
               
       return HttpResponseRedirect('/'+userid+'/' + bookid +'/'+ courseid+'/viewcourse')
    else:
       assert isinstance(request, HttpRequest)
       thisCourse = Course.objects.get(id = courseid)
       items = Item.objects.filter(course = thisCourse)
       thisCourse.num_items = Item.objects.filter(course = thisCourse).count()
       thisCourse.save()
       if thisCourse.num_items!=0:
           updateMark(thisCourse)
           getRequired(thisCourse)
       form1 = CourseForm(instance = thisCourse)
       form= GradeFormSet(queryset = Item.objects.filter(course = thisCourse))
       print('current')
       print(thisCourse.current_mark)
       return render(request, 'app/viewcourse.html',{'form':form,
                                                     'bookid': bookid,
                                                     'userid': userid,
                                                     'courseid': courseid,
                                                     'thisCourse':thisCourse,
                                                     'form1': form1})


def updateMark(thisCourse):
    grades = Item.objects.filter(course = thisCourse)
    thisCourse.current_mark=0.0000
    weight_sum = 0.0 
    print('here')
    print(len(grades))
    
    if len(grades)!=0:
        for grade in grades:
            if(grade.mark!=None and grade.weight!=None):
                thisCourse.current_mark += grade.mark*grade.weight
                grade.required_mark = None
                grade.save()
                weight_sum = weight_sum + grade.weight
                thisCourse.save()
        print(thisCourse.completion)
        if (weight_sum!=0.0):
            thisCourse.current_mark = thisCourse.current_mark/weight_sum
    thisCourse.save()
    print(thisCourse.current_mark)

def createAccount(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
                    
            return HttpResponseRedirect('/')
        error = form.errors
        return render(request, 'app/createaccount.html',{'form':form,
                                                        'error':error})
    else:
        assert isinstance(request, HttpRequest)
        form= UserCreationForm()
       
        return render(request, 'app/createaccount.html',{'form':form})
def getRequired(thisCourse):
    grades = Item.objects.filter(course = thisCourse)
    weight= 0.0
    completed_weight= 0.0
    remaining_weight = 0.0
    for grade in grades:
        if(grade.weight != None):

            weight += grade.weight
            if(grade.mark != None):
                completed_weight += grade.mark*grade.weight*0.01
            else:
                remaining_weight += grade.weight
    if remaining_weight!=0.0:
        required = (weight*thisCourse.goal_mark*0.01-completed_weight)/remaining_weight
        for grade in grades:
             if(grade.mark== None and grade.weight !=None):
                 grade.required_mark = required*100
                 grade.save()


def deleteBook(request,userid,bookid):
    safe = Authentication(request.user.id, userid)
    if not safe:
        return HttpResponseRedirect('/')
    thisBook = Book.objects.get(id = bookid)
    thisBook.delete()
    return HttpResponseRedirect('/' + userid + '/booklist')

def deleteCourse(request,userid,bookid,courseid):
    safe = Authentication(request.user.id, userid)
    if not safe:
        return HttpResponseRedirect('/')
    thisCourse = Course.objects.get(id = courseid)
    thisCourse.delete()
    return HttpResponseRedirect('/' + userid + '/' + bookid + '/viewbook')

def deleteItem(request,userid,bookid,courseid,itemid):
    safe = Authentication(request.user.id, userid)
    if not safe:
        return HttpResponseRedirect('/')
    thisItem = Item.objects.get(id = itemid)
    thisItem.delete()
    thisCourse = Course.objects.get(id= courseid)
    updateMark(thisCourse)
    return HttpResponseRedirect('/' + userid + '/' + bookid + '/' + courseid + '/viewcourse')

def Authentication(thisUser,id):
    print(thisUser)
    print(id)
    if int(thisUser) != int(id):
        return False
    else:
        return True

