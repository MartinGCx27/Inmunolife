from django.contrib import admin
from .models import Contactos, Register
from django.utils.html import format_html

# Register your models here.
# admin.site.register(Contactos)
# admin.site.register(Register)

#Personalización para el modelo Register -LGS
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    #`list_display`: Define las columnas que se mostrarán en la lista del admin -LGS
    list_display = ('name', 'last_name', 'email', 'cellphone', 'user_active', 'user_admin', 'reset_token_expiration', 'acciones_personalizadas')

    #`list_filter`: Agrega filtros laterales para facilitar la búsqueda por campos específicos -LGS
    list_filter = ('user_active', 'user_admin', 'reset_token_expiration')

    #`search_fields`: Habilita la búsqueda por los campos indicados -LGS
    search_fields = ('name', 'last_name', 'email', 'cellphone')

    #`ordering`: Ordena la lista de forma descendente por el campo `id` (el signo `-` indica descendente) -LGS
    ordering = ('-id',)

    #`list_per_page`: Define la cantidad de registros visibles por página -LGS
    list_per_page = 20

    #`readonly_fields`: Hace que el campo `reset_token_expiration` sea solo de lectura -LGS
    readonly_fields = ('reset_token_expiration',)

    #Agrega las acciones personalizadas que aparecen como opciones rápidas en el admin -LGS
    actions = ['activar_usuarios', 'desactivar_usuarios', 'eliminar_usuarios']  # Mantengo una sola acción de eliminar

    # Acción personalizada para activar usuarios -LGS
    @admin.action(description="✅ Activar usuarios seleccionados")
    def activar_usuarios(self, request, queryset):
        queryset.update(user_active=True)  # Activa los usuarios seleccionados
        self.message_user(request, f"{queryset.count()} usuario(s) activado(s).")

    # Acción personalizada para desactivar usuarios -LGS
    @admin.action(description="🚫 Desactivar usuarios seleccionados")
    def desactivar_usuarios(self, request, queryset):
        queryset.update(user_active=False)  # Desactiva los usuarios seleccionados -LGS
        self.message_user(request, f"{queryset.count()} usuario(s) desactivado(s).")

    # ✅ Única acción personalizada para eliminar usuarios seleccionados -LGS
    @admin.action(description="🗑️ Eliminar usuarios seleccionados")
    def eliminar_usuarios(self, request, queryset):
        count = queryset.count()  # Obtiene la cantidad de usuarios seleccionados -LGS
        queryset.delete()         # Elimina los usuarios seleccionados -LGS
        self.message_user(request, f"{count} usuario(s) eliminado(s).")

    # Botones de acciones personalizadas rápidas en cada registro -LGS
    def acciones_personalizadas(self, obj):
        # Botón para eliminar individualmente -LGS
        return format_html(
            '<a class="button" href="{}" style="color: red;" '
            'onclick="return confirm(\'¿Estás seguro de que deseas eliminar este usuario?\')">Eliminar</a>',
            f"/admin/core/register/{obj.id}/delete/"
        )

    # Cambia el nombre del campo personalizado en la interfaz del admin -LGS
    acciones_personalizadas.short_description = "Acción rápida"


#Personalización para el modelo Contactos -LGS
@admin.register(Contactos)
class ContactosAdmin(admin.ModelAdmin):

    #`list_display`: Muestra las columnas especificadas en la lista -LGS
    list_display = ('name_contact', 'email_contact', 'phone_contact', 'topic_contact', 'date_contact', 'seen_contact', 'acciones_personalizadas')

    #`list_filter`: Filtros para buscar por contactos vistos o no vistos, tema y fecha -LGS
    list_filter = ('seen_contact', 'topic_contact', 'date_contact')  #Filtros por visto/no visto -LGS

    #`search_fields`: Habilita la búsqueda por nombre, apellido, email o teléfono -LGS
    search_fields = ('name_contact', 'lastname_contact', 'email_contact', 'phone_contact')

    #`ordering`: Ordena por fecha de contacto, de forma descendente -LGS
    ordering = ('-date_contact',)

    list_per_page = 20
    #`list_per_page`: Muestra 20 registros por página -LGS

    #Agrega las acciones personalizadas para el modelo Contactos -LGS
    actions = ['marcar_como_visto', 'marcar_como_no_visto']
    #`actions`: Lista de métodos de acción que aparecerán en la vista del admin -LGS

    #Acción personalizada para marcar como visto -LGS
    @admin.action(description="👁️ Marcar como visto")
    def marcar_como_visto(self, request, queryset):
        queryset.update(seen_contact=True)  #Marca como visto -LGS
        self.message_user(request, f"{queryset.count()} contacto(s) marcado(s) como visto.")
    #Actualiza todos los registros seleccionados a `seen_contact=True`.

    #Acción personalizada para marcar como no visto -LGS
    @admin.action(description="🚫 Marcar como no visto")
    def marcar_como_no_visto(self, request, queryset):
        queryset.update(seen_contact=False)  # Marca como no visto -LGS
        self.message_user(request, f"{queryset.count()} contacto(s) marcado(s) como no visto.")
    #Actualiza todos los registros seleccionados a `seen_contact=False` -LGS

    #Botones de acción rápida para cada registro -LGS
    def acciones_personalizadas(self, obj):
        if obj.seen_contact:
            # Si ya está visto, muestra el botón para marcar como no visto
            return format_html(
                '<a class="button" href="{}" style="color: red;">Marcar como no visto</a>',
                f"/admin/core/contactos/{obj.id}/change/?visto=0"
            )
        else:
            #Si no está visto, muestra el botón para marcar como visto
            return format_html(
                '<a class="button" href="{}" style="color: green;">Marcar como visto</a>',
                f"/admin/core/contactos/{obj.id}/change/?visto=1"
            )

    #Cambia el nombre del campo personalizado en la interfaz del admin -LGS  
    acciones_personalizadas.short_description = "Acción rápida"

