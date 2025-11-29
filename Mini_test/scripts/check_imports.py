try:
    from usuarios.auth import CustomTokenObtainPairView
    from rest_framework_simplejwt.views import TokenRefreshView
    print('IMPORTS_OK')
except Exception as e:
    print('IMPORT_ERROR', e)
