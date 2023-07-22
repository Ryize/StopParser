from rest_framework import serializers


class OnlyHtmlSerializer(serializers.Serializer):
    html_code = serializers.CharField()


class OnlyCssSafe(serializers.Serializer):
    css_code = serializers.CharField()


class HtmlCssSafe(serializers.Serializer):
    html_code = serializers.CharField()
    css_code = serializers.CharField()
