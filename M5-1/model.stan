data {
  int<lower=0> N;
  vector[N] y;
}

parameters {
  real <upper = min(y)> alpha;
  real <lower = max(y)> beta;
}

model {
  alpha ~ normal(min(y), max(y)/2) T[, min(y)];
  beta ~ normal(max(y), max(y)/2) T[max(y), ];
  y ~ uniform(alpha, beta);
}