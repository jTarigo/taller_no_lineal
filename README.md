# Taller: Física no lineal en el aula — parte numérica

Cuadernos interactivos para un taller de tres días en un congreso de profesores
de física de secundaria. Los participantes **no instalan nada**: abren un link.

| Día | Cuaderno | Contenido |
|---|---|---|
| 1 | `Dia1_Pendulos_NoLineal.ipynb` | Péndulo lineal y exacto, espacio de fases, péndulo magnético, cuencas de atracción |
| 2 | `Dia2_MapaLogistico.ipynb` | Mapa logístico, telaraña, diagrama de bifurcación, constante de Feigenbaum |
| 3 | *(pendiente)* | Sistema de Lorenz, atractor extraño, exponente de Lyapunov |

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

**Día 1 — péndulo magnético.** El rozamiento está en `b = 0.05` (no 0.2). Con
rozamiento alto la estructura fractal de las cuencas se apaga y la demostración
de sensibilidad no muestra nada: todas las separaciones δ terminan en el mismo
imán. Con `b = 0.05` y `tmax = 500`, el 100 % de las trayectorias converge y
~21 % de los puntos cambia de destino ante una perturbación de 10⁻⁶. El punto de
suelta por defecto, (−0.75, −1.50), fue elegido por búsqueda: cambia de imán en
todas las escalas de δ.

**Día 1 — reproducibilidad de las cuencas.** Calculado con `dt=0.05` y `dt=0.02`,
el mapa coincide sólo en ~50 % de los puntos. No es un error: en el **interior** de
las cuencas la coincidencia es 96–98 %, y las proporciones globales de cada color
son estables (~33 % cada una). El desacuerdo está enteramente en la frontera
fractal, que ocupa la mayor parte del plano. Esto está convertido en el Ejercicio 2,
con la predicción pedida *antes* de ejecutar.

**Día 1 — precisión.** El período por integral elíptica coincide con el medido
sobre la simulación con error ~10⁻¹³. Atención: `scipy.special.ellipk` toma el
parámetro `m = k²`, no el módulo `k` — es un error clásico. El paso de medición
está en 10⁻³ (error 3×10⁻¹⁰, diez veces más rápido que 10⁻⁴).

**Día 1 — velocidad.** `integrar_rapido()` va retirando del cálculo los péndulos
que ya se detuvieron. Da resultados **100 % idénticos** y tarda la mitad. Tiempos
verificados: vista general 17 s, zoom 16 s, Ejercicio 2 28 s. El resto del cuaderno
es instantáneo (total ~68 s).

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
