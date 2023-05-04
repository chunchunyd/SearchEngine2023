from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Court)
admin.site.register(Procuratorate)
admin.site.register(Party)
admin.site.register(Agent)
admin.site.register(LawReference)
admin.site.register(Judge)
admin.site.register(LawDocument)
admin.site.register(Judgment)
admin.site.register(Prosecution)
admin.site.register(DocAgentParty)

