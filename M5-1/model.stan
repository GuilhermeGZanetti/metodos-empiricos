data {
  real lower_bound;
  real upper_bound; 
}

parameters {
  real<lower=-5, upper=30> x;
}

model {
  x ~ uniform(lower_bound, upper_bound); 
}