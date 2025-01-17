import datetime
from django.utils import timezone

def session_checker(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        session = request.session

        if not session.get('created_at'):
            print('new session created')
            session['created_at'] = timezone.now().isoformat()
  
            response = get_response(request)
            session['cookie_message'] = 1
        
        else:
            print('session already exists')
            response = get_response(request)

        

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware