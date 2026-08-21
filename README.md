# Taller: Física no lineal en el aula — parte numérica

Cuadernos interactivos para un taller de tres días en un congreso de profesores
de física de secundaria. Los participantes **no instalan nada**: abren un link.

| Día | Cuaderno | Contenido |
|---|---|---|
| 1 | `Dia1_Pendulos_NoLineal.ipynb` | Péndulo lineal y exacto, espacio de fases, péndulo magnético, cuencas de atracción |
| 2 | `Dia2_MapaLogistico.ipynb` | Mapa logístico, telaraña, diagrama de bifurcación, constante de Feigenbaum |
| 3 | `Dia3_Lorenz.ipynb` | Sistema de Lorenz, atractor extraño, exponente de Lyapunov, mapa de retorno |

---

## 1. Publicar los cuadernos (lo que hace el docente, una vez)

### Paso 1 — subir a GitHub

Crear un repositorio público (por ejemplo `taller-no-lineal`) y subir los `.ipynb`.
No hace falta usar la línea de comandos: la interfaz web de GitHub permite arrastrar
los archivos con *Add file → Upload files*.

### Paso 2 — armar el link de Colab

El formato es directo:

```
https://colab.research.google.com/github/USUARIO/REPO/blob/main/colab/Dia1_Pendulos_NoLineal.ipynb
```

Reemplazar `USUARIO/REPO`. Ese link abre el cuaderno en Colab, listo para usar.

### Paso 3 — acortar el link

Un link de Colab es largo e imposible de dictar. Conviene acortarlo
(bit.ly, tinyurl, o `is.gd`) y proyectar **el link corto**, además de escribirlo
en el pizarrón. Ideal: `bit.ly/nolineal-dia1`.

### Paso 4 (opcional) — badge en el README del repo

```markdown
[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USUARIO/REPO/blob/main/colab/Dia1_Pendulos_NoLineal.ipynb)
```

---

## 2. Las instrucciones para los participantes

Éstas ya están escritas dentro de cada cuaderno, pero conviene proyectarlas al
empezar:

1. Abrir el link.
2. Arriba a la derecha: **"Copiar en Drive"**.
   ⚠️ Sin este paso pueden mirar pero **no guardar** sus cambios.
3. Menú: **Entorno de ejecución → Ejecutar todas**.
4. Si aparece *"Este cuaderno no lo creó Google"* → **"Ejecutar de todos modos"**.
5. Esperar ~20 segundos.

**Requisito real:** una cuenta de Google. La mayoría de los docentes ya tiene una,
pero conviene avisarlo en la convocatoria del taller para que nadie llegue sin ella.

**No hay ningún `pip install`.** Los cuadernos usan sólo numpy, scipy, matplotlib
e ipywidgets, que Colab ya trae. El arranque es inmediato.

---

## 3. La regla de oro de Colab

Éste es el punto flojo de Jupyter/Colab frente a un cuaderno reactivo, y conviene
anticiparlo:

> **Las celdas se ejecutan en orden, de arriba hacia abajo.**
> Si algo da un error raro, casi siempre es porque se salteó una celda.
> Solución universal: *Entorno de ejecución → Reiniciar y ejecutar todo*.

Mitigaciones ya incluidas en los cuadernos:
- la regla está destacada en la introducción de cada uno;
- todos los deslizadores usan `continuous_update=False`, así no recalculan
  mientras se arrastra;
- las celdas que hay que editar están marcadas con `←←←` y dicen exactamente qué
  número cambiar.

---

## 4. Alternativa: marimo (si sobra tiempo antes del congreso)

**marimo** es a Python lo que Pluto es a Julia: un cuaderno **reactivo**, sin
estado oculto. Cambiar un valor recalcula sola todo lo que dependa de él, así que
el problema del orden de las celdas simplemente no existe.

Lo interesante es cómo se entrega:

```bash
pip install marimo
marimo edit notebook.py                                   # editar
marimo export html-wasm notebook.py -o sitio/ --mode run  # exportar
```

El export produce un HTML autocontenido que corre **Python entero dentro del
navegador** (vía Pyodide). Se sube a GitHub Pages y listo: **sin cuenta de Google,
sin servidor, sin esperar que arranque nada.** Un link y anda.

**Dos advertencias honestas:**

- Pyodide es bastante más lento que CPython. Los mapas de cuencas del Día 1 tardan
  ~17 s en Colab; en WASM podrían ser 1–2 minutos. Habría que bajar la resolución
  a N=60–80.
