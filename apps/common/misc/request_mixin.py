import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class AuthRequestMixin:
    base_uri: str = ""

    def auth_post(self, client: APIClient, admin=None, body=None, custom_headers=None,
                  uri=None, params=None, accept_lang="pt-BR"):
        headers = custom_headers or self._get_headers(
            admin, accept_lang=accept_lang)
        body = self._handle_body(body)
        url = self._get_url(uri or self.base_uri, params)
        return client.post(url, body, content_type="application/json;charset=UTF-8", **headers)

    def auth_patch(self, client: APIClient, obj=None, admin=None, body=None, custom_headers=None,
                   uri=None, accept_lang="pt-BR"):
        headers = custom_headers or self._get_headers(
            admin, accept_lang=accept_lang)
        url = uri or (f"{self.base_uri}{obj.id}/" if obj else self.base_uri)
        body = self._handle_body(body)
        return client.patch(url, body, content_type="application/json;charset=UTF-8", **headers)

    def auth_put(self, client: APIClient, obj, admin=None, body=None, custom_headers=None,
                 uri=None, accept_lang="pt-BR"):
        headers = custom_headers or self._get_headers(
            admin, accept_lang=accept_lang)
        url = uri or f"{self.base_uri}{obj.id}/"
        body = self._handle_body(body)
        return client.put(url, body, content_type="application/json;charset=UTF-8", **headers)

    def auth_delete(self, client: APIClient, obj, admin=None, params=None, custom_headers=None,
                    uri=None, body=None, accept_lang="pt-BR"):
        headers = custom_headers or self._get_headers(
            admin, accept_lang=accept_lang)
        url = self._get_url(
            uri or (f"{self.base_uri}{obj.id}/" if obj else self.base_uri), params)
        if body is not None:
            body = self._handle_body(body)
            return client.delete(url, data=body, content_type="application/json;charset=UTF-8", **headers)
        return client.delete(url, content_type="application/json;charset=UTF-8", **headers)

    def auth_get(self, client: APIClient, admin=None, obj=None, params=None, custom_headers=None,
                 uri=None, accept_lang="pt-BR"):
        headers = custom_headers or self._get_headers(
            admin, accept_lang=accept_lang)
        url = self._get_url(
            uri or (f"{self.base_uri}{obj.id}/" if obj else self.base_uri), params)
        return client.get(url, content_type="application/json;charset=UTF-8", **headers)

    def _get_headers(self, user=None, accept_lang="pt-BR"):
        if not user:
            return {"HTTP_ACCEPT_LANGUAGE": accept_lang}
        token = str(RefreshToken.for_user(user).access_token)
        return {
            "HTTP_AUTHORIZATION": f"Bearer {token}",
            "HTTP_ACCEPT_LANGUAGE": accept_lang,
        }

    def _handle_body(self, body):
        if isinstance(body, (dict, list)):
            return json.dumps(body, sort_keys=True, indent=1, cls=DjangoJSONEncoder)
        return body

    def _get_url(self, uri, params):
        if not params:
            return uri
        import urllib.parse
        return f"{uri}?{urllib.parse.urlencode(params)}"
