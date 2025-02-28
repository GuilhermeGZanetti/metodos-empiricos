data {
  int N;
  array[N] real S;
  real c;
}
generated quantities {
  // 
  array[N] real<upper=c> Si;
  for (j in 1:N) {
    // Amostra aleatóriamente de S
    real unif = uniform_rng(0,1);
    int idx = to_int(ceil(unif * N));
    Si[j] = S[idx];
  }
}
