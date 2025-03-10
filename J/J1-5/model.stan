data {
    int<lower=0> N;      // Número de observações
    vector[N] y;         // Observações de sentenças
}
parameters {
    real<lower=min(y), upper=max(y)> mu;             // Média da normal
    real<lower=0, upper=max(y)-min(y)> sigma; // Desvio padrão da normal
}
model {
    // Likelihood
    y ~ normal(mu, sigma);
}