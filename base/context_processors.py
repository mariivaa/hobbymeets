from .models import Topic, Room

#ontext that is available to all templates, added path in settings.py
def globalVars(request):
    topics = Topic.objects.all()
    top_topics = Topic.objects.all()[0:5] #lazy way of making above request work in the template:))
    total_room_count = Room.objects.all().count()
    
    context = {'topics': topics, 'total_room_count': total_room_count, 'top_topics': top_topics}
    return context