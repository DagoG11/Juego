En un mundo donde la emoción y la velocidad se entrelazan, un joven corredor y su perro fiel se embarcan en una aventura llena de desafíos y sorpresas. Mientras atraviesan paisajes dinámicos de día y noche, deben sortear obstáculos, vencer alipsis y mantener el ritmo para evitar que el perro alcance al corredor.

A medida que avanzan, el ritmo del juego se intensifica, poniendo a prueba tanto la habilidad como la estrategia del jugador. Golpear cajas otorga un impulso al perro que lo persigue y saltarlas lo ralentiza, afectando el equilibrio entre la persecución y la evasión. La atmósfera cambia con el ciclo natural de día y noche cada minuto, sumergiendo al jugador en una experiencia visual cautivadora.

¿Podrás mantener la distancia suficiente para atravesar esta carrera interminable? Solo los corredores más rápidos y astutos lograrán quedarse delante y completar la fuga. ¡Prepárate para correr, saltar y desafiar a tu fiel pero incansable perseguidor en Dog Runner!

Descripción General
Dog Runner es un juego 2D de plataforma side-scrolling desarrollado en Python con Pygame. El jugador controla a un corredor que es perseguido por un perro incansable. El objetivo es esquivar obstáculos, saltar cajas y evitar ser atrapado mientras unos elementos dinámicos afectan el juego, como el ciclo día/noche y un sistema de penalizaciones y beneficios mediante cajas.

Características Principales
Movimiento lateral controlado con teclas izquierda y derecha.

Salto con tecla espacio o flecha hacia arriba.

Perro enemigo con movimiento automático y capacidad de saltar obstáculos.

Cajas con efectos desplegados cuando el jugador las golpea o las salta:

Penalizaciones de ralentización y detención por tiempo limitado.

Ciclo dinámico día y noche que cambia el fondo cada 60 segundos.

Sistema de partículas para efectos visuales (polvo, impacto).

Indicador de distancia recorrida.

Escenario con scroll dinámico que depende del estado del jugador.

Estructura del Proyecto
game.py: Control de ciclo principal, gestión de estados (menú, juego, game over) y transición entre escenas.

src/scenes/main_menu.py: Menú principal con pantalla inicial, botón Play y controles.

src/scenes/level1.py: Nivel principal con lógica del juego, enemigos, obstáculos, fondos y HUD.

src/entities/player.py: Clase del jugador con física, controles, hitbox y animaciones.

src/entities/enemy.py: Clase del enemigo perro con IA básica.

src/entities/obstacle.py: Obstáculos y cajas con diferentes efectos.

Controles
Flechas izquierda/derecha o teclas A/D: Movimiento lateral.

Espacio o flecha arriba: Salto.

En el menú y pantalla de inicio: Espacio o click en botón Play para comenzar.

Pantalla Game Over: Espacio para reintentar, ESC para volver al menú.

Requisitos
Python 3.7+

Pygame instalado

Archivos de recursos en carpeta assets/images organizados como:

background/start.png: Imagen de inicio.

background/day/day.png: Fondo de día.

background/night/night.png: Fondo de noche.

Sprites para jugador, enemigo y obstáculos.

Ejecución
Ejecutar game.py o main.py para iniciar el juego. Comienza con la pantalla de inicio, seguido por el menú principal. Desde el menú se inicia la partida y el nivel 1.

Personalización
Ajusta variables en settings.py para modificar velocidad, duración de efectos de caja, separación entre cajas y otros parámetros.

Modifica gráficos en assets/images para cambiar apariencia.

Cambia duración del ciclo día/noche en level1.py con day_night_cycle_duration.