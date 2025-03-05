// Utility Functions
function getArrayFromInput(inputId) {
    const input = document.getElementById(inputId).value;
    return input.split(',').map(num => parseInt(num.trim())).filter(num => !isNaN(num));
}

function generateRandomArray() {
    const array = Array.from({length: 10}, () => Math.floor(Math.random() * 100) + 1);
    document.getElementById('arrayInput').value = array.join(', ');
    renderArray(array);
    return array;
}

function renderArray(array, highlightIndices = []) {
    const visualizer = document.getElementById('visualizer');
    if (!visualizer) {
        console.error('Visualizer element not found');
        return;
    }
    visualizer.innerHTML = '';
    
    if (array.length === 0) {
        visualizer.textContent = 'No valid array to display';
        return;
    }

    const maxValue = Math.max(...array, 1);
    const barWidth = Math.min(30, 600 / array.length - 2);

    array.forEach((value, index) => {
        const bar = document.createElement('div');
        bar.style.height = `${(value / maxValue) * 200}px`;
        bar.style.width = `${barWidth}px`;
        bar.style.backgroundColor = highlightIndices.includes(index) ? '#ff4444' : '#3498db';
        bar.style.margin = '0 1px';
        bar.style.display = 'inline-block';
        bar.textContent = value;
        bar.style.color = 'white';
        bar.style.textAlign = 'center';
        bar.style.fontSize = '12px';
        visualizer.appendChild(bar);
    });
}

// Visualize Steps from Server
async function visualizeSteps(steps) {
    const status = document.getElementById('status');
    for (const step of steps) {
        renderArray(step.array, step.highlight);
        status.textContent = step.status;
        await new Promise(resolve => setTimeout(resolve, 500));
    }
}

// Event Handlers
async function visualizeSorting() {
    let arr = getArrayFromInput('arrayInput');
    if (arr.length === 0) {
        arr = generateRandomArray();
    } else {
        renderArray(arr);
    }
    
    const algorithm = document.getElementById('algorithm').value;
    document.getElementById('status').textContent = `Sorting with ${algorithm}...`;

    const response = await fetch('/sort', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ array: arr, algorithm: algorithm })
    });
    
    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }
    await visualizeSteps(data.steps);
}

async function visualizeSearching() {
    const arr = getArrayFromInput('searchArrayInput');
    const target = parseInt(document.getElementById('targetInput').value);
    const algorithm = document.getElementById('searchAlgorithm').value;

    if (arr.length === 0 || isNaN(target)) {
        alert('Please enter a valid array and target number');
        return;
    }
    renderArray(arr);
    document.getElementById('status').textContent = `Searching with ${algorithm}...`;

    const response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ array: arr, target: target, algorithm: algorithm })
    });
    
    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }
    await visualizeSteps(data.steps);
}

// Set up event listeners
document.addEventListener('DOMContentLoaded', () => {
    const sortButton = document.getElementById('sort-visualize');
    const searchButton = document.getElementById('search-visualize');
    const randomButton = document.getElementById('random-array');

    if (sortButton) sortButton.addEventListener('click', visualizeSorting);
    else console.error('Sort button not found');
    
    if (searchButton) searchButton.addEventListener('click', visualizeSearching);
    else console.error('Search button not found');
    
    if (randomButton) randomButton.addEventListener('click', generateRandomArray);
    else console.error('Random button not found');
});