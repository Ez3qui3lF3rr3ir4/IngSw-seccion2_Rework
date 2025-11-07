import os
import sys
import random
import django
from faker import Faker
from django.contrib.auth.hashers import make_password

# === ⚙️ CONFIGURACIÓN DE DJANGO ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SystemScoutsApi.ApiCoreScouts')
django.setup()
0
# === 📦 IMPORTAR MODELOS DESPUÉS DE CONFIGURAR DJANGO ===
from SystemScoutsApi.ApiCoreScouts.models import Usuario, Perfil, Aplicacion, Perfil_Aplicacion


def poblar_datos_masivos(num_perfiles=5, num_apps=10, num_usuarios=50):
    fake = Faker('es_CL')  # Datos más realistas para Chile
    print("🚀 Iniciando poblamiento masivo de base de datos...")

    # --- 1️⃣ Crear perfiles ---
    perfiles = []
    for _ in range(num_perfiles):
        descripcion = fake.job()[:50]
        perfil, _ = Perfil.objects.get_or_create(
            PEL_DESCRIPCION=descripcion,
            defaults={"PEL_VIGENTE": fake.boolean(chance_of_getting_true=85)}
        )
        perfiles.append(perfil)
    print(f"✅ {len(perfiles)} perfiles creados.")

    # --- 2️⃣ Crear aplicaciones ---
    aplicaciones = []
    for _ in range(num_apps):
        descripcion = fake.catch_phrase()[:50]
        app, _ = Aplicacion.objects.get_or_create(
            APL_DESCRIPCION=descripcion,
            defaults={"APL_VIGENTE": fake.boolean(chance_of_getting_true=90)}
        )
        aplicaciones.append(app)
    print(f"✅ {len(aplicaciones)} aplicaciones creadas.")

    # --- 3️⃣ Crear permisos Perfil ↔ Aplicación ---
    total_permisos = 0
    for perfil in perfiles:
        apps_random = random.sample(aplicaciones, k=random.randint(2, len(aplicaciones)))
        for app in apps_random:
            Perfil_Aplicacion.objects.get_or_create(
                PEL_ID=perfil,
                APL_ID=app,
                defaults={
                    "PEA_INGRESAR": fake.boolean(chance_of_getting_true=60),
                    "PEA_MODIFICAR": fake.boolean(chance_of_getting_true=50),
                    "PEA_ELIMINAR": fake.boolean(chance_of_getting_true=40),
                    "PEA_CONSULTAR": True,
                },
            )
            total_permisos += 1
    print(f"🔐 {total_permisos} permisos generados entre perfiles y aplicaciones.")

    # --- 4️⃣ Crear usuarios ---
    usuarios_creados = 0
    for _ in range(num_usuarios):
        perfil = random.choice(perfiles)
        username = fake.user_name()[:100]
        ruta_foto = f"/media/usuarios/{username}.jpg"
        password = make_password(fake.password(length=10))

        Usuario.objects.get_or_create(
            USU_USERNAME=username,
            defaults={
                "PEL_ID": perfil,
                "USU_PASSWORD": password,
                "USU_RUTA_FOTO": ruta_foto,
                "USU_VIGENTE": fake.boolean(chance_of_getting_true=95),
            }
        )
        usuarios_creados += 1

    print(f"👤 {usuarios_creados} usuarios creados correctamente.")
    print("🎉 Poblamiento masivo completado con éxito.")


if __name__ == "__main__":
    poblar_datos_masivos(num_perfiles=10, num_apps=20, num_usuarios=200)
