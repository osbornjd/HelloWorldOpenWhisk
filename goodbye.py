
def main(args):
    name = args.get("name","stranger")
    msg = "Goodbye " + name + ", your name was too short"

    return {
"body" : "<html><body><h3>" + msg + "</h3></body></html>"
}
