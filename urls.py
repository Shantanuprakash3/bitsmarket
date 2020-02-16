from django.conf.urls import patterns, include, url
from BitsMarket import views, settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PS1Bajaj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main_view),
    url(r'^login/', views.login_view),
    url(r'^sell/', views.sell),
    url(r'^loggedin/', views.logged_in_view),
    url(r'^signUP/', views.signup_view),
    url(r'^viewSelf/', views.view_self),
    url(r'^editSelf/', views.edit_self),
    url(r'^addProduct/', views.product_uploader),
    url(r'^user/products', views.view_user_products),
    url(r'^deleteProduct/', views.remove_product),
    url(r'^viewProduct/', views.view_product),
    url(r'^logout/', views.logout),
    url(r'^sell/', views.logout),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns2 = patterns('',
    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),)
urlpatterns += urlpatterns2