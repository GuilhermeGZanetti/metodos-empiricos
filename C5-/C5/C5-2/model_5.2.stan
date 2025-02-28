data {
  int N_a;
  real mu_a;
  real sigma_a; 
  int N_b;
  real mu_b;
  real sigma_b;
}
generated quantities {
  array[N_a] real Si_a;
  array[N_b] real Si_b;
  for (j in 1:N_a) {
    Si_a[j] = normal_rng(mu_a, sigma_a);
  }
  for (j in 1:N_b) {
    Si_b[j] = normal_rng(mu_b, sigma_b);
  }
  real IQR_A = quantile(Si_a, 0.75) - quantile(Si_a, 0.25);
  real IQR_B = quantile(Si_b, 0.75) - quantile(Si_b, 0.25);
  real delta_IQR = IQR_A - IQR_B;
}