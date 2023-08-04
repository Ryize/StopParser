from django.http import JsonResponse
from rest_framework.generics import GenericAPIView

from api.encrypt import CodeEncrypt
from api.serializers import HtmlCssSerializer


class HtmlCssViewSet(GenericAPIView):
    """
    Позволяет изменить классы в HTML/CSS.
    Не влияет на работоспособность получившейся верстки.
    """
    def get_serializer(self, *args, **kwargs):
        return HtmlCssSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        html = request.POST.get('html_code')
        css = request.POST.get('css_code')
        encrypt_html, encrypt_css = CodeEncrypt(html_code=html, css_code=css).encrypt()
        return JsonResponse(
            {
                'encrypt_html': encrypt_html,
                'encrypt_css': encrypt_css,
            }
        )
