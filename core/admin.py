from django.contrib import admin
from .models import Contactos, Register
from django.utils.html import format_html
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Register your models here.
# admin.site.register(Contactos)
# admin.site.register(Register)

# Personalización para el modelo Register
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'cellphone', 'user_active', 'user_admin', 'reset_token_expiration', 'acciones_personalizadas')
    list_filter = ('user_active', 'user_admin', 'reset_token_expiration')
    search_fields = ('name', 'last_name', 'email', 'cellphone')
    ordering = ('-id',)
    list_per_page = 20
    readonly_fields = ('reset_token_expiration',)

    #Agrega las acciones personalizadas
    actions = ['activar_usuarios', 'desactivar_usuarios', 'eliminar_usuarios']

    #Acción: Activar usuarios
    @admin.action(description="✅ Activar usuarios seleccionados")
    def activar_usuarios(self, request, queryset):
        queryset.update(user_active=True)
        self.message_user(request, f"{queryset.count()} usuario(s) activado(s).")

    #Acción: Desactivar usuarios
    @admin.action(description="🚫 Desactivar usuarios seleccionados")
    def desactivar_usuarios(self, request, queryset):
        queryset.update(user_active=False)
        self.message_user(request, f"{queryset.count()} usuario(s) desactivado(s).")

    #Acción: Eliminar usuarios
    @admin.action(description="🗑️ Eliminar usuarios seleccionados")
    def eliminar_usuarios(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} usuario(s) eliminado(s).")

    #Botones de acciones personalizadas en cada registro
    def acciones_personalizadas(self, obj):
        if obj.user_active:
            return format_html(
                '<a class="button" href="{}" style="color: red;">Desactivar</a>',
                f"/admin/core/register/{obj.id}/change/?user_active=0"
            )
        else:
            return format_html(
                '<a class="button" href="{}" style="color: green;">Activar</a>',
                f"/admin/core/register/{obj.id}/change/?user_active=1"
            )
    
    acciones_personalizadas.short_description = "Acción rápida"


#Personalización para el modelo Contactos -LGS
@admin.register(Contactos)
class ContactosAdmin(admin.ModelAdmin):
    #Campos visibles en la lista -LGS
    list_display = ('name_contact', 'email_contact', 'phone_contact', 'topic_contact', 'date_contact', 'seen_contact', 'acciones_personalizadas')
    list_filter = ('seen_contact', 'topic_contact', 'date_contact')  # Filtros por visto/no visto
    search_fields = ('name_contact', 'lastname_contact', 'email_contact', 'phone_contact')
    ordering = ('-date_contact',)
    list_per_page = 20

    #Agrega las acciones personalizadas -LGS
    actions = ['marcar_como_visto', 'marcar_como_no_visto']

    # Acción: Marcar como visto
    @admin.action(description="👁️ Marcar como visto")
    def marcar_como_visto(self, request, queryset):
        queryset.update(seen_contact=True)
        self.message_user(request, f"{queryset.count()} contacto(s) marcado(s) como visto.")

    #Acción: Marcar como no visto -LGS
    @admin.action(description="🚫 Marcar como no visto")
    def marcar_como_no_visto(self, request, queryset):
        queryset.update(seen_contact=False)
        self.message_user(request, f"{queryset.count()} contacto(s) marcado(s) como no visto.")

    #Botones rápidos de acción individual -LGS
    def acciones_personalizadas(self, obj):
        if obj.seen_contact:
            return format_html(
                '<a class="button" href="{}" style="color: red;">Marcar como no visto</a>',
                f"/admin/core/contactos/{obj.id}/change/?visto=0"
            )
        else:
            return format_html(
                '<a class="button" href="{}" style="color: green;">Marcar como visto</a>',
                f"/admin/core/contactos/{obj.id}/change/?visto=1"
            )
    
    acciones_personalizadas.short_description = "Acción rápida"

