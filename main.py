import math
import random
import time
import sys

from utils import mod_pow, mod_inverse, linear_search_dlog, baby_step_giant_step, pollard_rho_dlog, pollard_rho_distinguished_points

def run_algorithm_with_timing(algorithm, g, h, p, name, **kwargs):
    print(f"\nRunning {name}...")
    start_time = time.time()
    
    if kwargs.get('num_runs', 1) > 1:
        if "Pollard" in name or "Distinguished" in name:
            result, total_iterations, successful_runs, num_runs, avg_iterations, first_hit_time = algorithm(g, h, p, **kwargs)
            success_rate = (successful_runs / num_runs) * 100
        else:
            result, iterations = algorithm(g, h, p, **kwargs)
            success_rate = None
            avg_iterations = iterations
            first_hit_time = None
    else:
        if "Pollard" in name or "Distinguished" in name:
            result, iterations, first_hit_time = algorithm(g, h, p, **kwargs)
            success_rate = None
            avg_iterations = iterations
        else:
            result, iterations = algorithm(g, h, p, **kwargs)
            success_rate = None
            avg_iterations = iterations
            first_hit_time = None
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"{name} result: {result}")
    print(f"{name} took {elapsed_time:.4f} seconds")
    if first_hit_time is not None:
        print(f"First hit found in {first_hit_time:.4f} seconds")
    
    if result is not None:
        verification = mod_pow(g, result, p) == h
        print(f"Verification: {'Correct' if verification else 'Incorrect'}")
    
    if success_rate is not None:
        return result, elapsed_time, success_rate, avg_iterations, p, (g, h), first_hit_time
    else:
        return result, elapsed_time, 100 if result is not None else 0, avg_iterations, p, (g, h), first_hit_time


def print_results_table(results):
    """Print a well-formatted table of algorithm results with statistics"""
    print("\n+------------------------+------------+------------+------------+------------+------------+----------------+------------+------------+")
    print("| Algorithm              | Prime Size | Time (s)   | First Hit(s)| Success (%)| Avg Iters  | Found Value    | Prime (p)  | Inputs (g,h)|")
    print("+------------------------+------------+------------+------------+------------+------------+----------------+------------+------------+")
    
    for result in results:
        algo_name, prime_size, time_taken, success_rate, avg_iterations, found_value, p, gh, first_hit_time = result
        value_str = str(found_value) if found_value is not None else "N/A"
        if len(value_str) > 14:
            value_str = value_str[:11] + "..."
        
        p_str = str(p)
        if len(p_str) > 10:
            p_str = p_str[:7] + "..."
            
        gh_str = f"{gh[0]},{gh[1]}"
        if len(gh_str) > 10:
            gh_str = gh_str[:7] + "..."
        
        first_hit_str = f"{first_hit_time:.4f}" if first_hit_time is not None else "N/A"
            
        print(f"| {algo_name:<22} | {prime_size:<10} | {time_taken:<10.4f} | {first_hit_str:<10} | {success_rate:<10.1f} | {avg_iterations:<10.1f} | {value_str:<14} | {p_str:<10} | {gh_str:<10} |")
    
    print("+------------------------+------------+------------+------------+------------+------------+----------------+------------+------------+")


if __name__ == "__main__":
    results = []
    num_pollard_runs = 10000
    
    print("===== Small Prime Example =====")
    p_small = 101
    g_small = 3
    h_small = 37
    print(f"Using p = {p_small}, g = {g_small}, h = {h_small}")
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(linear_search_dlog, g_small, h_small, p_small, "Linear Search")
    results.append(("Linear Search", "Small", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(baby_step_giant_step, g_small, h_small, p_small, "Baby-step Giant-step")
    results.append(("Baby-step Giant-step", "Small", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(pollard_rho_dlog, g_small, h_small, p_small, "Pollard's Rho")
    results.append(("Pollard's Rho", "Small", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(pollard_rho_distinguished_points, g_small, h_small, p_small, "Distinguished Points")
    results.append(("Distinguished Points", "Small", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    print("\n===== Multiple Pollard Trials on Small Prime =====")
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(
        pollard_rho_dlog, g_small, h_small, p_small, "Pollard's Rho (Multiple)", num_runs=num_pollard_runs
    )
    results.append(("Pollard's Rho (Multi)", "Small", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(
        pollard_rho_distinguished_points, g_small, h_small, p_small, "Distinguished Points (Multiple)", num_runs=num_pollard_runs
    )
    results.append(("Dist. Points (Multi)", "Small", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    print("\n===== Medium Prime Example =====")
    p_medium = 9973
    g_medium = 5
    # Using fixed value instead of random
    x_medium = 1235  # Fixed value
    h_medium = mod_pow(g_medium, x_medium, p_medium)
    print(f"Using p = {p_medium}, g = {g_medium}")
    print(f"Secret x = {x_medium}, h = {h_medium}")
    
    print("Linear Search would take too long, skipping...")
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(baby_step_giant_step, g_medium, h_medium, p_medium, "Baby-step Giant-step")
    results.append(("Baby-step Giant-step", "Medium", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(pollard_rho_dlog, g_medium, h_medium, p_medium, "Pollard's Rho")
    results.append(("Pollard's Rho", "Medium", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(pollard_rho_distinguished_points, g_medium, h_medium, p_medium, "Distinguished Points")
    results.append(("Distinguished Points", "Medium", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    print("\n===== Multiple Pollard Trials on Medium Prime =====")
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(
        pollard_rho_dlog, g_medium, h_medium, p_medium, "Pollard's Rho (Multiple)", num_runs=num_pollard_runs
    )
    results.append(("Pollard's Rho (Multi)", "Medium", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(
        pollard_rho_distinguished_points, g_medium, h_medium, p_medium, "Distinguished Points (Multiple)", num_runs=num_pollard_runs
    )
    results.append(("Dist. Points (Multi)", "Medium", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    print("\n===== Large Prime Example =====")
    p_large = 104729
    g_large = 5
    # Using fixed value instead of random
    x_large = 12345  # Fixed value
    h_large = mod_pow(g_large, x_large, p_large)
    print(f"Using p = {p_large}, g = {g_large}")
    print(f"Secret x = {x_large}, h = {h_large}")
    
    print("Linear Search and Baby-step Giant-step would take too long, skipping...")
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(pollard_rho_dlog, g_large, h_large, p_large, "Pollard's Rho")
    results.append(("Pollard's Rho", "Large", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(pollard_rho_distinguished_points, g_large, h_large, p_large, "Distinguished Points")
    results.append(("Distinguished Points", "Large", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    print("\n===== Multiple Pollard Trials on Large Prime =====")
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(
        pollard_rho_dlog, g_large, h_large, p_large, "Pollard's Rho (Multiple)", num_runs=num_pollard_runs
    )
    results.append(("Pollard's Rho (Multi)", "Large", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    result, time_taken, success_rate, avg_iterations, p, gh, first_hit = run_algorithm_with_timing(
        pollard_rho_distinguished_points, g_large, h_large, p_large, "Distinguished Points (Multiple)", num_runs=num_pollard_runs
    )
    results.append(("Dist. Points (Multi)", "Large", time_taken, success_rate, avg_iterations, result, p, gh, first_hit))
    
    # Print comprehensive summary table
    print_results_table(results)