- El HTML **debe servirse por HTTP**; no funciona abriéndolo como `file://`. O sea
  que igual hace falta GitHub Pages o similar.

**Recomendación:** Colab como opción principal (robusto, conocido, y los docentes
ya tienen cuenta de Google). marimo como respaldo que no depende de que Google
ande, si hay tiempo de prepararlo.

---

## 5. Plan B (obligatorio)

Antes del taller, en cada cuaderno: *Archivo → Descargar → .ipynb* y también
guardar una copia ejecutada como HTML/PDF. Subirlo a GitHub Pages y llevarlo en
un pendrive.

No es interactivo, pero tiene todas las figuras y todo el texto. **Si se cae el
wifi del congreso, el taller sigue.**

---

## 6. Checklist del día

- [ ] Link corto proyectado **y** escrito en el pizarrón
- [ ] Avisar en la convocatoria que hace falta cuenta de Google
- [ ] Versiones estáticas subidas y linkeadas
- [ ] Pendrive con los `.ipynb` y los HTML
- [ ] Probar el link desde el wifi del congreso, no desde casa
- [ ] Abrir un cuaderno 10 minutos antes para verificar que todo responde
- [ ] Para el Día 2: recordarles que traigan **calculadora** (o el celular)

---

## Notas técnicas sobre el contenido

Estas decisiones se tomaron después de verificar numéricamente los resultados;
quedan documentadas por si hay que retocar algo.

**Día 1 — fluidez de los deslizadores (revisión).** El cuello de botella era el
espacio de fases: integraba 6 trayectorias en bucles de Python separados con
dt=0.005 sobre hasta 200 s (~240.000 pasos, ~2.5 s por movimiento). Dos arreglos
medidos: (a) `rk4_varias()` integra las 6 juntas en un array (2,6) → 2.2×;
(b) paso a dt=0.02, cuyo error contra dt=0.001 en régimen caótico es 1.5×10⁻⁶,
irrelevante para dibujar → 4×. Combinados: **0.28 s en vez de 2.49 s (9×)**.
Además se submuestrean los puntos al graficar y se aligeró el `quiver` (21×15).
Todos los deslizadores usan `continuous_update=False`, así que recalculan al
soltar, no al arrastrar.

**Día 1 — péndulo magnético: legibilidad vs fractalidad.** Son dos caras de la
misma cantidad física (cuánto explora el transitorio antes de asentarse) y no
existe un juego de parámetros que dé ambas: se escaneó k ∈ {0.5, 1.0},
d ∈ {0.15, 0.25, 0.40}, b ∈ {0.10, 0.15, 0.20} sin candidatos. La solución es
pedagógica, no numérica: mostrar la transición como contenido.

- **Mapa principal: b = 0.20**, legible (52 % de píxeles "interiores"), tres
  cuencas claras. Enseña atractor y cuenca sin ruido visual.
- **Tres paneles b = 0.30 / 0.15 / 0.06** para ver cómo la zona de mezcla se come
  el plano al bajar el rozamiento.

**Día 1 — exponente de incertidumbre.** Es la respuesta rigurosa a "¿son fractales
las fronteras?" (método de Grebogi–McDonald–Ott–Yorke 1983): se perturban puntos
al azar en ε y se mide la fracción que cambia de destino; f(ε) ~ ε^α y D = 2 − α.
Medido con 2500–8000 puntos y perturbación isótropa:

| b | α | D = 2 − α |
|---|---|---|
| 0.30 | 0.84 | 1.16 |
| 0.20 | 0.68 | 1.32 |
| 0.15 | 0.49 | 1.51 |
| 0.10 | 0.20–0.23 | 1.77–1.80 |

**Todas las fronteras son fractales (D > 1), incluida la de b = 0.30 que a simple
vista parece lisa.** Lo que cambia con b no es *si* hay fractalidad sino qué
porción del plano ocupa la zona enredada.

**Día 1 — el experimento de dt usa b = 0.06, no 0.20.** Esto importa y se verificó
explícitamente:

| b | dt .05 vs .02 | dt .02 vs .01 | ¿converge? |
|---|---|---|---|
| 0.20 | 0.15–0.36 % | **0.00 %** | sí, totalmente |
| 0.10 | 4.9 % | 0.20 % | casi |
| 0.06 | 26.5 % | **7.3 %** | no |

