import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.benchmark as benchmark
device = "cuda" if torch.cuda.is_available() else "cpu"


#example usage
query, key, value = torch.randn(2, 3, 8, device=device), torch.randn(2, 3, 8, device=device), torch.randn(2, 3, 8, device=device)

# this is an SDPA -> caled dot product attention
F.scaled_dot_product_attention(query, key, value)

# Explicit Dispatcher Control

## While the function will implicitly dispatch to one of the three implementations, the user can also explicitly control the dispatch via the use of a context manager. This context manager allows users to explicitly disable certain implementations. If a user wants to ensure the function is indeed using the fastest implementation for their specific inputs, the context manager can be used to sweep through measuring performance.

def benchmark_torch_function_in_microseconds(f, *args, **kwargs):
    t0 = benchmark.Timer(
            stmt = "f(*args, **kwargs)",
            globals = {"args": args, "kwargs": kwargs, "f":f}
            )
    return t0

# lets define the hyper-parameters os our inputs
batch_size = 32
max_squence_len = 1024
num_heads = 32
embed_dimension = 32

dtype = torch.float16

query = torch.rand(batch_size, num_heads, max_squence_len, 
                   embed_dimension, device=device, dtype=dtype)
key = torch.rand(batch_size, num_heads, max_squence_len, 
                   embed_dimension, device=device, dtype=dtype)
value = torch.rand(batch_size, num_heads, max_squence_len, 
                   embed_dimension, device=device, dtype=dtype)

#quick benchmark

bb = benchmark_torch_function_in_microseconds(F.scaled_dot_product_attention(query, key, value))

bb.blocked_autorange()

print(f"The default implementation runs in {benchmark_torch_function_in_microseconds(F.scaled_dot_product_attention(query, key, value)):.3f} microseconds")

