#!/usr/bin/python3

import webapp


class URLShortener(webapp.webApp):
    resource = {}
    mirrors = {}

    NotFound = ["404 Not Found",
                "<html><body><h1>404 Not Found</h1></body></html>"]

    def URLcomplete(self, url):

        if "http://" in url or "https://" in url:
            return url
        else:
            return ("http://" + url)

    def makelist(self):
        mirrorslist = ""
        for mirror, url in self.mirrors.items():
            line = ("Original: <a href=" + url + ">" + url +
                    "</a> => Mirror: <a href=" +
                    mirror + ">" + mirror + "</a></br>")
            mirrorslist += line
        return mirrorslist

    def parse(self, request):
        request = str(request, 'utf8')
        input = request.split()[0:2]
        if "URL=" in request:
            input.append(request.split('=')[-1])
        print("input: ", input)
        return input

    def process(self, parsedRequest):

        if parsedRequest[0] == "GET":
            if parsedRequest[1] == "/":
                mirrorslist = self.makelist()
                print("mirrorslist: ", mirrorslist)
                OK = ("<html><head><meta charset='utf-8'><h1 align='center'>"
                      "X-Serv-18.1-Practica1</h1></head><body>"
                      "<form method='POST'><p align='center'>URL a acortar: "
                      "<input type='text' name='URL' ></p></form>"
                      "Previous URLs:<br>" + mirrorslist + "</body></html>")
                return ("200 OK", OK)
            elif parsedRequest[1] in self.mirrors.keys():
                RedirURL = self.URLcomplete(self.mirrors[parsedRequest[1]])
                print(RedirURL)
                Redirect = ("<html><body>"
                            "<meta http-equiv='refresh' content=0;url=" +
                            RedirURL + "></p></body></html>")
                print(Redirect)
                return ("300 Redirect", Redirect)
            else:
                return (self.NotFound)
        elif parsedRequest[0] == "POST":
            if parsedRequest[2] == "":
                return (self.NotFound)
            url = self.URLcomplete(parsedRequest[2])
            if url not in self.resource:
                key = "/" + str(len(self.mirrors))
                self.mirrors[key] = url
                self.resource[url] = key
            mirror = "http://localhost:1234" + self.resource[url]
            htmlBody = ("<html><body>Url a acortar = <a href=" + url +
                        ">" + url + "</a><br>Url Acortada = <a href=" +
                        mirror + ">" + mirror + "</a></br></body></html>")
            return ("200 OK", htmlBody)
        else:
            return (self.NotFound)
if __name__ == "__main__":
    testWebApp = URLShortener("localhost", 1234)
