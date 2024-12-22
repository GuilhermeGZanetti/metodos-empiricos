data {
    int<lower=0> N;      // Número de observações
    vector[N] y;         // Observações
}
parameters {
    real mu;             // Média da normal
    real<lower=0> sigma; // Desvio padrão da normal
}
model {
    y ~ normal(mu, sigma); // Likelihood
}