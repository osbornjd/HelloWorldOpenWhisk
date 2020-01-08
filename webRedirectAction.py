# This FaaS demonstrates how you can create a function which acts as
# a decision point to trigger other FaaS. This is a hello world
# example, which takes in a name as an argument and then, depending
# on the length of the name, calls either the hello or goodbye FaaS
# web URLs with the name parameter

def main(args):

    name = args.get("name","stranger")

    # Make some dummy criteria as a decision, e.g. whether or not the
    # name is longer than 5 characters
    if(len(name) > 5):
        # return a dictionary with the location URL and an http status
        # code
        return {
            "headers": {"location": "https://192.168.33.16/api/v1/web/guest/pythondemo/hello?name=" + name},
            "statusCode": "302"
        }
    else:
        return {
            "headers": {"location": "https://192.168.33.16/api/v1/web/guest/pythondemo/goodbye?name=" + name},
            "statusCode": "302"
        }

