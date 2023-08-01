from rest_framework import serializers


class HtmlCssSerializer(serializers.Serializer):
    html_code = serializers.CharField()
    css_code = serializers.CharField()
