from django.middleware.common import MiddlewareMixin
from django.shortcuts import resolve_url
from django.http import JsonResponse
from MainApp.views import test, fail


global status_list

# ++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++===

def RJR(status=False, msg=False):
    response_data = {
        "status": status if status else "Success, or not success, that is the question",
        "msg": status_list[status] + msg if status and msg else status_list[status] or msg if status or msg else "???UNDEFINED ERROR???",
    }
    return JsonResponse(response_data)

# ++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++====++===

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
#        if request.method != "POST":
#            return RJR(12)

        bearer_header = request.headers.get('Authorization')
        token = bearer_header.split(' ')[1]

        if token == "token":
            response = test(request)
        else:
            response = fail(request)

        return response





# ------------------------------------------------------------- #
#                            STATUSES                           #
# ------------------------------------------------------------- #
#   1<..>  -> Error
#   2<..>  -> Success
#   3<..>  -> Warning
#   4<..>  -> Info

status_list = {
    10: "Undefined error. ",
    11: "Node already exists. ",
    12: "Invalid request method. ",
    13: "Invalid request data. ",
    14: "Token is expired. ",
    15: "Invalid Token. ",
    16: "Request have no auth token (Bearer). ",
    # ------------------------------------------------------------- #
    20: "Undefined success. ",
    21: "Node or user was successfully created. ",
    22: "Token is Valid. ",
    23: "Data successfully changed. ",
    # ------------------------------------------------------------- #
    30: "Undefined warning. ",
    # ------------------------------------------------------------- #
    40: "Undefined info. ",
}
