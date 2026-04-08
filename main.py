import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do modelo
lam  = 1/100   # taxa de falha por módulo
mu_c = 1/1     # taxa de reparo corretivo
mu_p = 1/10    # taxa de reparo preventivo

C_values = [1.0, 0.95, 0.9, 0.8]

def build_Q(C):
    return np.array([
        [-2*lam,        lam*C,         lam*C,         lam*(1-C),   lam*(1-C)],
        [ mu_c,  -(lam+mu_c),              0,                 0,        lam  ],
        [ mu_c,          0,       -(lam+mu_c),                0,        lam  ],
        [ mu_p,          0,                0,       -(lam+mu_p),        lam  ],
        [ mu_c,          0,                0,                 0,      -mu_c  ],
    ])

def build_Q_abs(C):
    """Mesma Q mas com F absorvente: remove reparo F → M1."""
    Q = build_Q(C)
    Q[-1, :] = 0   # última linha zerada: F não tem saída
    return Q

def steady_state_availability(Q):
    A_mat = Q.copy()
    A_mat[:, -1] = 1.0
    b = np.zeros(5); b[-1] = 1.0
    pi = np.linalg.solve(A_mat.T, b)
    return 1 - pi[4]

# --- Disponibilidade A(t): sistema com reparo, janela curta ---
dt    = 0.05
T_max = 500
steps = int(T_max / dt)
t_A   = np.arange(steps) * dt

# --- Confiabilidade R(t): F absorvente, janela longa ---
dt_r    = 1.0
T_max_r = 50_000          # cobre MTTF de até ~5150 h com folga
steps_r = int(T_max_r / dt_r)
t_R     = np.arange(steps_r) * dt_r

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
colors = plt.cm.tab10.colors

print(f"\n{'C':>6}  {'D.A.':>12}  {'MTTF (h)':>12}")
print("-" * 36)

for i, C in enumerate(C_values):
    Q     = build_Q(C)
    Q_abs = build_Q_abs(C)

    # --- A(t): loop com reparo ---
    M = np.eye(5) + Q * dt
    P = np.zeros((steps, 5)); P[0] = [1, 0, 0, 0, 0]
    for k in range(steps - 1):
        P[k + 1] = P[k] @ M
    A = 1.0 - P[:, 4]

    # --- R(t): mesmo loop, sem reparo de F ---
    M_abs = np.eye(5) + Q_abs * dt_r
    P_abs = np.zeros((steps_r, 5)); P_abs[0] = [1, 0, 0, 0, 0]
    for k in range(steps_r - 1):
        P_abs[k + 1] = P_abs[k] @ M_abs
    R = 1.0 - P_abs[:, 4]

    # --- métricas extraídas das curvas ---
    da   = steady_state_availability(Q)   # D.A. analítico (exato)
    mttf = np.trapezoid(R, t_R)          # MTTF = área sob R(t)

    print(f"{C:>6.2f}  {da:>12.6f}  {mttf:>12.2f}")

    axes[0].plot(t_A, A, color=colors[i], label=f"C = {C}")
    axes[1].plot(t_R, R, color=colors[i], label=f"C = {C}  (MTTF = {mttf:.0f} h)")

# --- gráfico A(t) ---
axes[0].set_xlabel("t (h)"); axes[0].set_ylabel("A(t)")
axes[0].set_title("Disponibilidade — com reparo"); axes[0].legend(); axes[0].grid(True, alpha=0.3)

# --- gráfico R(t) ---
axes[1].set_xlabel("t (h)"); axes[1].set_ylabel("R(t)")
axes[1].set_title("Confiabilidade — sem reparo (F absorvente)"); axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("disponibilidade.png", dpi=150)
plt.show()
