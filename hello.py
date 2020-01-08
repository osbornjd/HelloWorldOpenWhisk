# This is a hello world FaaS. It takes a name as an
# argument, builds a hello message, and returns an
# html webpage. It can also take a separator as
# an argument and be chained together with the
# default sort and split FaaS provided by OpenWhisk

def main(args):
    name = args.get("name","stranger")
    msg = "Hello " + name + ", this is the python demo"
    sep = args.get("separator","\n");
    return {
        "body": "<html><body><h3>" + msg + "</h3></body></html>",
        "separator": sep,
        "payload": msg
    }