Con b = 0.20 el cálculo converge al refinar el paso: la discrepancia con dt=0.05
es simple error de integración y presentarla como "sensibilidad" sería incorrecto.
Con b = 0.06 no converge, y ahí sí el efecto es la limitación de fondo que ata con
la anécdota de Lorenz del Día 3. El cuaderno muestra ambos renglones y explica la
diferencia entre *error numérico que se corrige* y *limitación irreducible*.

**Día 1 — condición inicial de la sección 6.1.** Con b = 0.20 los únicos puntos
sensibles hasta δ=10⁻⁶ sobre la grilla del deslizador (paso 0.05) caen en x = 0,
que es eje de simetría y por lo tanto degenerado. Se usa **(0.30, −1.40) con
b = 0.10**, verificado: cambia de imán en las seis escalas de δ y está lejos del
eje. La sección tiene además un deslizador de rozamiento para que se vea que con
b = 0.30 la sensibilidad desaparece.

**Día 1 — tiempos verificados (total ~100 s).** Todo instantáneo salvo: cuencas
principales 5 s, tres paneles 18 s, exponente de incertidumbre 18 s, Ejercicio 2
22 s, tabla de convergencia 34 s.

**Día 2 — Feigenbaum.** Se usan **ciclos superestables** ($f^{2^n}(0.5) = 0.5$,
resuelto por bisección) en vez de los puntos de bifurcación: es numéricamente
mucho más estable y el método es elemental. Las ventanas de búsqueda se calculan
solas usando la propia escala 4.669. Converge hasta período 512 dando
δ = 4.669191 (error 10⁻⁵). Más allá de n=9 falla por redondeo de punto flotante,
y eso está explicado en el cuaderno como tema de discusión, no escondido.

**Día 2 — universalidad.** Verificado con el mapa seno `r·sin(πx)`: los $R_n$ son
completamente distintos (0.777, 0.846, 0.861...) pero δ converge a 4.669151. El
rango de búsqueda de `r` se detecta automáticamente, así que el ejercicio funciona
descomentando una sola línea.

**Día 2 — chequeos.** Punto fijo en r=2.8 coincide con 1−1/r exacto; períodos 2, 4
y 3 detectados en r=3.2, 3.5 y 3.83; exponente de Lyapunov en r=4 da 0.693149
contra ln2 = 0.693147.

**Día 3 — paso de integración.** Verificado que `dt = 0.005` converge: de ahí para
abajo la posición a t=10 ya no cambia. Con `dt = 0.02` hay error visible (3.7×10⁻²).
El cuaderno muestra esta comparación explícitamente, como hábito de trabajo.

**Día 3 — Lyapunov.** Algoritmo de Benettin con renormalización cada paso. La
implementación es **escalar** (x, y, z como floats sueltos en vez de un array de
numpy de 3 elementos): da el mismo resultado y es ~60 veces más rápida — 0.5 s en
vez de 32 s para tmax=1000. Converge a λ ≈ 0.90 contra el ≈0.9056 de la
literatura. Dos controles incluidos: ρ=13 da λ negativo, y el resultado no cambia
con el paso de integración.

**Día 3 — clasificación de regímenes.** Ojo con una diferencia respecto del Día 2:
en un **flujo continuo** una órbita periódica da λ ≈ 0, no λ < 0, porque existe la
dirección a lo largo de la trayectoria. Sólo los puntos fijos dan λ netamente
negativo. El clasificador del Ejercicio 1 distingue los tres casos y el cuaderno
explica la sutileza.

**Día 3 — rangos verificados para el Ejercicio 1.** ρ = 13 → −0.44 (punto fijo);
23 → −0.055; 24 → +0.76 (transición brusca); 28 → +0.90; 45 → +1.22 (sigue
caótico); 100 y 160 → ≈0 (ciclo límite). Cuidado: ρ = 40–50 **siguen** siendo
caóticos, la vuelta al orden llega mucho más arriba.

**Día 3 — mapa de máximos.** Los picos de z(t) se afinan con interpolación
parabólica sobre los tres puntos vecinos. Con el transitorio descartado, la
relación z_(n+1) vs z_n tiene grosor de 1.1 % de su extensión: es una curva, no
una nube. La pendiente típica |f'| ≈ 1.65 > 1 explica el caos en el lenguaje del
Día 2 y cierra los tres días.
