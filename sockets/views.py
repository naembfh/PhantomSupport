from django.shortcuts import render, redirect
from .models import Room, Message 

def Index(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']
        
        try:
            get_room = Room.objects.get(room_name=room)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
        
        # Redirect after the room is found or created
        return redirect('room', room_name=room, username=username)
    
    # Render the form if the request method is not POST
    return render(request, 'base.html')

def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)
    
    context = {
        "messages": get_messages,
        "user": username,
        "room_name": room_name,
    }
    
    return render(request, 'chatRoom.html', context)

