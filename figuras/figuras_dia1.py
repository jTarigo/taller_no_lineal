"""Diagramas estaticos del Dia 1. Cada funcion guarda un PNG que despues va
incrustado en una celda de texto del cuaderno.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

AZUL = "#1f4e79"
ROJO = "#c0392b"
VERDE = "#1e8449"
NARANJA = "#d68910"
GRIS = "#7f8c8d"


def flecha(ax, desde, vec, color, lw=2.0, ls="-", escala=15):
    ax.annotate("", xy=(desde[0] + vec[0], desde[1] + vec[1]), xytext=desde,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, mutation_scale=escala))


# ------------------------------------------------------------------ fuerzas
def diagrama_fuerzas(salida="diagrama_fuerzas.png"):
    TH = np.radians(28.0)
    BOB = np.array([np.sin(TH), -np.cos(TH)])
    u_rod = BOB/np.linalg.norm(BOB)
    u_tan = np.array([-u_rod[1], u_rod[0]])

    fig, ax = plt.subplots(figsize=(5.2, 4.8), dpi=130)
    ax.plot([-0.28, 0.28], [0, 0], color="black", lw=2.5)
    for xx in np.linspace(-0.26, 0.24, 7):
        ax.plot([xx, xx + 0.07], [0, 0.09], color="black", lw=1.0)
    ax.plot([0, 0], [0, -1.22], ls="--", lw=1.1, color=GRIS)
    ax.plot([0, BOB[0]], [0, BOB[1]], color="black", lw=1.8)
    ax.plot(0, 0, "o", ms=5, color="black")
    ax.add_patch(plt.Circle(BOB, 0.085, color=AZUL, zorder=5))
    ax.add_patch(Arc((0, 0), 1.05, 1.05, theta1=-90, theta2=-90 + np.degrees(TH),
                     lw=1.3, color=GRIS))
    ax.text(0.145, -0.62, r"$\theta$", fontsize=15, color=GRIS)
    ax.text(0.5*BOB[0] - 0.13, 0.5*BOB[1] + 0.04, "L", fontsize=13)

    P = 0.62
    peso = np.array([0.0, -P])
    comp_rad = np.dot(peso, u_rod)*u_rod
    comp_tan = np.dot(peso, u_tan)*u_tan

    flecha(ax, BOB, peso, "black", lw=2.2, escala=16)
    ax.text(BOB[0] - 0.06, BOB[1] - P - 0.12, "mg", fontsize=13, ha="center")
    flecha(ax, BOB, -0.42*u_rod, AZUL, lw=2.2, escala=16)
    ax.text(BOB[0] - 0.34*u_rod[0] + 0.07, BOB[1] - 0.34*u_rod[1] + 0.02,
            "T", fontsize=13, color=AZUL)
    flecha(ax, BOB, comp_tan, ROJO, lw=2.6, escala=16)
    flecha(ax, BOB, comp_rad, GRIS, lw=1.6, ls="--", escala=16)
    ax.plot([BOB[0] + comp_tan[0], BOB[0] + peso[0]],
            [BOB[1] + comp_tan[1], BOB[1] + peso[1]], ls=":", lw=0.9,
            color=GRIS, alpha=0.8)
    ax.plot([BOB[0] + comp_rad[0], BOB[0] + peso[0]],
            [BOB[1] + comp_rad[1], BOB[1] + peso[1]], ls=":", lw=0.9,
            color=GRIS, alpha=0.8)
    ax.text(BOB[0] + comp_tan[0] - 0.09, BOB[1] + comp_tan[1] + 0.05,
            r"$mg\,\sin\theta$", fontsize=13, color=ROJO, ha="right")
    ax.text(BOB[0] + comp_rad[0] + 0.07, BOB[1] + comp_rad[1] - 0.06,
            r"$mg\,\cos\theta$", fontsize=12, color=GRIS)
    ax.text(0.30, -1.74, r"$m\,L\,\ddot{\theta} \;=\; -\,m\,g\,\sin\theta$",
            fontsize=15, ha="center")
    ax.set_xlim(-0.80, 1.40)
    ax.set_ylim(-1.92, 0.22)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(salida, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# -------------------------------------------------------------------- Euler
def diagrama_euler(salida="diagrama_euler.png"):
    h = 1.0
    t = np.linspace(-0.12, 1.32, 300)
    fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=130)
    ax.plot(t, np.exp(t), lw=2.4, color=AZUL, zorder=2,
            label="solución verdadera")

    ax.plot([0, h], [1, 2], lw=2.2, color=ROJO, zorder=3)
    flecha(ax, (0, 1), (h, 1), ROJO, lw=2.2, escala=14)
    ax.plot(0, 1, "o", ms=8, color="black", zorder=5)
    ax.plot(h, 2, "o", ms=8, color=ROJO, zorder=5)
    ax.plot(h, np.e, "o", ms=8, mfc="white", mec=AZUL, mew=2, zorder=5)

    ax.annotate("", xy=(h, np.e), xytext=(h, 2),
                arrowprops=dict(arrowstyle="<->", color=VERDE, lw=1.8))
    ax.text(h + 0.05, 0.5*(2 + np.e), "error\ndel paso", color=VERDE,
            fontsize=11, va="center")

    ax.plot([0, 0], [0, 1], ls=":", lw=1.0, color=GRIS)
    ax.plot([h, h], [0, 2], ls=":", lw=1.0, color=GRIS)
    ax.annotate("", xy=(h, 0.35), xytext=(0, 0.35),
                arrowprops=dict(arrowstyle="<->", color=GRIS, lw=1.2))
    ax.text(0.5*h, 0.45, "dt", ha="center", fontsize=12, color=GRIS)

    ax.text(0.06, 0.92, r"$u_n$", fontsize=13, va="top")
    ax.text(h + 0.05, 2.0, r"$u_{n+1}$", fontsize=13, color=ROJO, va="center")
    ax.text(0.40, 1.02, "la recta usa la pendiente\nsólo del punto de partida",
            fontsize=10.5, color=ROJO, va="top")

    ax.set_xlim(-0.15, 1.45)
    ax.set_ylim(0.2, 3.5)
    ax.set_xticks([0, h])
    ax.set_xticklabels([r"$t_n$", r"$t_n + dt$"], fontsize=12)
    ax.set_yticks([])
    ax.set_title("Método de Euler: un paso", fontsize=13)
    ax.legend(loc="upper left", fontsize=10, frameon=False)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    fig.tight_layout()
    fig.savefig(salida, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------- RK4
def diagrama_rk4(salida="diagrama_rk4.png"):
    h = 1.5
    t = np.linspace(-0.25, 1.75, 400)
    u0 = 1.0
    k1 = u0                                   # f(u) = u
    u_a = u0 + h/2*k1;  k2 = u_a
    u_b = u0 + h/2*k2;  k3 = u_b
    u_c = u0 + h*k3;    k4 = u_c
    prom = (k1 + 2*k2 + 2*k3 + k4)/6
    u1 = u0 + h*prom

    fig, ax = plt.subplots(figsize=(7.0, 4.6), dpi=130)
    ax.plot(t, np.exp(t), lw=2.4, color=AZUL, zorder=2,
            label="solución verdadera")
    ax.plot(0, u0, "o", ms=8, color="black", zorder=6)
    ax.text(-0.08, u0, r"$u_n$", fontsize=13, ha="right", va="center")

    MORADO = "#8e44ad"
    # los cuatro tanteos: donde se evalua la pendiente y cuanto vale
    tanteos = [(0.0,  u0,  k1, r"$k_1$", ROJO,    0.34, "izq"),
               (h/2,  u_a, k2, r"$k_2$", NARANJA, 0.34, "abajo"),
               (h/2,  u_b, k3, r"$k_3$", VERDE,   0.34, "arriba"),
               (h,    u_c, k4, r"$k_4$", MORADO,  0.30, "der")]
    for tt, uu, kk, nombre, col, s, donde in tanteos:
        ax.plot([tt - s, tt + s], [uu - s*kk, uu + s*kk], lw=2.2, color=col,
                zorder=4)
        if donde != "der":
            ax.plot(tt, uu, "o", ms=7, color=col, zorder=6)
        if donde == "izq":
            ax.text(tt - s - 0.05, uu - s*kk, nombre, color=col, fontsize=14,
                    ha="right", va="center")
        elif donde == "abajo":
            ax.text(tt + s + 0.05, uu + s*kk - 0.12, nombre, color=col,
                    fontsize=14, va="top")
        elif donde == "arriba":
            ax.text(tt - s - 0.14, uu - s*kk + 0.26, nombre, color=col,
                    fontsize=14, ha="right", va="center")
        else:
            ax.text(tt + s + 0.05, uu + s*kk, nombre, color=col, fontsize=14,
                    va="center")

    # como se llega a cada tanteo
    ax.plot([0, h/2], [u0, u_a], ls=":", lw=1.3, color=ROJO)
    ax.plot([0, h/2], [u0, u_b], ls=":", lw=1.3, color=NARANJA)
    ax.plot([0, h], [u0, u_c], ls=":", lw=1.3, color=VERDE)

    flecha(ax, (0, u0), (h, h*prom), "black", lw=2.8, escala=18)
    ax.plot(h, u1, "o", ms=9, color="black", zorder=7)
    ax.annotate(r"$u_{n+1}$", xy=(h, u1), xytext=(h - 0.30, u1 - 1.15),
                fontsize=13, ha="center",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.9))
    ax.text(0.02, 5.6, "el paso final avanza con el promedio pesado\n"
                       r"$(k_1 + 2k_2 + 2k_3 + k_4)\,/\,6$", fontsize=11.5)

    ax.plot([h/2, h/2], [0, u_a], ls=":", lw=1.0, color=GRIS, zorder=1)
    ax.set_xlim(-0.45, 2.00)
    ax.set_ylim(0.0, 6.6)
    ax.set_xticks([0, h/2, h])
    ax.set_xticklabels([r"$t_n$", "mitad del paso", r"$t_n + dt$"], fontsize=11)
    ax.set_yticks([])
    ax.set_title("Runge–Kutta 4: cuatro tanteos y un promedio", fontsize=13)
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    for lado in ["top", "right"]:
        ax.spines[lado].set_visible(False)
    fig.tight_layout()
    fig.savefig(salida, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ------------------------------------------------------- pendulo magnetico
def diagrama_iman(salida="diagrama_iman.png"):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 4.6), dpi=125)

    # ---------------- vista de costado ----------------
    a1.plot([-1.3, 1.3], [2.0, 2.0], color="black", lw=2.5)
    for xx in np.linspace(-1.25, 1.15, 12):
        a1.plot([xx, xx + 0.1], [2.0, 2.1], color="black", lw=0.9)
    xb, yb = 0.62, 0.42
    a1.plot([0, xb], [2.0, yb], color="black", lw=1.5)
    a1.plot([0, 0], [2.0, 0.0], ls="--", lw=1.0, color=GRIS)
    a1.add_patch(plt.Circle((xb, yb), 0.13, color=AZUL, zorder=5))
    a1.text(xb + 0.20, yb + 0.06, "imán del péndulo", fontsize=10, va="center")

    a1.plot([-1.5, 1.5], [0, 0], color="#5d4037", lw=3)
    a1.text(-1.45, -0.28, "mesa", fontsize=10, color="#5d4037")
    for xm, col in [(-0.95, "#e74c3c"), (-0.25, "#3498db"),
                    (0.45, "#2ecc71"), (1.15, "#9b59b6")]:
        a1.add_patch(plt.Rectangle((xm - 0.09, 0.0), 0.18, 0.12, color=col,
                                   ec="k", lw=0.7, zorder=4))
    a1.annotate("", xy=(xb, 0.02), xytext=(xb, yb - 0.13),
                arrowprops=dict(arrowstyle="<->", color=ROJO, lw=1.5))
    a1.text(xb + 0.09, 0.5*yb - 0.04, "d", fontsize=13, color=ROJO)
    a1.text(0.36, 1.45, "hilo largo", fontsize=10, color=GRIS)
    a1.set_xlim(-1.7, 2.3)
    a1.set_ylim(-0.5, 2.35)
    a1.set_aspect("equal")
    a1.axis("off")
    a1.set_title("Visto de costado", fontsize=12)

    # ---------------- vista de arriba ----------------
    COLORES = ["#e74c3c", "#3498db", "#2ecc71", "#9b59b6", "#e67e22", "#16a085"]
    ang = np.pi/2 + 2*np.pi*np.arange(6)/6
    IX, IY = np.cos(ang), np.sin(ang)
    P = np.array([0.40, -0.30])

    a2.add_patch(plt.Circle((0, 0), 1.0, fill=False, ls=":", lw=1.0, color=GRIS))
    for i in range(6):
        a2.add_patch(plt.Circle((IX[i], IY[i]), 0.115, color=COLORES[i],
                                ec="k", lw=0.8, zorder=4))
        a2.annotate(str(i + 1), (IX[i], IY[i]), ha="center", va="center",
                    fontsize=9, zorder=5)
    a2.plot(0, 0, "+", ms=12, color="black", mew=1.5)
    a2.text(-0.12, 0.10, "centro", fontsize=9.5, color=GRIS, ha="right")

    puntas = []
    for i in range(6):
        d = np.array([IX[i], IY[i]]) - P
        d = 0.48*d/np.linalg.norm(d)
        flecha(a2, P, d, COLORES[i], lw=1.4, escala=11)
        puntas.append(P + d)
    a2.plot([0, P[0]], [0, P[1]], lw=1.0, color=AZUL, alpha=0.7)
    a2.text(0.5*P[0] + 0.03, 0.5*P[1] + 0.11, r"$\vec{r}$", fontsize=13,
            color=AZUL)
    flecha(a2, P, -0.45*P/np.linalg.norm(P), "black", lw=2.4, escala=15)
    a2.add_patch(plt.Circle(P, 0.07, color=AZUL, zorder=6))
    a2.annotate(r"$-k\,\vec{r}$", xy=tuple(P - 0.30*P/np.linalg.norm(P)),
                xytext=(-0.52, -0.58), fontsize=13, ha="center",
                arrowprops=dict(arrowstyle="-", color="black", lw=0.8))
    a2.annotate("atracción de\ncada imán", xy=tuple(puntas[5]),
                xytext=(1.30, 0.55), fontsize=10, color=GRIS,
                arrowprops=dict(arrowstyle="-", color=GRIS, lw=0.8))

    a2.set_xlim(-1.45, 2.15)
    a2.set_ylim(-1.42, 1.42)
    a2.set_aspect("equal")
    a2.axis("off")
    a2.set_title("Visto desde arriba: 6 imanes en hexágono", fontsize=12)

    fig.tight_layout()
    fig.savefig(salida, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    diagrama_fuerzas()
    diagrama_euler()
    diagrama_rk4()
    diagrama_iman()
    print("cuatro figuras generadas")
