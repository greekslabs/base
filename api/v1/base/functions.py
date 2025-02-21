# Generate serializer errors in readable format
def generate_serializer_errors(args):
    message = ""
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        message += "%s : %s | " % (key, error_message)
    return message[:-3]

def create_response_data(statuscode, title, data, errors, message):
    return {
        'statuscode': statuscode,
        'title': title,
        'data': data,
        'errors': errors,
        'message': message,
    }