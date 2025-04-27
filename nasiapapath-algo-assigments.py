import re
import itertools
import argparse

def s_j(j, s, t):
    binary = format(j, f'0{s-1}b')  
    balanced = ''.join('-' if bit == '1' else '+' for bit in binary)
    s_j = '0' * t + '-' + balanced
    return s_j

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
        body = '-' + '+' * (end - start - 2) + '0'
        return s[:start] + body + s[end:]
    elif block == 'L':
        previous = s[:start]
        body = '0' + '+' * (end - start - 2) + '+'
        return s[:start] + body + s[end:]
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

def create_all_peaks(s, t):
    n = s + t
    elements = '1' * s + '0' * t
    unique_numbers = set(int(''.join(p), 2) for p in itertools.permutations(elements))
    return sorted(unique_numbers)

def homogeneous(x, y):
    return bin(x ^ y).count('1') == 1

def genlex_compare(a, u):
    a_bin = format(a, 'b').zfill(32)
    u_bin = format(a, 'b').zfill(32)
    return a_bin < u_bin

def dfs(node, visited, path, peaks, results):
     visited.add(node)
     path.append(node)
     if len(path) == len(peaks):
        results.append(path.copy())

     else:
        for neighbor in peaks:
            if neighbor not in visited and homogeneous(node, neighbor) and genlex_compare(path[-1], neighbor):
                     dfs(neighbor, visited, path, peaks, results)

     path.pop()
     visited.remove(node)

def find_all_genlex_paths(peaks):
    results = []
    for start in peaks:
        dfs(start, set(), [], peaks, results)
    return results

def print_path(path):
    print(path)

def create_graph(s, t):
    peaks = create_all_peaks(s, t)
    connections = {}

    for a in peaks:
        neighbors = []
        for b in peaks:
            if a != b and homogeneous(a, b):
                neighbors.append(b)
        connections[a] = neighbors

    for node in connections:
        print(f"{node} -> {sorted(connections[node])}")

def create_bts_paths(s, t):
    for j in range(2 ** (s-1)):
        sigma = s_j(j, s, t)
        chain = create_chain(sigma)
        binary_chain = [balanced_to_binary_string(s) for seq in chain]
        decimal_chain = [binary_string_to_decimal(b) for b in binary_chain]

        print(decimal_chain)

def create_dfs_path(s, t, start_node=None):
    peaks = create_all_peaks(s, t)
    paths = []

    if start_node is not None:
        if start_node not in peaks:
            print(f"Start node {start_node} is not a valid peak.")
            return
        dfs(start_node, set(), [], peaks, paths)
    else:
        paths = find_all_genlex_paths(peaks)

    for path in paths:
        print_path(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("s", type=int, help="1")
    parser.add_argument("t", type=int, help="0")
    parser.add_argument("mode", choices=["graph", "dfs", "bts"])
    parser.add_argument("start", type=int, nargs="?")

    args = parser.parse_args()

    if args.mode == "graph":
        create_graph(args.s, args.t)
    elif args.mode == "bts":
        create_bts_paths(args.s, args.t)
    elif args.mode == "dfs":
        create_dfs_path(args.s, args.t, args.start)
