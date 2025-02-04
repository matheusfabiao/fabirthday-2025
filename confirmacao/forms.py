from django import forms
from .models import ConfirmacaoPresenca


class ConfirmacaoPresencaForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ConfirmacaoPresenca
        fields = [
            'nome',
            'email',
            'acompanhante',
            'email_acompanhante',
            'mensagem',
            'confirmado',
        ]
        widgets = {
            'nome': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Seu nome'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Seu e-mail'}
            ),
            'acompanhante': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nome do acompanhante (opcional)',
                }
            ),
            'email_acompanhante': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'E-mail do acompanhante (opcional)',
                }
            ),
            'mensagem': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Deixe uma mensagem (opcional)',
                }
            ),
            'confirmado': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
        labels = {
            'email': 'E-mail',
            'email_acompanhante': 'E-mail do acompanhante',
            'confirmado': 'Confirmo minha presença',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].required = True
        self.fields['email'].required = True
        self.fields['confirmado'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ConfirmacaoPresenca.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Este e-mail já foi usado para confirmar presença.'
            )
        return email

    def clean_honeypot(self):
        if self.cleaned_data['honeypot']:
            raise forms.ValidationError('Erro de validação. Tente novamente.')
        return self.cleaned_data['honeypot']
