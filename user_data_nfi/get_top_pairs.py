import requests
import json
import os
import subprocess
import sys

def get_top_binance_pairs_usdt(limit=50):
    """
    Επιστρέφει τα κορυφαία USDT ζεύγη από το Binance με βάση το volume. 
    Φιλτράρει σταθερά νομίσματα και εξαιρεί μη επιθυμητά ζεύγη.
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Φιλτράρισμα ζευγών USDT
        usdt_pairs = [
            item for item in data 
            if item['symbol'].endswith('USDT') 
            and not any(stable in item['symbol'] for stable in ['BUSD', 'TUSD', 'USDC', 'DAI'])
            and not any(x in item['symbol'] for x in ['DOWN', 'UP', 'BEAR', 'BULL'])
        ]
        
        # Ταξινόμηση με βάση το quote volume
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        
        # Επιστροφή των κορυφαίων ζευγών
        top_pairs = [f"{item['symbol'][:-4]}/USDT" for item in sorted_pairs[:limit]]
        
        return top_pairs
    
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη των ζευγών: {e}", file=sys.stderr)
        return []

def update_config_with_pairs(pairs):
    """
    Ενημερώνει το config.json με τα νέα ζεύγη
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    try:
        # Φόρτωση του υπάρχοντος config
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Ενημέρωση του pair_whitelist
        config['pair_whitelist'] = pairs
        
        # Προσαρμογή του pairlists
        config['pairlists'] = [
            {
                "method": "StaticPairList",
                "pair_whitelist": pairs
            }
        ]
        
        # Αποθήκευση του ενημερωμένου config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"Ενημερώθηκαν {len(pairs)} ζεύγη στο configuration", file=sys.stderr)
        print("Κορυφαία ζεύγη:", file=sys.stderr)
        for pair in pairs:
            print(f"  - {pair}", file=sys.stderr)
    
    except Exception as e:
        print(f"Σφάλμα κατά την ενημέρωση του config: {e}", file=sys.stderr)

def run_backtests():
    """
    Εκτέλεση backtesting μέσω Docker
    """
    try:
        # Εκτέλεση backtesting μέσω Docker
        cmd = [
            "docker", "run", "--rm", 
            "-v", f"{os.path.dirname(__file__)}:/freqtrade/user_data",
            "freqtradeorg/freqtrade:stable", 
            "backtesting", 
            "--config", "/freqtrade/user_data/config.json", 
            "--strategy", "NostalgiaForInfinityX6", 
            "--strategy-path", "/freqtrade/user_data/strategies", 
            "--timerange", "20240101-20240601"
        ]
        
        print(f"Εντολή Docker: {' '.join(cmd)}", file=sys.stderr)
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Εκτύπωση πλήρους εξόδου
        print("Έξοδος stdout:", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        
        print("Έξοδος stderr:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        
        # Επιστροφή της εξόδου του backtesting
        return result.stdout
    
    except Exception as e:
        print(f"Γενικό σφάλμα: {e}", file=sys.stderr)
        return ""

def main():
    # Λήψη των κορυφαίων ζευγών
    pairs = get_top_binance_pairs_usdt(limit=50)
    
    # Ενημέρωση του configuration με τα ζεύγη
    update_config_with_pairs(pairs)
    
    # Εκτέλεση backtesting
    backtest_results = run_backtests()
    
    # Εμφάνιση αποτελεσμάτων
    print("\nΑποτελέσματα Backtesting:")
    print(backtest_results)

if __name__ == "__main__":
    main() 