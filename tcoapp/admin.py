from django.contrib import admin

from .models import userinfo, Architecture, FeatureArchitecture,ArchitectureType,Chat

class userinfoAdmin(admin.ModelAdmin):
  	list_display = ('user_id', 'phone', 'created_at','updated_at')
  	model = userinfo

class ArchitectureAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("architecture_img",)}
    list_display = ('id','architecture_img', 'architecture_name','archtype')
    # search_fields = ('name', )

class FeatureArchitectureAdmin(admin.ModelAdmin):
    # prepopulated_fields = {"slug": ("architecture_img",)}
    list_display = ('architecture_id', 'feature_img',)
    # search_fields = ('name', )
class ArchitectureTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'archtype',)

class ChatAdmin(admin.ModelAdmin):
	list_display = ('id', 'user_id','usermsg','botmsg','created_at')


admin.site.register(userinfo,userinfoAdmin)
admin.site.register(Architecture, ArchitectureAdmin)
admin.site.register(FeatureArchitecture, FeatureArchitectureAdmin)
admin.site.register(ArchitectureType, ArchitectureTypeAdmin	)
admin.site.register(Chat,ChatAdmin	)