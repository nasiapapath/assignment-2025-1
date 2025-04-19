def s_j(j, s, t):
    binary = format(j, f'0{s-1}b')  
    balanced = ''.join('-' if bit == '1' else '+' for bit in binary)
    s_j = '0' * t + '-' + balanced
    return s_j
import re

def rightest_block(s):
    r= list(re.finditer(r'0-[-+]*\+', s))
    l = list(re.finditer(r'\+[-+]*-0?', s))

    last_r = r[-1] if r else None
    last_l = l[-1] if l else None

    if last_r and (not last_l or last_r.start() > last_l.start()):
        return ('R', last_r.start(), last_r.end())
    elif last_l:
        return ('L', last_l.start(), last_l.end())
    else:
        return (None, None, None)
    
def replacement(s, block, start, end):
    if block == 'R':
        previous = s[:start]
        body = s[start+1:end-1]
        replaced = '-' + '+' * len(body) + '0'
        return previous + replaced + s[end:]
    elif block == 'L':
        previous = s[:start]
        body = s[start+1:end-1]
        replaced = '0' + '+' * len(body) + '+'
        return previous + replaced + s[end:]
    else:
        return s  

def create_chain(s):
    chain = [s]
    current = s
    while True:
        block, start, end = rightest_block(current)
        if block is None:
            break
        current = replacement(current, block, start, end)
        chain.append(current)
    return chain

def balanced_to_binary_string(balanced):
    return ''.join('1' if ch == '0' else '0' for ch in balanced)

def binary_string_to_decimal(binary):
    return int(binary, 2)

def s_chain_to_graph(s):
    chain = create_chain(s)
    binary_nodes = [balanced_to_binary_string(b) for b in chain]
    decimal_nodes = [binary_string_to_decimal(b) for b in binary_nodes]
    return decimal_nodes

def create_all_s(s, t):
    sigma = []
    for j in range(2 ** (s - 1)):
        sigma.append(s_j(j, s, t))
    return sigma

import itertools

def create_graph_peaks(s, t):
    n = s + t
    peaks = set()

    for bits in itertools.permutations('1'*s + '0'*t, n):
        bin_str = ''.join(bits)
        decimal = int(bin_str, 2)
        peaks.add(decimal)

    return sorted(peaks)

def homogeneous(x, y):
    return bin(x ^ y).count('1') == 1

def genlex_compare(a, u):
    a_bin = format(a, 'b').zfill(max(len(bin(a)), len(bin(u))))
    u_bin = format(a, 'b').zfill(max(len(bin(a)), len(bin(u))))
    return a_bin < u_bin

def genlex_path(path):
    return all(genlex_compare(path[i], path[i+1]) for i in range(len(path)-1))

def homogeneous_genlex_path(path):
    for i in range(1, len(path)):
        if not homogeneous(path[i-1], path[i]):
            return False
     return genlex_path(path)

def dfs(current, visited, path, peaks, results):
     visited.add(current)
     path.append(current)
     if len(path) == len(peaks):
        results.append(path.copy())

     else:
        for neighbor in peaks:
            if neighbor not in visited:
                if homogeneous(current, neighbor):
                    if len(path) == 0 or genlex_compare(path[-1], neighbor):
                        dfs(neighbor, visited, path, peaks, results)

     visited.remove(current)
     path.pop()

def find_all_genlex_paths(peaks):
    results = []
    for start in peaks:
        dfs(start, set(), [], peaks, results)
    return results

if __name__ == "__main__":
    s = int(input("Δώσε το πλήθος των 1 (s): "))
    t = int(input("Δώσε το πλήθος των 0 (t): "))

    sigma = create_all_s(s, t)

    for idx, s in enumerate(sigma):
        path = s_chain_to_graph(s)
        print(f"Path from σ_{idx} ({s}): {path}")
        is_valid = homogeneous_genlex_path(path)
        print(" Ομογενής Genlex διαδρομή" if is_valid else " Δεν είναι ομογενής")

    print(" Πλήρεις Ομογενείς Genlex Διαδρομές με DFS:")
    peaks = create_graph_peaks(s, t)
    full_paths = find_all_genlex_paths(peaks)
    if full_paths:
        for p in full_paths:
            print(p)
    else:
        print(" Δεν βρέθηκαν πλήρεις διαδρομές.")
       
