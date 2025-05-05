from django.urls import path
from main.views import landing_page, voting_page, thank_you


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', landing_page, name='landing_page'),           # Entry point: enter student ID
    path('vote/', voting_page, name='voting_page'),        # Voting interface: vote for candidates
    path('thank-you/', thank_you, name='thank_you'),       # Final thank-you page after voting
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)