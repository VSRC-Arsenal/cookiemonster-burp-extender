from burp import IBurpExtender, IHttpListener,IExtensionHelpers

cookiemonster_path = "./cookiemonster" # path cookie monster header

class BurpExtender(IBurpExtender,IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.listCookie = []
        self.lenResult = len(open("./output.txt",'r').read())
        callbacks.setExtensionName("CookieMonster Extender")
        callbacks.registerHttpListener(self)
        print("Load successful!\nAuthor: m0nsieur")
        return

    def getResponseHeadersAndRequestURL(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders() or '')

        httpService = content.getHttpService()
        request = content.getRequest()
        request_data = self._helpers.analyzeRequest(httpService,request)
        
        return headers, request_data.getUrl()

    def processHttpMessage(self, tool, is_request, content):
        if is_request:
            return
        headers, fullURL = self.getResponseHeadersAndRequestURL(content)
        fullURL = str(fullURL).split("?")[0]
        
        # free list cookie
        if len(self.listCookie) > 100000000:
            self.listCookie = []

        cookieMap = self.buildCookieMap(headers, fullURL)

        for k in cookieMap:
            if CheckExpressCookie(cookieMap,k):
                v = k.split("||")[1] + "=" + cookieMap[k] + "^" + cookieMap[k + ".sig"]
            else:
                v = cookieMap[k]
            if v not in self.listCookie:
                self.RunCookieMonster(v,fullURL)
                self.listCookie.append(v)     

    def buildCookieMap(self, headers, fullURL):
        cookieMap = {}
        for header in headers:
            headerKeyValue = header.split(": ")
            if len(headerKeyValue) >= 2:
                key = headerKeyValue[0]
                value = "".join(headerKeyValue[1:])
                if key.lower() == "set-cookie":
                    cookieStr = value.split(";")[0]
                    cookieName = fullURL + "||" +cookieStr.split("=")[0]
                    cookieValue = cookieStr.split("=")[1]
                    cookieMap[cookieName] = cookieValue
        
        return cookieMap

    def RunCookieMonster(self, cookie,fullURL):
        import os     
        cmd = "{} -cookie {}".format(cookiemonster_path,cookie)

        if os.system(cmd) != 0:
            cmd = "wsl {} -cookie \"{}\"".format(cookiemonster_path,cookie)
            os.system(cmd)

        output = open("./output.txt",'r').read()
        if len(output) > self.lenResult:
            self._callbacks.issueAlert("Found new weak key at: {}. Check log output.".format(fullURL))
            print("Found new weak key at: {}. Cookie is: {}".format(fullURL,cookie))
            
            self.lenResult = len(output)
        

        


def CheckExpressCookie(cookieMap,k):
    sigCookie = k + ".sig"
    if sigCookie in cookieMap:
        return True

    return False