from django.shortcuts import redirect
from django.urls import reverse


# class AdminRedirectMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == reverse("admin:index"):
#             return redirect("login:loginapps")
#         response = self.get_response(request)
#         return response
