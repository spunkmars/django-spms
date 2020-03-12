# coding=utf-8


"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponse
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from django.conf import settings

from django.views.static import serve

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
SITE_NAME = getattr(settings, 'SITE_NAME')

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import include, url  # For django versions before 2.0

yasg_schema_view = get_schema_view(
    openapi.Info(
        # title='%s Snippets-API DOCS' % settings.SITE_NAME,
        title='Snippets-API DOCS',
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view = get_swagger_view(title='%s API DOCS' % SITE_NAME)


def health_view(request):
    return HttpResponse('')


urlpatterns = [
    url(r'^$', lambda x: HttpResponseRedirect('/index/')),
    url(r'^index/$', lambda x: HttpResponseRedirect(reverse('quickstart:index')), name='site_index'),
    # url(r'^index/$', lambda x: HttpResponseRedirect('/health/'), name='site_index'),
    url(r'^cas/', include('mama_cas.urls')),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),  # api普通验证
    url(r'^api/', include(('appxs.api.urls', 'api'), namespace='api')),  # DRF api入口
    url(r'^accounts/', include(('appxs.account.urls', 'account'), namespace='account')),
    url(r'^admin/', admin.site.urls),
    url(r'^asset/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),  # 静态文件
    url(r'^commonx/', include('appxs.commonx.urls', namespace='commonx')),
    url(r'^health/', health_view),  # 用于监测此应用是否存活
    url(r'^quickstart/', include('appxs.quickstart.urls', namespace='quickstart')),

]

# if settings.DEBUG:
if True:
    urlpatterns += [
        url(r'^api-docs/', include_docs_urls(title='%s API DOCS' % SITE_NAME)),
        url(r'^swagger(?P<format>\.json|\.yaml)$', yasg_schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^swagger/$', yasg_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^redoc/$', yasg_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        # url(r'^docs1/', schema_view, name='docs1'),
        # url(r'^docs2/', include('rest_framework_docs.urls')),
    ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                      url(r'^admin/uwsgi/', include('django_uwsgi.urls')),
                  ] + urlpatterns
