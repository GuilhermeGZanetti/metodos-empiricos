data {
    int<lower=0> N;      // Número de observações
    vector[N] x;         // Observações
}
parameters {
    real mu;             // Média da normal
    real<lower=0> sigma; // Desvio padrão da normal
}
model {
    mu ~ normal(5, 10);   // Prior
    sigma ~ normal(0, 10); // Prior
    x ~ normal(mu, sigma); // Likelihood
}