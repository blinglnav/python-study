from functools import wraps
from study_user.models import *

def admin_only(func):
    @wraps(func)
    def admin_check_view(request, *args, **kwargs):
        if request.
