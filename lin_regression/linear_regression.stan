data {
    int<lower=0> N;       // Número de pontos de dados
    vector[N] x;       // Variável preditora
    vector[N] y;;             // Variável resposta
}
parameters {
    real alpha;            // Intercepto
    real beta;             // Coeficiente da regressão
    real<lower=0> sigma;   // Desvio padrão dos resíduos
}
model {    
    y ~ normal(alpha + x * beta, sigma);  // Likelihood
}
