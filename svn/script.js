const execBtn = document.getElementById('execBtn');
const budgetNum = document.getElementById('budgetNum');
const resultArea = document.getElementById('resultArea');
const totalNum = document.getElementById('totalNum');
const cardList = document.getElementById('cardList');

let productData = [];

async function loadData() {
    try {
        const response = await fetch('./products_seven.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        productData = await response.json();
    } catch (e) {
        console.error("データの読み込みに失敗しました:", e);
    }
}

function doGacha() {
    const budget = parseInt(budgetNum.value);
    
    if (isNaN(budget) || budget <= 0) {
        alert('有効な予算を入力してください。');
        return;
    }

    execBtn.disabled = true;
    setTimeout(() => {
        let bestResult = {
            items: [],
            total: 0,
            diff: Infinity
        };

        const TRY_COUNT = 100;
        for (let i = 0; i < TRY_COUNT; i++) {
            const candidates = [...productData].sort(() => Math.random() - 0.5);
            
            let currentTotal = 0;
            let currentItems = [];

            for (const item of candidates) {
                const tolerance = Math.max(budget * 0.05, 50);
                if (currentTotal + item.price <= budget + tolerance) {
                    currentItems.push(item);
                    currentTotal += item.price;
                }
            }

            const currentDiff = Math.abs(Math.floor(currentTotal) - budget);
            if (currentDiff < bestResult.diff) {
                bestResult = {
                    items: currentItems,
                    total: currentTotal,
                    diff: currentDiff
                };
            }
            if (currentDiff === 0) break;
        }

        renderResult(bestResult.items, bestResult.total);
        execBtn.disabled = false;
    }, 500);
}

function renderResult(items, total) {
    cardList.innerHTML = '';
    totalNum.textContent = `合計: ${Math.floor(total)} 円`;
    
    items.forEach(item => {
        const cardItem = document.createElement('a');
        cardItem.className = 'card';
        cardItem.href = item.url;
        cardItem.target = "_blank";
        cardItem.rel = "noopener noreferrer";
        cardItem.innerHTML = `
            <img src="${item.image}" alt="${item.name}" onerror="this.src='https://placehold.jp/150x150.png?text=No+Image'">
            <div class="card-info">
                <h3>${item.name}</h3>
                <p class="price">¥${item.price}</p>
                <p class="category">${item.category}</p>
            </div>
        `;
        cardList.appendChild(cardItem);
    });
    resultArea.classList.remove('hidden');
}

execBtn.addEventListener('click', doGacha);
loadData();