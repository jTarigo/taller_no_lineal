# Taller: Física no lineal en el aula — parte numérica

Cuadernos interactivos para un taller de tres días en un congreso de profesores de
física de secundaria. Los participantes no instalan nada: abren un link.

| Día | Cuaderno | Contenido |
|---|---|---|
| 1 | `Dia1_Pendulos_NoLineal.ipynb` | Péndulo lineal y exacto, Euler contra RK4, período por integral elíptica, espacio de fases, péndulo magnético de 6 imanes |
| 2 | `Dia2_MapaLogistico.ipynb` | De dónde sale el mapa logístico, telaraña, diagrama de bifurcación con zoom, constante de Feigenbaum a mano y con un algoritmo, universalidad, ventana de período 3 |
| 3 | `Dia3_Lorenz.ipynb` | La historia de Lorenz, el atractor, exponente de Lyapunov, el mapa escondido, reconstrucción de Takens para los circuitos |

La carpeta `figuras/` tiene el script que genera los diagramas estáticos del Día 1
(fuerzas, Euler, RK4, péndulo magnético). Los PNG están incrustados en el cuaderno
como datos, así que el cuaderno anda solo: la carpeta es sólo para poder editarlos
y volver a generarlos.

---

## 1. Cómo se publican (lo que hace el docente, una vez)

**Subir a GitHub.** Un repositorio público con los `.ipynb` adentro. No hace falta
línea de comandos: la interfaz web permite arrastrar los archivos con
*Add file → Upload files*.

**Armar el link de Colab.** El formato es directo:

```
https://colab.research.google.com/github/USUARIO/REPO/blob/main/Dia1_Pendulos_NoLineal.ipynb
```

**Acortarlo.** Un link de Colab es imposible de dictar. Conviene acortarlo
(bit.ly, tinyurl, is.gd) y proyectar el link corto además de escribirlo en el
pizarrón. Algo tipo `bit.ly/nolineal-dia1`.

---

## 2. Las instrucciones para los participantes

Están escritas dentro de cada cuaderno, pero conviene proyectarlas al empezar:

1. Abrir el link.
2. Arriba a la derecha: **Copiar en Drive**. Sin ese paso pueden mirar y mover
   controles, pero al cerrar la pestaña se pierde todo.
3. **Entorno de ejecución → Ejecutar todas**.
4. Si aparece *"Este cuaderno no lo creó Google"* → **Ejecutar de todos modos**.
5. Esperar unos segundos: la primera celda no instala nada, sólo carga las
   herramientas y compila los integradores.

**Requisito real:** una cuenta de Google. Conviene avisarlo en la convocatoria.

**El "Ejecutar todas" anda de una, y esto costó dos arreglos.**

*Uno: se sacó ipympl.* Los cuadernos lo usaban para que las figuras respondieran al
mouse. Colab no siempre lo trae, así que la celda de preparación lo instalaba con
pip y cambiaba el backend de matplotlib en caliente — algo que en Colab exige
reiniciar el entorno, con lo cual había que ejecutar todo dos veces. Y encima el
módulo que dibuja esas figuras (jupyter-matplotlib) lo baja el navegador de
internet, así que las primeras figuras de un "Ejecutar todas" salían mudas.

Ahora cada figura se dibuja con matplotlib de siempre, se pasa a PNG y se muestra
adentro de un `ipywidgets.Image`, que es un widget básico y Colab lo dibuja sin
bajar nada. Los deslizadores siguen siendo `ipywidgets` y siguen recalculando
mientras se los arrastra: lo único que cambia es que, en vez de refrescarse el
lienzo, se reemplaza la imagen. Medido: entre 20 y 130 ms por cuadro según la
figura. Lo que se perdió a cambio es la lupa de la barra de herramientas, el click
adentro de la figura y girar el 3D con el mouse; los dos lugares que usaban click
y el atractor 3D ahora tienen deslizadores y botones, que además andan desde el
celular, donde apuntar adentro de un gráfico era incómodo.

*Dos: cada celda interactiva nombra sus cosas distinto.* Todas usaban `fig`, `ax`,
`a1`, `a2`. Un cuaderno tiene un solo espacio de nombres, así que después de un
"Ejecutar todas" el `fig` de cualquier celda era el de la última, y los
deslizadores de las anteriores movían el gráfico equivocado, o ninguno. Se veía
como figuras interactivas congeladas que revivían al reejecutar sólo esa celda.
Ahora cada una usa `fig_lineal`, `fig_fases`, `fig_zoom`, y así. Como red de
seguridad, `mostrar()` refresca además cualquier figura que matplotlib haya
marcado como cambiada.

---

## 3. Lo que instala cada cuaderno

**Nada.** numpy, scipy, matplotlib, ipywidgets y numba ya vienen en Colab, y no se
usa nada más. La celda de preparación sólo importa, fija cuatro `rcParams` y define
`lienzo()` y `mostrar()`: no corre pip, no toca el backend de matplotlib y no
espera a que se baje nada de internet.

