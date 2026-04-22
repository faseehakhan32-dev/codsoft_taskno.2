/**
 * Modern Calculator — Script
 * Prompts the user to input two numbers and an operation,
 * performs the calculation, and displays the result with history.
 */

(function () {
    'use strict';

    // ─── DOM References ─────────────────────────────────────
    const num1Input        = document.getElementById('num1');
    const num2Input        = document.getElementById('num2');
    const opGrid           = document.getElementById('operation-grid');
    const opButtons        = document.querySelectorAll('.op-btn');
    const calculateBtn     = document.getElementById('btn-calculate');
    const displayExpr      = document.getElementById('display-expression');
    const displayResult    = document.getElementById('display-result');
    const inputSection     = document.getElementById('input-section');
    const resultSection    = document.getElementById('result-section');
    const resultExpression = document.getElementById('result-expression');
    const resultValue      = document.getElementById('result-value');
    const newCalcBtn       = document.getElementById('btn-new-calc');
    const historyList      = document.getElementById('history-list');
    const historyEmpty     = document.getElementById('history-empty');
    const clearHistoryBtn  = document.getElementById('btn-clear-history');

    // ─── State ──────────────────────────────────────────────
    let selectedOp = null;
    let history    = [];

    // ─── Operation Maps ─────────────────────────────────────
    const opSymbols = { '+': '+', '-': '−', '*': '×', '/': '÷' };
    const opNames   = { '+': 'Addition', '-': 'Subtraction', '*': 'Multiplication', '/': 'Division' };

    // ─── Utility: Format Number ─────────────────────────────
    function formatNumber(n) {
        if (!isFinite(n)) return String(n);
        // Show up to 10 significant digits, trim trailing zeros
        const str = parseFloat(n.toPrecision(12)).toString();
        return str;
    }

    // ─── Calculation Logic ──────────────────────────────────
    function calculate(a, b, op) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/':
                if (b === 0) return { error: 'Cannot divide by zero' };
                return a / b;
            default:
                return { error: 'Invalid operation' };
        }
    }

    // ─── Update Live Display ────────────────────────────────
    function updateDisplay() {
        const a = num1Input.value;
        const b = num2Input.value;
        const sym = selectedOp ? opSymbols[selectedOp] : '?';

        if (a || b || selectedOp) {
            displayExpr.textContent = `${a || '?'} ${sym} ${b || '?'}`;
        } else {
            displayExpr.textContent = '';
        }
    }

    // ─── Operation Selection ────────────────────────────────
    opButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            opButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            selectedOp = btn.dataset.op;
            updateDisplay();
        });
    });

    // ─── Live Input Feedback ────────────────────────────────
    num1Input.addEventListener('input', () => {
        num1Input.classList.remove('error');
        updateDisplay();
    });
    num2Input.addEventListener('input', () => {
        num2Input.classList.remove('error');
        updateDisplay();
    });

    // ─── Validation ─────────────────────────────────────────
    function validate() {
        let valid = true;

        if (num1Input.value.trim() === '') {
            num1Input.classList.add('error', 'shake');
            setTimeout(() => num1Input.classList.remove('shake'), 500);
            valid = false;
        }

        if (num2Input.value.trim() === '') {
            num2Input.classList.add('error', 'shake');
            setTimeout(() => num2Input.classList.remove('shake'), 500);
            valid = false;
        }

        if (!selectedOp) {
            opGrid.classList.add('shake');
            setTimeout(() => opGrid.classList.remove('shake'), 500);
            valid = false;
        }

        return valid;
    }

    // ─── Perform Calculation ────────────────────────────────
    function performCalculation() {
        if (!validate()) return;

        const a = parseFloat(num1Input.value);
        const b = parseFloat(num2Input.value);
        const result = calculate(a, b, selectedOp);

        if (result && typeof result === 'object' && result.error) {
            displayResult.textContent = result.error;
            displayResult.classList.add('pop');
            setTimeout(() => displayResult.classList.remove('pop'), 350);
            return;
        }

        const formatted = formatNumber(result);
        const exprStr = `${formatNumber(a)} ${opSymbols[selectedOp]} ${formatNumber(b)}`;

        // Update display
        displayExpr.textContent = exprStr;
        displayResult.textContent = formatted;
        displayResult.classList.add('pop');
        setTimeout(() => displayResult.classList.remove('pop'), 350);

        // Show result section, hide input section
        inputSection.style.display = 'none';
        resultSection.classList.remove('hidden');
        resultExpression.textContent = exprStr;
        resultValue.textContent = formatted;

        // Add to history
        addToHistory(exprStr, formatted);
    }

    // ─── History Management ─────────────────────────────────
    function addToHistory(expr, val) {
        history.unshift({ expr, val });
        if (history.length > 20) history.pop();
        renderHistory();
    }

    function renderHistory() {
        historyEmpty.style.display = history.length === 0 ? 'block' : 'none';

        // Remove existing items (keep the empty message)
        const existing = historyList.querySelectorAll('.history-item');
        existing.forEach(el => el.remove());

        history.forEach((item, idx) => {
            const el = document.createElement('div');
            el.className = 'history-item';
            el.style.animationDelay = `${idx * 0.04}s`;
            el.innerHTML = `
                <span class="history-expr">${item.expr}</span>
                <span class="history-val">${item.val}</span>
            `;
            el.addEventListener('click', () => {
                // Re-show this result
                displayExpr.textContent = item.expr;
                displayResult.textContent = item.val;
                displayResult.classList.add('pop');
                setTimeout(() => displayResult.classList.remove('pop'), 350);

                inputSection.style.display = 'none';
                resultSection.classList.remove('hidden');
                resultExpression.textContent = item.expr;
                resultValue.textContent = item.val;
            });
            historyList.appendChild(el);
        });
    }

    clearHistoryBtn.addEventListener('click', () => {
        history = [];
        renderHistory();
    });

    // ─── New Calculation ────────────────────────────────────
    function resetForNew() {
        num1Input.value = '';
        num2Input.value = '';
        num1Input.classList.remove('error');
        num2Input.classList.remove('error');
        opButtons.forEach(b => b.classList.remove('active'));
        selectedOp = null;

        displayExpr.textContent = '';
        displayResult.textContent = '0';

        resultSection.classList.add('hidden');
        inputSection.style.display = 'block';

        num1Input.focus();
    }

    // ─── Event Bindings ─────────────────────────────────────
    calculateBtn.addEventListener('click', performCalculation);
    newCalcBtn.addEventListener('click', resetForNew);

    // Keyboard support: Enter to calculate
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            if (resultSection.classList.contains('hidden')) {
                performCalculation();
            } else {
                resetForNew();
            }
        }
    });

    // Keyboard shortcuts for operations
    document.addEventListener('keydown', (e) => {
        if (document.activeElement.tagName === 'INPUT') return; // Don't hijack input
        const keyMap = { '+': '+', '-': '-', '*': '*', 'x': '*', '/': '/' };
        if (keyMap[e.key]) {
            const op = keyMap[e.key];
            opButtons.forEach(b => b.classList.remove('active'));
            const target = document.querySelector(`.op-btn[data-op="${op}"]`);
            if (target) {
                target.classList.add('active');
                selectedOp = op;
                updateDisplay();
            }
        }
    });

    // ─── Init ───────────────────────────────────────────────
    updateDisplay();
})();
