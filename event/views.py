from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from event.models import Event, Category
from event.forms import EventModelForm, CategoryModelForm

# Create your views here.
def home(request):
    return render(request, "event/dashboard.html")

def create_event(request):
    if request.method == "POST":
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Created Successfully!")
            print("Event  Created Successfully!")
            return redirect("event_list")
        else:
            print("Form errors:", form.errors)
    else:
        form = EventModelForm()
        
    return render(request, "task_form.html", {"form": form})

def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventModelForm(instance=event)
    
    if request.method == "POST":
        form = EventModelForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Updated Successfully!")
            return redirect("event_list")
    
    return render(request, "event/event_form.html", {"form": form})

def delete_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event Deleted Successfully!")
    else:
        messages.error(request, "Something went wrong")
    return redirect("event_list")

from django.shortcuts import render
from .models import Event

def event_list(request):
    query = request.GET.get('q', '')  
    if query:
        events = Event.objects.filter(name__icontains=query) | Event.objects.filter(location__icontains=query)
    else:
        events = Event.objects.all()

    return render(request, "event/event_list.html", {"events": events, "query": query})


def create_category(request):
    if request.method == "POST":
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Created Successfully!")
            return redirect("event_list")
    else:
        form = CategoryModelForm()
    return render(request, "event/category_form.html", {"form": form})

def category_list(request):
    categories = Category.objects.annotate(num_events=Count("event")).order_by("num_events")
    return render(request, "event/category_list.html", {"categories": categories})
