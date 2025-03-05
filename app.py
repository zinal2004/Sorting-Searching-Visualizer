from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sorting Algorithms
def bubble_sort(arr):
    steps = []
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            steps.append({
                'array': arr.copy(),
                'highlight': [j, j + 1],
                'status': 'Comparing'
            })
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append({
                    'array': arr.copy(),
                    'highlight': [j, j + 1],
                    'status': 'Swapped'
                })
    steps.append({
        'array': arr.copy(),
        'highlight': [],
        'status': 'Sorting Complete'
    })
    return steps

def selection_sort(arr):
    steps = []
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            steps.append({
                'array': arr.copy(),
                'highlight': [min_idx, j],
                'status': 'Comparing'
            })
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({
                'array': arr.copy(),
                'highlight': [i, min_idx],
                'status': 'Swapped'
            })
    steps.append({
        'array': arr.copy(),
        'highlight': [],
        'status': 'Sorting Complete'
    })
    return steps

def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        steps.append({
            'array': arr.copy(),
            'highlight': [i],
            'status': 'Selected key'
        })
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            steps.append({
                'array': arr.copy(),
                'highlight': [j, j + 1],
                'status': 'Shifting'
            })
            j -= 1
        arr[j + 1] = key
        steps.append({
            'array': arr.copy(),
            'highlight': [j + 1],
            'status': 'Inserted'
        })
    steps.append({
        'array': arr.copy(),
        'highlight': [],
        'status': 'Sorting Complete'
    })
    return steps

def merge_sort(arr, start=0, end=None):
    steps = []
    if end is None:
        end = len(arr) - 1
    
    if start < end:
        mid = (start + end) // 2
        steps.extend(merge_sort(arr, start, mid))
        steps.extend(merge_sort(arr, mid + 1, end))
        steps.extend(merge(arr, start, mid, end))
    
    if start == 0 and end == len(arr) - 1:
        steps.append({
            'array': arr.copy(),
            'highlight': [],
            'status': 'Sorting Complete'
        })
    return steps

def merge(arr, start, mid, end):
    steps = []
    left = arr[start:mid + 1].copy()
    right = arr[mid + 1:end + 1].copy()
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        steps.append({
            'array': arr.copy(),
            'highlight': [k],
            'status': 'Merging'
        })
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        steps.append({
            'array': arr.copy(),
            'highlight': [k],
            'status': 'Merging left remainder'
        })
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        steps.append({
            'array': arr.copy(),
            'highlight': [k],
            'status': 'Merging right remainder'
        })
        arr[k] = right[j]
        j += 1
        k += 1
    
    return steps

# Searching Algorithms
def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        steps.append({
            'array': arr.copy(),
            'highlight': [i],
            'status': 'Searching'
        })
        if arr[i] == target:
            steps.append({
                'array': arr.copy(),
                'highlight': [i],
                'status': f'Found {target} at index {i}'
            })
            return steps
    steps.append({
        'array': arr.copy(),
        'highlight': [],
        'status': f'{target} not found'
    })
    return steps

def binary_search(arr, target):
    steps = []
    # Sort the array first for binary search
    sorted_arr = arr.copy()
    steps.extend(bubble_sort(sorted_arr))  # Using bubble sort for visualization
    steps[-1]['status'] = 'Array sorted for Binary Search'
    
    left, right = 0, len(sorted_arr) - 1
    while left <= right:
        mid = (left + right) // 2
        steps.append({
            'array': sorted_arr.copy(),
            'highlight': [mid],
            'status': 'Checking middle element'
        })
        if sorted_arr[mid] == target:
            steps.append({
                'array': sorted_arr.copy(),
                'highlight': [mid],
                'status': f'Found {target} at index {mid}'
            })
            return steps
        elif sorted_arr[mid] < target:
            steps.append({
                'array': sorted_arr.copy(),
                'highlight': [mid],
                'status': 'Target is greater, searching right half'
            })
            left = mid + 1
        else:
            steps.append({
                'array': sorted_arr.copy(),
                'highlight': [mid],
                'status': 'Target is smaller, searching left half'
            })
            right = mid - 1
    
    steps.append({
        'array': sorted_arr.copy(),
        'highlight': [],
        'status': f'{target} not found'
    })
    return steps

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort_array():
    data = request.get_json()
    array = data.get('array', [])
    algorithm = data.get('algorithm', 'Bubble Sort')
    
    if not array:
        return jsonify({'error': 'No array provided'}), 400
    
    if algorithm == 'Bubble Sort':
        steps = bubble_sort(array.copy())
    elif algorithm == 'Selection Sort':
        steps = selection_sort(array.copy())
    elif algorithm == 'Insertion Sort':
        steps = insertion_sort(array.copy())
    elif algorithm == 'Merge Sort':
        steps = merge_sort(array.copy())
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    return jsonify({'steps': steps})

@app.route('/search', methods=['POST'])
def search_array():
    data = request.get_json()
    array = data.get('array', [])
    target = data.get('target', None)
    algorithm = data.get('algorithm', 'Linear Search')
    
    if not array or target is None:
        return jsonify({'error': 'Array or target missing'}), 400
    
    if algorithm == 'Linear Search':
        steps = linear_search(array.copy(), target)
    elif algorithm == 'Binary Search':
        steps = binary_search(array.copy(), target)
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    return jsonify({'steps': steps})

if __name__ == '__main__':
    app.run(debug=True)