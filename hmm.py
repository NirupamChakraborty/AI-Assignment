states       = ["Healthy", "Sick"]
observations = ["No Fever", "Fever"]


pi = [0.7, 0.3]


A = [[0.80, 0.20],   
    [0.30, 0.70],]

B = [[0.90, 0.10],   
    [0.20, 0.80],]

#  Fever, No Fever, Fever, Fever
obs_seq = [1, 0, 1, 1]



def forward(obs_seq, pi, A, B):
    T, N = len(obs_seq), len(states)
    alpha = [[0.0] * N for _ in range(T)]

    for i in range(N):
        alpha[0][i] = pi[i] * B[i][obs_seq[0]]

    for t in range(1, T):
        for j in range(N):
            alpha[t][j] = (
                sum(alpha[t-1][i] * A[i][j] for i in range(N))
                * B[j][obs_seq[t]]
            )

    return alpha, sum(alpha[T-1])



def viterbi(obs_seq, pi, A, B):
    T, N = len(obs_seq), len(states)
    delta = [[0.0] * N for _ in range(T)]
    psi   = [[0]   * N for _ in range(T)]

    for i in range(N):
        delta[0][i] = pi[i] * B[i][obs_seq[0]]

    for t in range(1, T):
        for j in range(N):
            probs     = [delta[t-1][i] * A[i][j] for i in range(N)]
            psi[t][j] = max(range(N), key=lambda i: probs[i])
            delta[t][j] = probs[psi[t][j]] * B[j][obs_seq[t]]

    best_path      = [0] * T
    best_path[T-1] = max(range(N), key=lambda i: delta[T-1][i])
    for t in range(T-2, -1, -1):
        best_path[t] = psi[t+1][best_path[t+1]]

    return best_path, delta[T-1][best_path[T-1]]



print("HMM Patient Health")
print(f"\nObservations: {[observations[o] for o in obs_seq]}")



alpha, prob = forward(obs_seq, pi, A, B)
print(f"\n[Forward] P(O | λ) = {prob:.6f}")
print(f"\n{'t':<4} {'Healthy':>10} {'Sick':>10}")
for t, row in enumerate(alpha):
    print(f"{t:<4} {row[0]:>10.6f} {row[1]:>10.6f}")



path, path_prob = viterbi(obs_seq, pi, A, B)
print(f"\n[Viterbi] Most likely hidden states:")

for t, s in enumerate(path):
    print(f"  t={t}: {states[s]}  (observed: {observations[obs_seq[t]]})")
print(f"Path probability = {path_prob:.8f}\n")


# What-if scenarios
print("WHAT-IF SCENARIOS")

test_cases = [
    ([0, 0, 0], "Three days, no fever"),
    ([1, 1, 1], "Three days, persistent fever"),
    ([0, 1, 0], "Fever appears only on day 2"),
]

for seq, description in test_cases:
    _, p   = forward(seq, pi, A, B)
    path2, _ = viterbi(seq, pi, A, B)
    print(f"\n{description}:")
    print(f"  Symptoms : {[observations[o] for o in seq]}")
    print(f"  Diagnosis: {[states[s] for s in path2]}")
    print(f"  P(O | λ) : {p:.6f}")