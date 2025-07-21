from django.http import HttpResponse

def sayHello(request):
    
    # Get the name parameter from the URL query string.  
    name = request.GET.get("name")
    
    # Return an HTTPResponse with a "Hello" message that includes the name. 
    return HttpResponse("Hello, {}!".format(name)) 
