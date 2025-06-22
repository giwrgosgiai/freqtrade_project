# Freqtrade Multi-Strategy Trading Setup

## Προετοιμασία

1. Εγκατάσταση Docker και Docker Compose
2. Κλωνοποίηση του repository

## Εκτέλεση Στρατηγικών

### Εμπορική Λειτουργία
```bash
# Για συγκεκριμένη στρατηγική
docker-compose run --rm nfi
docker-compose run --rm swing
docker-compose run --rm scalp
```

### Backtesting
```bash
# NFI Backtesting
docker-compose run --rm nfi_backtest
```

### Hyperopt
```bash
# NFI Hyperopt
docker-compose run --rm nfi_hyperopt
```

### Έλεγχος Στρατηγικής
```bash
# Έλεγχος στρατηγικής Scalp
docker-compose run --rm scalp_test_strategy
```

## Σημειώσεις
- Όλες οι στρατηγικές τρέχουν σε Dry Run mode
- Χρησιμοποιείστε με προσοχή σε πραγματικές συναλλαγές
- Απαιτείται σύνδεση με exchange και API keys

## Στρατηγικές
- NFI (Nostalgia For Infinity)
- Swing Trading
- Scalp Trading
- FreqAI
- Multi-Strategy

## Υποστήριξη
Ανατρέξτε στην τεκμηρίωση του Freqtrade για περισσότερες λεπτομέρειες. 