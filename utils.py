import math
import random
import time
import sys


def mod_pow(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result


def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def linear_search_dlog(g, h, p):
    value = 1
    iterations = 0
    for x in range(p):
        iterations += 1
        if x % max(1, p // 10) == 0:
            sys.stdout.write(f"\rLinear Search: {x}/{p} ({x/p*100:.1f}%)")
            sys.stdout.flush()
        
        if value == h:
            sys.stdout.write(f"\rLinear Search: Complete       \n")
            return x, iterations
        value = (value * g) % p
    
    sys.stdout.write(f"\rLinear Search: Complete       \n")
    return None, iterations


def baby_step_giant_step(g, h, p):
    m = math.ceil(math.sqrt(p))
    iterations = 0
    
    print(f"Baby Steps: Computing table with {m} entries")
    baby_steps = {}
    for j in range(m):
        if j % max(1, m // 10) == 0:
            sys.stdout.write(f"\rBaby Steps: {j}/{m} ({j/m*100:.1f}%)")
            sys.stdout.flush()
            
        baby_steps[mod_pow(g, j, p)] = j
        iterations += 1
    
    sys.stdout.write(f"\rBaby Steps: Complete         \n")
    
    g_inv_m = mod_pow(g, p - 1 - m, p)
    
    print(f"Giant Steps: Searching")
    value = h
    for i in range(m):
        if i % max(1, m // 10) == 0:
            sys.stdout.write(f"\rGiant Steps: {i}/{m} ({i/m*100:.1f}%)")
            sys.stdout.flush()
            
        if value in baby_steps:
            sys.stdout.write(f"\rGiant Steps: Complete         \n")
            return i * m + baby_steps[value], iterations + i
        value = (value * g_inv_m) % p
        iterations += 1
    
    sys.stdout.write(f"\rGiant Steps: Complete         \n")
    return None, iterations

def pollard_rho_dlog(g, h, p, max_iterations=None, num_runs=1):
    n = p - 1
    
    def f(x_pair):
        x, a, b = x_pair
        subset = x % 3
        
        if subset == 0:
            x_new = (x * g) % p
            a_new = (a + 1) % n
            b_new = b
        elif subset == 1:
            x_new = (x * h) % p
            a_new = a
            b_new = (b + 1) % n
        else:
            x_new = (x * x) % p
            a_new = (2 * a) % n
            b_new = (2 * b) % n
        
        return (x_new, a_new, b_new)
    
    if max_iterations is None:
        max_iterations = 3 * int(math.sqrt(p))
    
    # Track statistics for multiple runs
    successful_runs = 0
    total_iterations = 0
    best_result = None
    first_hit_time = None
    start_time = time.time()
    
    for run in range(1, num_runs + 1):
        # Random starting point
        a0 = random.randint(1, n - 1)
        b0 = random.randint(1, n - 1)
        x0 = (mod_pow(g, a0, p) * mod_pow(h, b0, p)) % p
        
        # Initialize tortoise and hare
        tortoise = (x0, a0, b0)
        hare = f(tortoise)
        
        if num_runs == 1:
            print(f"Pollard's Rho: Running")
        
        iterations = 0
        
        # Find the collision
        while tortoise[0] != hare[0] and iterations < max_iterations:
            tortoise = f(tortoise)
            hare = f(f(hare))
            iterations += 1
            
            if num_runs == 1 and iterations % max(1, max_iterations // 10) == 0:
                sys.stdout.write(f"\rPollard's Rho: {iterations}/{max_iterations} ({iterations/max_iterations*100:.1f}%)")
                sys.stdout.flush()
        
        total_iterations += iterations
        
        if num_runs == 1:
            sys.stdout.write(f"\rPollard's Rho: Complete                        \n")
        
        if iterations >= max_iterations:
            if num_runs == 1:
                print(f"Reached maximum iterations without finding a collision")
            continue
        
        # Extract the discrete logarithm
        a_diff = (hare[1] - tortoise[1]) % n
        b_diff = (tortoise[2] - hare[2]) % n
        
        # Make sure b_diff is invertible
        gcd, _, _ = extended_gcd(b_diff, n)
        if gcd != 1:
            continue
        
        # Compute the result
        x = (a_diff * mod_inverse(b_diff, n)) % n
        
        # Verify the result
        if mod_pow(g, x, p) == h:
            successful_runs += 1
            # Record first success time if not already set
            if first_hit_time is None:
                first_hit_time = time.time() - start_time
            
            best_result = x
            if num_runs == 1:
                return best_result, iterations, first_hit_time
        
    if num_runs > 1:
        avg_iterations = total_iterations / num_runs if num_runs > 0 else 0
        success_rate = successful_runs / num_runs * 100
        print(f"Pollard's Rho: {successful_runs}/{num_runs} successful runs ({success_rate:.1f}%)")
        print(f"Pollard's Rho: Average {avg_iterations:.1f} iterations per run")
        
        # If no successful hits, set first_hit_time to None
        if first_hit_time is None:
            first_hit_time = None
        
        return best_result, total_iterations, successful_runs, num_runs, avg_iterations, first_hit_time
    
    return best_result, total_iterations, first_hit_time


def pollard_rho_distinguished_points(g, h, p, max_iterations=None, num_runs=1):
    n = p - 1
    
    trailing_zero_bits = max(1, int(math.log2(p) / 8))
    distinguished_mask = (1 << trailing_zero_bits) - 1
    
    def is_distinguished(x):
        return (x & distinguished_mask) == 0
    
    def f(x_pair):
        x, a, b = x_pair
        subset = x % 3
        
        if subset == 0:
            x_new = (x * g) % p
            a_new = (a + 1) % n
            b_new = b
        elif subset == 1:
            x_new = (x * h) % p
            a_new = a
            b_new = (b + 1) % n
        else:
            x_new = (x * x) % p
            a_new = (2 * a) % n
            b_new = (2 * b) % n
        
        return (x_new, a_new, b_new)
    
    if max_iterations is None:
        max_iterations = 3 * int(math.sqrt(p))
    
    # Track statistics for multiple runs
    successful_runs = 0
    total_iterations = 0
    best_result = None
    first_hit_time = None
    start_time = time.time()
    
    for run in range(1, num_runs + 1):
        # Random starting point
        a0 = random.randint(1, n - 1)
        b0 = random.randint(1, n - 1)
        x0 = (mod_pow(g, a0, p) * mod_pow(h, b0, p)) % p
        
        # Store distinguished points
        distinguished_points = {}
        
        # Start walk
        current = (x0, a0, b0)
        
        if num_runs == 1:
            print(f"Distinguished Points: Running")
        
        run_iterations = 0
        x_result = None
        
        for iteration in range(max_iterations):
            if num_runs == 1 and iteration % max(1, max_iterations // 10) == 0:
                sys.stdout.write(f"\rDistinguished Points: {iteration}/{max_iterations} ({iteration/max_iterations*100:.1f}%)")
                sys.stdout.flush()
                
            current = f(current)
            x, a, b = current
            run_iterations += 1
            
            if is_distinguished(x):
                if x in distinguished_points:
                    # Collision found
                    a_old, b_old = distinguished_points[x]
                    a_diff = (a - a_old) % n
                    b_diff = (b_old - b) % n
                    
                    # Make sure b_diff is invertible
                    gcd, _, _ = extended_gcd(b_diff, n)
                    if gcd != 1:
                        break
                    
                    # Compute the result
                    x_result = (a_diff * mod_inverse(b_diff, n)) % n
                    
                    # Verify the result
                    if mod_pow(g, x_result, p) == h:
                        successful_runs += 1
                        # Record first success time if not already set
                        if first_hit_time is None:
                            first_hit_time = time.time() - start_time
                        
                        best_result = x_result
                        if num_runs == 1:
                            sys.stdout.write(f"\rDistinguished Points: Complete                        \n")
                            return best_result, run_iterations, first_hit_time
                    break
                else:
                    # Store the distinguished point
                    distinguished_points[x] = (a, b)
        
        total_iterations += run_iterations
        
        if num_runs == 1:
            sys.stdout.write(f"\rDistinguished Points: Complete                        \n")
    
    if num_runs > 1:
        avg_iterations = total_iterations / num_runs if num_runs > 0 else 0
        success_rate = successful_runs / num_runs * 100
        print(f"Distinguished Points: {successful_runs}/{num_runs} successful runs ({success_rate:.1f}%)")
        print(f"Distinguished Points: Average {avg_iterations:.1f} iterations per run")
        
        # If no successful hits, set first_hit_time to None
        if first_hit_time is None:
            first_hit_time = None
            
        return best_result, total_iterations, successful_runs, num_runs, avg_iterations, first_hit_time
    
    return best_result, total_iterations, first_hit_time

