from utils import get_characters

def generar_estadisticas():
    personajes = get_characters()

    estadisticas = {}

    for personaje in personajes:
        autor = personaje['autor']
        libro = personaje['libro']
        
        if autor not in estadisticas:
            estadisticas[autor] = {}

        if libro not in estadisticas[autor]:
            estadisticas[autor][libro] = 0

        estadisticas[autor][libro] += 1

    print("📊 Estadísticas\n")

    total_autores = 0
    total_general = 0

    for autor, libros in estadisticas.items():
        total_por_autor = 0
        print(f"🖋️ {autor}")
        total_autores += 1

        for libro, cantidad in libros.items():
            print(f"   📖 {libro}: {cantidad} personajes")
            total_por_autor += cantidad

        print(f"   👥 Total personajes: {total_por_autor}\n")
        total_general += total_por_autor

    print("\nTotal\n")
    print(f"🖋️ Autores: {total_autores}")
    print(f"👥 Personajes: {total_general}")

generar_estadisticas()