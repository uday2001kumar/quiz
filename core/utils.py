from rest_framework.response import Response
import random 
from rest_framework.views import exception_handler

def success_response(message="Success", data=None, status_code=200):
    return Response(
        {
            "message": message,
            "data": data
        },
        status=status_code
    )

def error_response(message="Error", errors=None, status_code=400):
    return Response(
        {
            "message": message,
            "errors": errors
        },
        status=status_code
    )




def generate_username(email):
    # take part before @
    base = email.split("@")[0]

    # clean special characters
    base = "".join([c for c in base if c.isalnum()])

    if not base:
        base = "user"

    random_number = random.randint(1000, 9999)

    return f"{base}_{random_number}"




from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    print("🔥 Exception:", exc)
    print("📦 Raw response:", getattr(response, "data", None))

    if response is not None:

        data = response.data
        first_error = "Something went wrong!"

        try:
            if isinstance(data, dict):

                for field, errors in data.items():

                    # DRF list of errors
                    if isinstance(errors, list) and errors:
                        first_error = str(errors[0])
                        break

                    # single ErrorDetail
                    elif isinstance(errors, ErrorDetail):
                        first_error = str(errors)
                        break

            elif isinstance(data, list) and data:
                first_error = str(data[0])

            elif isinstance(data, str):
                first_error = data

        except Exception as e:
            print("❌ Handler error:", e)
            first_error = "Invalid data!"

        response.data = {
            "message": "Something went wrong!",
            "errors": first_error
        }

        response.status_code = 400

    return response