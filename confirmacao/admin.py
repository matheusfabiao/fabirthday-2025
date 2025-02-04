from django.contrib import admin
from .models import ConfirmacaoPresenca


@admin.register(ConfirmacaoPresenca)
class ConfirmacaoPresencaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'email',
        'confirmado',
        'mensagem_preview',
        'criado_em',
    )
    list_filter = ('confirmado', 'criado_em')
    search_fields = ('nome', 'email')
    ordering = ('-criado_em',)
    actions = ['marcar_como_nao_confirmado']

    def mensagem_preview(self, obj):
        return (obj.mensagem[:30] + '...') if obj.mensagem else '-'

    mensagem_preview.short_description = 'Mensagem'

    @admin.action(description='Marcar como não confirmado')
    def marcar_como_nao_confirmado(self, request, queryset):
        queryset.update(confirmado=False)