Sin numba los cuadernos andan igual: la celda de preparación define un `njit` de
mentira que no compila nada, y los deslizadores pesados se arrastran un poco.

Las tres celdas de preparación son casi iguales (`lienzo`, `_imagen`, `_refrescar`,
`mostrar`, y después lo propio de cada día). Si hay que tocar eso, hay que tocarlo
en los tres.

---

## 4. Plan B (obligatorio)

Antes del taller, en cada cuaderno: *Archivo → Descargar → .ipynb*, y también una
copia ejecutada en HTML o PDF. Subirlo a GitHub Pages y llevarlo en un pendrive.

La versión estática no es interactiva y las figuras quedan en sus valores por
defecto, pero tiene todas las figuras y todo el texto. Si se cae el wifi del
congreso, el taller sigue.

---

## 5. Checklist del día

- [ ] Link corto proyectado y escrito en el pizarrón
- [ ] Avisar en la convocatoria que hace falta cuenta de Google
- [ ] Versiones estáticas subidas y linkeadas
- [ ] Pendrive con los `.ipynb` y los HTML
- [ ] Probar el link desde el wifi del congreso, no desde casa
- [ ] Abrir un cuaderno 10 minutos antes: *Ejecutar todas* y verificar que las
      figuras aparezcan y que los deslizadores respondan
- [ ] Día 2: la parte de la calculadora va **antes** de abrir el cuaderno
- [ ] Día 3: tener a mano los circuitos (Chua y el tipo Duffing) para la conexión
      del Ejercicio 2

---

## Notas técnicas sobre el contenido

Decisiones tomadas después de verificar los resultados numéricamente. Quedan
documentadas por si hay que retocar algo.

### Generales

**Deslizadores continuos.** Todos usan `continuous_update=True` y los callbacks
actualizan los datos de las curvas (`set_data`) en vez de rearmar la figura. Eso
sigue importando: volver a crear los artistas en cada evento es varias veces más
caro que rasterizar de nuevo los que ya están.

