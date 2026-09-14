# Taller: Física no lineal en el aula — parte numérica

Cuadernos interactivos para un taller de tres días en un congreso de profesores
de física de secundaria. Los participantes **no instalan nada**: abren un link.

| Día | Cuaderno | Contenido |
|---|---|---|
| 1 | `Dia1_Pendulos_NoLineal.ipynb` | Péndulo lineal y exacto, espacio de fases, péndulo magnético, sensibilidad a condiciones iniciales |
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

**Día 1 — alcance.** El cuaderno termina en la sensibilidad a las condiciones
iniciales (sección 6.1). Se quitaron los mapas de cuencas, los paneles de
rozamiento, el exponente de incertidumbre y el experimento de paso de integración.

**Día 1 — fluidez de los deslizadores.** Costos medidos por movimiento:

| | antes | ahora |
|---|---|---|
| Sección 5, tmax=40 (default) | ~1.0 s | **0.042 s** |
| Sección 5, tmax=150 (máximo) | ~2.7 s | **0.14 s** |
| Sección 6.1, b=0.10 (default) | ~3.0 s | **0.15 s** |
| Sección 6.1, b=0.30 | ~3.0 s | **0.057 s** |

Tres cambios lo consiguen:

1. **Sección 5 vectorizada.** `rk4_varias()` integra las 6 trayectorias juntas en
   un array (2,6) en vez de 6 bucles separados.
2. **Paso dt = 0.03** en el retrato de fases. Verificado con conservación de
   energía (b=0, A=0, tmax=150): deriva relativa 2.0×10⁻⁵, invisible al dibujar.
   El test de "error contra dt pequeño" NO sirve en régimen caótico — da
   resultados no monótonos porque las trayectorias divergen por definición; la
   conservación de energía es el criterio correcto. El tope del deslizador de
   tiempo bajó de 200 s a 150 s.
3. **Sección 6.1 con aritmética escalar y corte temprano.** Las funciones
   `paso_iman` / `soltar_dos` usan floats sueltos en vez de arrays de numpy: para
   dos trayectorias es **20× más rápido** (numpy tiene un costo fijo por operación
   que sólo se amortiza con miles de datos). Además la integración corta apenas
   ambos péndulos se detuvieron, en vez de llegar siempre a los 500 s.

**Día 1 — la física no cambió con las optimizaciones.** Verificado tras los
cambios: el punto (0.30, −1.40) con b=0.10 sigue cambiando de imán en las **seis**
escalas de δ (10⁻¹ a 10⁻⁶); el control cerca de un imán (0, 1) sigue siendo
estable en las tres escalas probadas; con b=0.20 la sensibilidad desaparece (6/6
coinciden); el período elíptico sigue coincidiendo con el medido con error 10⁻¹¹.

**Día 1 — condición inicial de la sección 6.1.** Con b = 0.20 los únicos puntos
sensibles hasta δ=10⁻⁶ sobre la grilla del deslizador (paso 0.05) caen en x = 0,
que es eje de simetría y por lo tanto degenerado. Se usa **(0.30, −1.40) con
b = 0.10**. La sección tiene un deslizador de rozamiento para mostrar que con
b = 0.30 la sensibilidad desaparece: el péndulo se frena antes de poder "dudar".

**Día 1 — tiempo total de ejecución: ~1.5 s** (antes ~100 s), porque ya no hay
mapas de cuencas.

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
