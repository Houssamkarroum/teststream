import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(page_title="Fibonacci Comparison", layout="wide")

# --- Functions for Fibonacci ---
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_dynamic(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fibonacci_dynamic(n - 1, memo) + fibonacci_dynamic(n - 2, memo)
    return memo[n]

def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def measure_execution_time(n_values):
    recursive_times = []
    dynamic_times = []
    iterative_times = []
    
    for n in n_values:
        # Recursive Simple
        start_time = time.time()
        if n <= 35:  # Limit for the recursive approach
            fibonacci_recursive(n)
        recursive_times.append(time.time() - start_time)
        
        # Recursive with Dynamic Programming
        start_time = time.time()
        fibonacci_dynamic(n, {})
        dynamic_times.append(time.time() - start_time)
        
        # Iterative
        start_time = time.time()
        fibonacci_iterative(n)
        iterative_times.append(time.time() - start_time)
    
    return recursive_times, dynamic_times, iterative_times

# --- User Interface ---
st.title("Fibonacci Sequence: Comparing Implementations")

# Bloc 1: Versions of Fibonacci
st.subheader("1. Fibonacci Implementations")

col1, col2, col3 = st.columns(3)

with col1:
    st.code("""
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
""", language="python")

with col2:
    st.code("""
def fibonacci_dynamic(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fibonacci_dynamic(n - 1, memo) + fibonacci_dynamic(n - 2, memo)
    return memo[n]
""", language="python")

with col3:
    st.code("""
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
""", language="python")

# Bloc 2: Entire Code
st.subheader("2. Entire Application Code")
global_code = """
import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt

# --- Functions for Fibonacci ---
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_dynamic(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fibonacci_dynamic(n - 1, memo) + fibonacci_dynamic(n - 2, memo)
    return memo[n]

def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def measure_execution_time(n_values):
    recursive_times = []
    dynamic_times = []
    iterative_times = []
    
    for n in n_values:
        # Recursive Simple
        start_time = time.time()
        if n <= 35:  # Limit for the recursive approach
            fibonacci_recursive(n)
        recursive_times.append(time.time() - start_time)
        
        # Recursive with Dynamic Programming
        start_time = time.time()
        fibonacci_dynamic(n, {})
        dynamic_times.append(time.time() - start_time)
        
        # Iterative
        start_time = time.time()
        fibonacci_iterative(n)
        iterative_times.append(time.time() - start_time)
    
    return recursive_times, dynamic_times, iterative_times

# --- User Interface ---
st.title("Fibonacci Sequence: Comparing Implementations")
# UI continues as shown in the application code.
# Bloc 3: Interval Selection
st.subheader("3. Select Range for n")
n_min, n_max = st.slider("Choose the range of n:", 1, 50, (5, 35))
n_values = range(n_min, n_max + 1)

# Measure Execution Times
recursive_times, dynamic_times, iterative_times = measure_execution_time(n_values)

# Prepare Data for Table
data = {
    "n": n_values,
    "Recursive Simple (s)": recursive_times,
    "Dynamic Recursive (s)": dynamic_times,
    "Iterative (s)": iterative_times,
}
df = pd.DataFrame(data)

# Bloc 4: Results
st.subheader("4. Results")

# Plotting Results
st.write("### Execution Time for Each Implementation")
plt.figure(figsize=(10, 6))
plt.plot(n_values, recursive_times, label="Recursive Simple", marker='o', linestyle='--')
plt.plot(n_values, dynamic_times, label="Dynamic Recursive", marker='s', linestyle='-')
plt.plot(n_values, iterative_times, label="Iterative", marker='^', linestyle='-.')

plt.title("Comparison of Execution Times for Fibonacci Implementations")
plt.xlabel("n (Fibonacci size)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid()
st.pyplot(plt)

# Displaying the Table
st.write("### Comparison Table of Execution Times")
st.dataframe(df, use_container_width=True)
"""
st.code(global_code, language="python")

# Bloc 3: Interval Selection
st.subheader("3. Select Range for n")
n_min, n_max = st.slider("Choose the range of n:", 1, 50, (5, 35))
n_values = range(n_min, n_max + 1)

# Measure Execution Times
recursive_times, dynamic_times, iterative_times = measure_execution_time(n_values)

# Prepare Data for Table
data = {
    "n": n_values,
    "Recursive Simple (s)": recursive_times,
    "Dynamic Recursive (s)": dynamic_times,
    "Iterative (s)": iterative_times,
}
df = pd.DataFrame(data)

# Bloc 4: Results
st.subheader("4. Results")

# Plotting Results
st.write("### Execution Time for Each Implementation")
plt.figure(figsize=(10, 6))
plt.plot(n_values, recursive_times, label="Recursive Simple", marker='o', linestyle='--')
plt.plot(n_values, dynamic_times, label="Dynamic Recursive", marker='s', linestyle='-')
plt.plot(n_values, iterative_times, label="Iterative", marker='^', linestyle='-.')

plt.title("Comparison of Execution Times for Fibonacci Implementations")
plt.xlabel("n (Fibonacci size)")
plt.ylabel("Time (seconds)")
plt.legend()
plt.grid()
st.pyplot(plt)

# Displaying the Table
st.write("### Comparison Table of Execution Times")
st.dataframe(df, use_container_width=True)
