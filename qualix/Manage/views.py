import urllib, ssl, json
from django.shortcuts import render
from django.views.generic.base import ContextMixin, TemplateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views import View
from django.conf import settings
# Create your views here.


class MyBaseMixin(ContextMixin):

    def jsonrpc(self,url='https://slb.medv.ru/api/v2/', method="auth.check", params={}):
        js = {"jsonrpc": "2.0", "method": method, 'params': params, "id": 1}
        params = json.dumps(js).encode('utf8')
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        new_crt = open('n.crt', 'w')
        new_key = open('n.key', 'w')
        new_crt.write(settings.CRT)
        new_key.write(settings.KEY)
        new_key.close()
        new_crt.close()

        ssl_context.load_cert_chain('n.crt', keyfile='n.key')
        req = urllib.request.Request(
            url,
            data=params,
            headers={'content-type': 'application/json'}
        )
        response = urllib.request.urlopen(req, context=ssl_context)
        resp = json.loads(response.read().decode('utf8'))

        if 'error' in resp:
            result = resp['error']
        elif 'result' in resp:
            result = resp['result']
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthView(View, MyBaseMixin):
    def get(self,request):
        j = self.jsonrpc()
        return HttpResponse(';)')
