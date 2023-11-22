from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser, user_registrated, Application, Category


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Повторите пароль еще раз')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    consent = forms.BooleanField(label='Согласие на обработку персональных данных', widget=forms.CheckboxInput, )

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введённые пароли не совпадают!', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        user_registrated.send(UserRegisterForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('full_name', 'username', 'email', 'password1', 'password2')


class ApplicationForm(forms.ModelForm):
    title = forms.CharField(label='Название', widget=forms.TextInput)
    description = forms.CharField(label="Описание", help_text="Введите сюда описание вашей заяки",
                                  widget=forms.Textarea())

    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']


class ApplicationStatusChangeForm(forms.ModelForm):
    class Meta:
        model = Application
        comment = forms.CharField(label="Комментарий", help_text="Введите сюда комментарий для смены статуса",
                                  widget=forms.Textarea())
        fields = ['status', 'comment', 'completed_image']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('comment')
        completed_image = cleaned_data.get('completed_image')

        if status == 'B' and not comment:
            self.add_error('comment', "Требуется комментарий для смены статуса.")

        if status == 'C' and not completed_image:
            self.add_error('completed_image', "Требуется загрузка изображения для смены статуса.")

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
