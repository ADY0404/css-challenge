from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from homepage import views
from users.views import login_view, signup_view

# Custom Django Admin Site Branding & Layout
admin.site.site_header = "Computer Science Society Administration"
admin.site.site_title = "CSS Admin Portal"
admin.site.index_title = "Society Management & Operations Portal"

from homepage.admin_site import setup_custom_admin_dashboard
setup_custom_admin_dashboard(admin.site)

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/com.png', permanent=True)),
    path('adcs/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('', views.home, name='home'),

    # Community
    path('community/', views.community, name='community'),
    path('community/propose/', views.propose_community_channel, name='propose_community_channel'),
    path('community2/', views.community2, name='community2'),
    path('community/channel/<slug:channel>/', views.community2, name='community_channel'),
    path('community/api/messages/', views.community_messages_api, name='community_messages_api'),

    # Challenges & Leaderboard
    path('challenges/', views.challenge_list, name='challenge'),
    path('challenges/<slug:slug>/', views.challenge_detail, name='challenge_detail'),
    path('challenges/submission/<int:sub_id>/upvote/', views.upvote_submission, name='upvote_submission'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # Global Search
    path('search/', views.search, name='search'),

    # Blog / Journal
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.article_detail, name='article_detail'),

    # Internships & Careers
    path('internships/', views.internships_list, name='internships'),
    path('internships/share/', views.share_opportunity, name='share_opportunity'),

    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Informational Pages & Programs
    path('guidelines/', views.info_page, {'page': 'guidelines'}, name='guidelines'),
    path('programs/', views.info_page, {'page': 'programs'}, name='programs'),
    path('programs/clinic/', views.clinic_dates, name='pc_clinic'),
    path('clinic/', views.clinic_dates, name='clinic_dates'),
    path('terms/', views.info_page, {'page': 'terms'}, name='terms'),
    path('privacy/', views.info_page, {'page': 'privacy'}, name='privacy'),

    # Legacy / exploratory route masks
    path('home/', RedirectView.as_view(url='/', permanent=False)),
    path('home/users/', RedirectView.as_view(pattern_name='profile', permanent=False)),
    path('users/', RedirectView.as_view(pattern_name='profile', permanent=False)),

    # App includes
    path('executives/', include('executives.urls', namespace='executives')),
    path('activities/', include('activities.urls', namespace='act')),
    path('', include('users.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
