data {
  int N;
  real mu;
  real sigma; 
}
generated quantities {
  array[N] real Si;
  for (j in 1:N) {
    Si[j] = normal_rng(mu, sigma);
  }
  real IQR = quantile(Si, 0.75) - quantile(Si, 0.25);
}