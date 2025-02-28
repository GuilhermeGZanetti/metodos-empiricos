data {
  int<lower = 0> N;
  array[N] real x;
  array[N] real y;
}
transformed data {
  simplex[N] uniform = rep_vector(1.0 / N, N);
  array[N] int<lower = 1, upper = N> boot_idxs;
  for (n in 1:N)
    boot_idxs[n] = categorical_rng(uniform);
}
parameters {
  real corr_mu;
  real<lower = 0> sigma;
}
model {
  array[N] real this_x = x;//x[boot_idxs];
  array[N] real this_y = y;//y[boot_idxs];
  real mu_x = mean(this_x);
  real mu_y = mean(this_y);
  real cov_xy = 0;
  for (n in 1:N)
    cov_xy += (this_x[n] - mu_x) * (this_y[n] - mu_y);
  cov_xy /= (N - 1);
  real corr = cov_xy / (sd(this_x) * sd(this_y));
  
  corr ~ normal(corr_mu, sigma);
}