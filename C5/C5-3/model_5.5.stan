data {
  int N_a;
  array[N_a] real S_a;
  int N_b;
  array[N_b] real S_b;
  real c;
}
generated quantities {
  array[N_a] real<upper=c> Si_a;
  // Juntando S_a e S_b
  array[N_a+N_b] real S_merge;

  for (i in 1:N_a+N_b) {
    if (i <= N_a){
      S_merge[i] = S_a[i];
    } else {
      S_merge[i] = S_b[i-N_a];
    }
  }

  // Pseudo amostra A
  for (j in 1:N_a) {
    // Amostra aleatóriamente de S
    real unif = uniform_rng(0,1);
    int idx = to_int(ceil(unif * (N_a+N_b)));
    Si_a[j] = S_merge[idx];
  }
  // Calcula média censurada de Si_a
  real sum = 0;
  int count = 0;
  for (j in 1:N_a) {
    if (Si_a[j] < c) {
      sum += Si_a[j];
      count += 1;
    }
  }
  real mean_censored_a = sum / count;

  // Pseudo amostra B
  array[N_b] real<upper=c> Si_b;
  for (j in 1:N_b) {
    // Amostra aleatóriamente de S
    real unif = uniform_rng(0,1);
    int idx = to_int(ceil(unif * (N_a+N_b)));
    Si_b[j] = S_merge[idx];
  }
  // Calcula média censurada de Si_b
  sum = 0;
  count = 0;
  for (j in 1:N_b) {
    if (Si_b[j] < c) {
      sum += Si_b[j];
      count += 1;
    }
  }
  real mean_censored_b = sum / count;

  // Calcula diferença entre médias censuradas
  real mean_diff = mean_censored_a - mean_censored_b;
}