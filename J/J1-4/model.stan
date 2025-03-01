data {
    int<lower=0> N;      // Número de observações
    vector[N] x;         // Observações
}
parameters {
    real<lower=min(x), upper=max(x)> mu;             // Média da normal
    real<lower=0, upper=max(x)-min(x)> sigma; // Desvio padrão da normal
}
model {
    x ~ normal(mu, sigma); // Likelihood
}