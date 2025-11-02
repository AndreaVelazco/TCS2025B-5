from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Extiende TokenObtainPairSerializer para usar el campo `correo`.

    Esto permite que SimpleJWT reciba JSON con {'correo','password'} y
    devuelva access+refresh tokens manteniendo la lógica de generación
    y los claims estándar de SimpleJWT.
    """

    # Indicar que el campo a usar como username es 'correo'
    username_field = 'correo'

    # Accept 'usuario' in the incoming payload as an alias for the username_field
    usuario = serializers.CharField(write_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the serializer does not require the username_field (correo)
        # because we accept 'usuario' as input. The parent class created a field
        # named after self.username_field (correo); make it optional here.
        if self.username_field in self.fields:
            self.fields[self.username_field].required = False

    def validate(self, attrs):
        # Map 'usuario' or 'correo' into the expected username_field before
        # delegating to the parent implementation.
        if 'usuario' in attrs and attrs.get('usuario'):
            attrs[self.username_field] = attrs.get('usuario')
        elif 'correo' in attrs and attrs.get('correo'):
            attrs[self.username_field] = attrs.get('correo')

        return super().validate(attrs)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