**Cómo llega la figura a la pantalla.** `mostrar(fig, *controles)` guarda la figura
junto a un `ipywidgets.Image`, muestra los controles arriba y reemplaza
`fig.canvas.draw_idle` por una función que vuelve a generar el PNG. Las celdas no
se enteran: siguen terminando en `fig.canvas.draw_idle()` como si hubiera un
backend interactivo. Dos detalles que no son obvios: `savefig` deja la figura
marcada como *stale*, así que `_imagen()` la apaga a mano (sin eso, "refrescar sólo
las que cambiaron" refresca todas); y `view_init`, el giro del 3D, no marca nada
como cambiado, por eso `_refrescar` siempre rehace la figura que se lo pidió.

**numba.** Los integradores van compilados. Medido en Colab: 15 trayectorias del
péndulo magnético de 200 unidades de tiempo tardan 100–200 ms compiladas, contra
unos 2 s en Python puro. Sin numba los cuadernos funcionan igual, sólo que los
deslizadores pesados se arrastran.

**Celdas plegadas.** El código de dibujo y de widgets está en celdas-formulario de
Colab (`#@title ... {display-mode: "form"}` más `"cellView": "form"` en los
metadatos), que se abren con doble click. La física siempre queda a la vista.

**Diagramas estáticos.** Los cuatro diagramas del Día 1 van incrustados como data
URI en las celdas de texto: se ven sin ejecutar nada y sobreviven al PDF.

### Día 1

**Euler contra RK4.** Sección nueva. Números verificados, con θ₀ = 90° y 10 s:

| dt | error de energía, Euler | RK4 |
|---|---|---|
| 0.02 | 120 % (se escapa y da vueltas) | 2·10⁻⁷ |
| 0.005 | 34 % (espiral visible) | 1·10⁻¹⁰ |
| 0.001 | 6.6 % | 1·10⁻¹³ |

El orden se verificó contra una referencia fina, comparando a igual tiempo final:
Euler divide el error por 2 al partir el paso al medio, RK4 por 16. Ojo que el
error de *energía* de RK4 cae más rápido que eso (factores de 30 a 45), así que el
texto habla del error de la trayectoria, que es el que da 16 limpio.

**Se sacó el forzado.** Ya no están `A` ni `Ω`, ni en la ecuación ni en el espacio
de fases. El cierre menciona en una línea que el péndulo forzado también es
caótico, sin hacerlo.

**Espacio de fases.** Las trayectorias se agregan eligiendo (θ₀, ω₀) con dos
deslizadores —un círculo rojo marca el estado elegido— y apretando "soltar". Se
dibujan además la separatriz y los equilibrios. El deslizador de rozamiento
recalcula todas las trayectorias que haya puestas.

**Péndulo magnético: 6 imanes.** Hexágono de radio 1, `k = 0.5`, `d = 0.25`. El
punto de partida de las quince sueltas es **(0.310096746049, −1.40)**, que está
sobre el borde entre dos cuencas y lo encontré por bisección con `b = 0.10`. Los
péndulos se sueltan repartidos sobre un segmento de largo δ centrado en ese punto.
Verificado con esa configuración:

| δ | imanes distintos (15 sueltas) |
|---|---|
| 10⁻¹ | 5 |
| 10⁻² | 6 |
| 10⁻³ | 6 |
| 10⁻⁴ | 2 |
| 10⁻⁵ | 3 |
| 10⁻⁶ | 2 |

Con `b = 0.20` o más, las quince caen juntas en el mismo imán: el punto deja de
estar sobre un borde y además el péndulo se frena antes de deambular. La
integración corta apenas el péndulo se detuvo (ahorra ~30 % de los pasos) y se
verificó que el corte no cambia ningún destino.

### Día 2

**Se sacó el método de ciclos superestables.** Queda mencionado en una línea como
la forma de llegar a los seis decimales.

**Feigenbaum a mano.** El diagrama de bifurcación tiene cuatro deslizadores
desde/hasta, el diagrama completo al lado con un recuadro, cinco botones de atajo y
una raya punteada en el centro de la ventana con su valor de `r` en el título:
medir una bifurcación es centrarla y leer. Con 3 decimales se obtiene δ ≈ 4.73 y
4.75; con 2 decimales, 5.0 y 4.5.

**El algoritmo.** Contar el período (tras 20000 iteraciones de transitorio,
tolerancia 10⁻⁸) más bisección sobre `r`. Resultados verificados:

| | δ₁ | δ₂ | δ₃ | δ₄ |
|---|---|---|---|---|
| detectado | 4.748 | 4.649 | 4.654 | 4.642 |
| exacto | 4.751 | 4.656 | 4.668 | 4.669 |

El sesgo es sistemático y está explicado en el cuaderno: cerca de la bifurcación el
transitorio se vuelve lentísimo, queda un temblor por encima de la tolerancia y el
detector declara la bifurcación antes de tiempo. Se achica subiendo `n_trans`.

**La ventana de búsqueda importa.** Los dos primeros `r_n` se buscan en todo el
rango; de ahí en más, en `[r_n, r_n + 0.4·hueco anterior]`. Con ventanas más
grandes la bisección se cuelga en las ventanas periódicas del caos (una ventana de
período 3 tiene período ≤ 4 y confunde el criterio "todavía no bifurcó").

**Mapa seno.** `r·sin(πx)` con `r ∈ (0, 1]`. Bifurcaciones en 0.7198, 0.8332,
0.8586, 0.8641: nada que ver con las del logístico. δ detectados: 4.47, 4.62, 4.65.

**Dibujo por densidad.** Los diagramas se arman contando cuántas veces cae la
órbita en cada casillero (`bincount`) y se muestran con `imshow` e interpolación
`antialiased`, con `vmax` en el percentil 90 y raíz cuadrada de las cuentas. Son
unos 20 ms por cuadro contra varios cientos dibujando medio millón de puntos, y
además se ve mejor.

### Día 3

**La historia va primero.** LGP-30, el modelo de 12 ecuaciones, 0.506 contra
0.506127, el café, Saltzman, Ellen Fetter, la charla de la mariposa de 1972 y el
título de Merilees. Recién después las ecuaciones.

**Se sacó la verificación del paso de integración** y la referencia al Día 1 que ya
no existía. En su lugar hay un aparte opcional sobre **sombreado** (*shadowing*):
por qué la trayectoria calculada no es la verdadera pero sirve igual, y dónde está
el límite (no sirve como pronóstico).

**Lyapunov.** Benettin, con renormalización cada paso, marcado como opcional y con
el código plegado. Verificado: converge a λ ≈ 0.90 (0.92 a t = 100, 0.916 a
t = 300); ρ = 13 da −0.45; ρ = 45 da +1.21 (sigue caótico); ρ = 100 y 160 dan ≈ 0
(ciclo límite); el resultado no cambia con dt = 0.002.

**Se sacó la observación sobre el Día 2** (la diferencia entre mapas y flujos
continuos para λ de órbitas periódicas). El clasificador del Ejercicio 1 sigue
distinguiendo los tres casos.

**Mapa de retorno.** Máximos de z afinados con interpolación parabólica. Grosor
típico 1.0 % de la extensión y pendiente |f'| ≈ 1.62. Sección marcada como
opcional.

**Ejercicio 2 corregido.** La versión anterior reconstruía con `z(t)` y afirmaba
que era equivalente al atractor. Es falso: z no distingue las dos alas, porque el
sistema es simétrico ante (x, y) → (−x, −y), y la reconstrucción las superpone en
un solo lóbulo. Ahora el ejercicio usa `x(t)`, que sí da la mariposa, y tiene un
selector para ver el caso de z como advertencia práctica: **qué variable se mide
importa**. Los tres paneles son la señal cruda, el modo XY con dos canales y la
reconstrucción con retardo, que es exactamente la situación de los circuitos de
Chua y Duffing con el osciloscopio.

**Cierre.** Figura de resumen con los tres sistemas del taller lado a lado
(espacio de fases, diagrama de bifurcación, atractor), tabla corregida y las tres
ideas.
