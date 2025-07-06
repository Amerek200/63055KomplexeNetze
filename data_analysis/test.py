import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def get_degree_distribution(degrees):
    """
    Calculates the probability distribution of node degrees.
    
    Args:
        degrees (list or np.array): A list of node degrees.
        
    Returns:
        tuple: A tuple containing two numpy arrays:
               - k: The unique degree values.
               - Pk: The probability of each degree value.
    """
    degree_counts = Counter(degrees)
    k = np.array(list(degree_counts.keys()))
    # Get counts and normalize to get probabilities
    Pk = np.array(list(degree_counts.values())) / len(degrees)
    
    # Sort by degree for plotting
    sort_indices = np.argsort(k)
    k = k[sort_indices]
    Pk = Pk[sort_indices]
    
    return k, Pk

def log_binning(k, Pk, factor=2.0):
    """
    Performs logarithmic binning of a probability distribution.
    
    This helps to visualize heavy-tailed distributions on a log-log plot
    by grouping points into exponentially larger bins and averaging them.
    
    Args:
        k (np.array): Degree values.
        Pk (np.array): Probability of each degree.
        factor (float): The base for the logarithmic bins (e.g., 2.0 for powers of two).
        
    Returns:
        tuple: A tuple containing two numpy arrays:
               - bin_centers: The geometric mean of the degrees in each bin.
               - bin_values: The average probability of the degrees in each bin.
    """
    # Define bin edges
    max_k = np.max(k)
    min_k = np.min(k)
    if min_k == 0:
        min_k = 1 # Avoid log(0) issues
        
    num_bins = int(np.log(max_k / min_k) / np.log(factor)) + 1
    bin_edges = np.logspace(np.log10(min_k), np.log10(max_k), num=num_bins, base=10.0)
    # Ensure the last bin edge includes the max value
    bin_edges[-1] = max_k + 1 

    # Digitize the k values into bins
    bin_indices = np.digitize(k, bin_edges)
    
    bin_centers = []
    bin_values = []
    
    for i in range(1, len(bin_edges)):
        # Find all data points that fall into the current bin
        mask = (bin_indices == i)
        if np.any(mask):
            # Use geometric mean for the x-value (bin center)
            # This is standard practice for log-binned data
            k_in_bin = k[mask]
            Pk_in_bin = Pk[mask]
            
            # Geometric mean for k
            center = np.exp(np.mean(np.log(k_in_bin)))
            # Arithmetic mean for Pk
            value = np.mean(Pk_in_bin)
            
            bin_centers.append(center)
            bin_values.append(value)
            
    return np.array(bin_centers), np.array(bin_values)

# --- Main Script ---

if __name__ == '__main__':
    # 1. Generate some dummy data that follows a broken power law
    # This simulates a network with two regimes of connectivity
    np.random.seed(42)
    s1 = np.random.zipf(a=1.5, size=10000) 
    s2 = np.random.zipf(a=2.7, size=1000) * 50 # Scale the second part
    degrees = np.concatenate((s1, s2))
    degrees = degrees[degrees > 0] # Ensure degrees are positive

    # 2. Get the raw and binned distributions
    k_raw, Pk_raw = get_degree_distribution(degrees)
    k_binned, Pk_binned = log_binning(k_raw, Pk_raw, factor=1.8)

    # 3. --- PLOTTING LOGIC ---
    # This is the key part to adapt to your code.
    
    # Assume you have already determined the slopes and the cutting point.
    # These values are for demonstration, based on the paper's values.
    gamma1 = 1.50
    gamma2 = 2.70
    
    # Find the cutting point in your binned data.
    # Here, we'll manually choose an index for demonstration.
    # In your code, this would correspond to the key (e.g., 12, 13, 14) from your dictionary.
    # Let's say the first regime ends around k=100.
    cut_k_value = 100
    cut_index = np.searchsorted(k_binned, cut_k_value)
    if cut_index >= len(k_binned):
        cut_index = len(k_binned) - 2 # Ensure we have at least one point for the second regime

    plt.figure(figsize=(10, 8))
    
    # Plot the binned data points
    plt.scatter(k_binned, Pk_binned, marker='o', color='C0', label='Binned Data', zorder=5)

    # --- Plotting the first regime ---
    if cut_index > 0:
        # Select the data for the first regime
        k1_data = k_binned[:cut_index]
        
        # **CRITICAL STEP: Calculate the constant C for the first line**
        # We anchor the line to the first data point in the binned set.
        anchor_k1 = k_binned[0]
        anchor_Pk1 = Pk_binned[0]
        C1 = anchor_Pk1 / (anchor_k1 ** -gamma1)
        
        # Generate k values for plotting the line
        k1_fit = np.linspace(k_binned[0], k_binned[cut_index-1], 100)
        Pk1_fit = C1 * (k1_fit ** -gamma1)
        
        plt.plot(k1_fit, Pk1_fit, 'r--', linewidth=2, label=f'Slope γ1 = -{gamma1:.2f}')

    # --- Plotting the second regime ---
    if cut_index < len(k_binned):
        # Select the data for the second regime
        k2_data = k_binned[cut_index:]
        
        # **CRITICAL STEP: Calculate the constant C for the second line**
        # We anchor this line to the first point of its regime.
        anchor_k2 = k_binned[cut_index]
        anchor_Pk2 = Pk_binned[cut_index]
        C2 = anchor_Pk2 / (anchor_k2 ** -gamma2)
        
        # Generate k values for plotting the line
        k2_fit = np.linspace(k_binned[cut_index], k_binned[-1], 100)
        Pk2_fit = C2 * (k2_fit ** -gamma2)
        
        plt.plot(k2_fit, Pk2_fit, 'g--', linewidth=2, label=f'Slope γ2 = -{gamma2:.2f}')

    # --- Final plot formatting ---
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Degree k', fontsize=14)
    plt.ylabel('P(k)', fontsize=14)
    plt.title('Degree Distribution with Two Power-Law Regimes', fontsize=16)
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.show()

