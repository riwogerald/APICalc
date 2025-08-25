/**
 * Advanced Precision Calculator - Frontend JavaScript
 * Handles UI interactions and API communication
 */

class AdvancedCalculator {
    constructor() {
        this.currentExpression = '';
        this.isComplexMode = false;
        this.history = JSON.parse(localStorage.getItem('calculatorHistory')) || [];
        this.settings = {
            precision: 'standard',
            base: 10,
            decimals: 15
        };
        
        this.initializeElements();
        this.attachEventListeners();
        this.updateStatusIndicators();
        this.loadHistory();
        this.checkBackendConnection();
    }

    initializeElements() {
        // Display elements
        this.expressionDisplay = document.getElementById('expressionDisplay');
        this.resultDisplay = document.getElementById('resultDisplay');
        
        // Input elements
        this.calculatorInput = document.getElementById('calculatorInput');
        this.calculateBtn = document.getElementById('calculateBtn');
        
        // Settings elements
        this.precisionMode = document.getElementById('precisionMode');
        this.numberBase = document.getElementById('numberBase');
        this.complexModeBtn = document.getElementById('complexModeBtn');
        
        // Advanced panel
        this.advancedPanel = document.getElementById('advancedPanel');
        this.advancedToggle = document.getElementById('advancedToggle');
        
        // History panel
        this.historyPanel = document.getElementById('historyPanel');
        this.historyToggle = document.getElementById('historyToggle');
        this.historyContent = document.getElementById('historyContent');
        this.clearHistory = document.getElementById('clearHistory');
        
        // Status indicators
        this.modeIndicator = document.getElementById('modeIndicator');
        this.baseIndicator = document.getElementById('baseIndicator');
        this.precisionIndicator = document.getElementById('precisionIndicator');
        this.connectionStatus = document.getElementById('connectionStatus');
        
        // Modal elements
        this.errorModal = document.getElementById('errorModal');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorModalClose = document.getElementById('errorModalClose');
        this.errorModalOk = document.getElementById('errorModalOk');
        this.loadingOverlay = document.getElementById('loadingOverlay');
    }

    attachEventListeners() {
        // Input and calculation
        this.calculatorInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.calculate();
            }
        });
        
        this.calculateBtn.addEventListener('click', () => this.calculate());
        
        // Settings
        this.precisionMode.addEventListener('change', (e) => {
            this.settings.precision = e.target.value;
            this.updateStatusIndicators();
        });
        
        this.numberBase.addEventListener('change', (e) => {
            this.settings.base = parseInt(e.target.value);
            this.updateStatusIndicators();
        });
        
        this.complexModeBtn.addEventListener('click', () => this.toggleComplexMode());
        
        // Advanced panel toggle
        this.advancedToggle.addEventListener('click', () => this.toggleAdvancedPanel());
        
        // History panel toggle
        this.historyToggle.addEventListener('click', () => this.toggleHistoryPanel());
        this.clearHistory.addEventListener('click', () => this.clearCalculationHistory());
        
        // Button clicks
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleButtonClick(e));
        });
        
        // Modal close
        this.errorModalClose.addEventListener('click', () => this.hideErrorModal());
        this.errorModalOk.addEventListener('click', () => this.hideErrorModal());
        
        // Click outside modal to close
        this.errorModal.addEventListener('click', (e) => {
            if (e.target === this.errorModal) {
                this.hideErrorModal();
            }
        });
    }

    handleButtonClick(e) {
        const btn = e.target;
        const action = btn.dataset.action;
        const value = btn.dataset.value;
        const func = btn.dataset.function;
        const example = btn.dataset.example;

        if (action) {
            this.handleAction(action);
        } else if (value) {
            this.appendToInput(value);
        } else if (func) {
            this.handleFunction(func);
        } else if (example) {
            this.setInput(example);
        }
    }

    handleAction(action) {
        switch (action) {
            case 'clear':
                this.clearAll();
                break;
            case 'clear-entry':
                this.clearEntry();
                break;
            case 'backspace':
                this.backspace();
                break;
            case 'calculate':
                this.calculate();
                break;
            case 'pi':
                this.insertConstant('pi');
                break;
            case 'e':
                this.insertConstant('e');
                break;
        }
    }

    handleFunction(funcName) {
        const currentInput = this.calculatorInput.value.trim();
        
        if (!currentInput) {
            this.showError('Please enter a value first');
            return;
        }

        // Format function call
        const functionExpression = `${funcName}(${currentInput})`;
        this.callFunction(funcName, [currentInput]);
    }

    appendToInput(value) {
        const currentInput = this.calculatorInput.value;
        const cursorPos = this.calculatorInput.selectionStart;
        const newValue = currentInput.substring(0, cursorPos) + value + currentInput.substring(cursorPos);
        
        this.calculatorInput.value = newValue;
        this.calculatorInput.focus();
        
        // Move cursor after inserted value
        const newCursorPos = cursorPos + value.length;
        this.calculatorInput.setSelectionRange(newCursorPos, newCursorPos);
        
        this.updateExpressionDisplay(newValue);
    }

    setInput(value) {
        this.calculatorInput.value = value;
        this.calculatorInput.focus();
        this.updateExpressionDisplay(value);
    }

    clearAll() {
        this.calculatorInput.value = '';
        this.resultDisplay.textContent = '0';
        this.expressionDisplay.textContent = 'Ready';
        this.calculatorInput.focus();
    }

    clearEntry() {
        this.calculatorInput.value = '';
        this.expressionDisplay.textContent = 'Ready';
        this.calculatorInput.focus();
    }

    backspace() {
        const input = this.calculatorInput;
        const cursorPos = input.selectionStart;
        
        if (cursorPos > 0) {
            const currentValue = input.value;
            const newValue = currentValue.substring(0, cursorPos - 1) + currentValue.substring(cursorPos);
            input.value = newValue;
            input.setSelectionRange(cursorPos - 1, cursorPos - 1);
            this.updateExpressionDisplay(newValue);
        }
        
        input.focus();
    }

    updateExpressionDisplay(expression) {
        if (expression && expression.trim()) {
            this.expressionDisplay.textContent = expression;
        } else {
            this.expressionDisplay.textContent = 'Ready';
        }
    }

    async calculate() {
        const expression = this.calculatorInput.value.trim();
        
        if (!expression) {
            this.showError('Please enter an expression');
            return;
        }

        this.showLoading();
        
        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    expression: expression,
                    precision_mode: this.settings.precision,
                    base: this.settings.base
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.displayResult(data.result);
                this.addToHistory(expression, data.result);
                this.updateConnectionStatus(true);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError(`Connection error: ${error.message}`);
            this.updateConnectionStatus(false);
        } finally {
            this.hideLoading();
        }
    }

    async callFunction(funcName, args) {
        this.showLoading();
        
        try {
            const response = await fetch('/api/function', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    function: funcName,
                    args: args,
                    precision_mode: this.settings.precision,
                    base: this.settings.base
                })
            });

            const data = await response.json();
            
            if (data.success) {
                const expression = `${funcName}(${args.join(', ')})`;
                this.displayResult(data.result);
                this.addToHistory(expression, data.result);
                this.updateConnectionStatus(true);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError(`Connection error: ${error.message}`);
            this.updateConnectionStatus(false);
        } finally {
            this.hideLoading();
        }
    }

    async insertConstant(constantName) {
        this.showLoading();
        
        try {
            const response = await fetch('/api/constants?precision=25');
            const data = await response.json();
            
            if (data.success) {
                const value = constantName === 'pi' ? data.pi : data.e;
                this.appendToInput(value);
                this.updateConnectionStatus(true);
            } else {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError(`Connection error: ${error.message}`);
            this.updateConnectionStatus(false);
        } finally {
            this.hideLoading();
        }
    }

    displayResult(result) {
        this.resultDisplay.textContent = result;
        this.updateExpressionDisplay(this.calculatorInput.value);
    }

    addToHistory(expression, result) {
        const historyItem = {
            expression: expression,
            result: result,
            timestamp: new Date().toISOString(),
            settings: { ...this.settings }
        };
        
        this.history.unshift(historyItem);
        
        // Limit history to 50 items
        if (this.history.length > 50) {
            this.history = this.history.slice(0, 50);
        }
        
        // Save to localStorage
        localStorage.setItem('calculatorHistory', JSON.stringify(this.history));
        
        // Update history display if panel is open
        if (this.historyPanel.classList.contains('show')) {
            this.loadHistory();
        }
    }

    loadHistory() {
        const historyContent = this.historyContent;
        
        if (this.history.length === 0) {
            historyContent.innerHTML = '<p class="history-empty">No calculations yet</p>';
            return;
        }
        
        historyContent.innerHTML = '';
        
        this.history.forEach((item, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.innerHTML = `
                <div class="history-expression">${item.expression}</div>
                <div class="history-result">${item.result}</div>
            `;
            
            historyItem.addEventListener('click', () => {
                this.setInput(item.expression);
                this.hideHistoryPanel();
            });
            
            historyContent.appendChild(historyItem);
        });
    }

    clearCalculationHistory() {
        this.history = [];
        localStorage.removeItem('calculatorHistory');
        this.loadHistory();
    }

    toggleComplexMode() {
        this.isComplexMode = !this.isComplexMode;
        this.updateStatusIndicators();
    }

    toggleAdvancedPanel() {
        const panel = this.advancedPanel;
        const btn = this.advancedToggle;
        
        if (panel.classList.contains('show')) {
            panel.classList.remove('show');
            btn.classList.remove('active');
        } else {
            panel.classList.add('show');
            btn.classList.add('active');
        }
    }

    toggleHistoryPanel() {
        const panel = this.historyPanel;
        
        if (panel.classList.contains('show')) {
            this.hideHistoryPanel();
        } else {
            this.showHistoryPanel();
        }
    }

    showHistoryPanel() {
        this.historyPanel.classList.add('show');
        this.loadHistory();
    }

    hideHistoryPanel() {
        this.historyPanel.classList.remove('show');
    }

    updateStatusIndicators() {
        // Mode indicator
        this.modeIndicator.textContent = this.isComplexMode ? 'Complex Mode' : 'Real Mode';
        
        // Complex mode button
        if (this.isComplexMode) {
            this.complexModeBtn.classList.add('active');
            this.complexModeBtn.innerHTML = '<i class="fas fa-plus-minus"></i> Complex';
        } else {
            this.complexModeBtn.classList.remove('active');
            this.complexModeBtn.innerHTML = '<i class="fas fa-plus-minus"></i> Real';
        }
        
        // Base indicator
        const baseNames = {
            2: 'Binary',
            8: 'Octal',
            10: 'Decimal',
            16: 'Hexadecimal'
        };
        this.baseIndicator.textContent = `${baseNames[this.settings.base]} (${this.settings.base})`;
        
        // Precision indicator
        const precisionNames = {
            'standard': 'Standard',
            'high': 'High',
            'extreme': 'Extreme'
        };
        this.precisionIndicator.textContent = `${precisionNames[this.settings.precision]} Precision`;
    }

    updateConnectionStatus(connected) {
        const status = this.connectionStatus;
        
        if (connected) {
            status.className = 'status-connected';
            status.innerHTML = '<i class="fas fa-circle"></i> Connected';
        } else {
            status.className = 'status-disconnected';
            status.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
        }
    }

    async checkBackendConnection() {
        try {
            const response = await fetch('/api/constants?precision=10');
            const data = await response.json();
            this.updateConnectionStatus(data.success);
        } catch (error) {
            this.updateConnectionStatus(false);
        }
    }

    showLoading() {
        this.loadingOverlay.classList.add('show');
    }

    hideLoading() {
        this.loadingOverlay.classList.remove('show');
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorModal.classList.add('show');
    }

    hideErrorModal() {
        this.errorModal.classList.remove('show');
    }
}

// Utility functions for better UX
class CalculatorUtils {
    static formatNumber(num, maxLength = 20) {
        const str = num.toString();
        if (str.length <= maxLength) {
            return str;
        }
        
        // Try scientific notation for very long numbers
        if (str.includes('.')) {
            const [whole, decimal] = str.split('.');
            if (whole.length > maxLength - 5) {
                return Number(num).toExponential(maxLength - 8);
            }
            
            const availableDecimal = maxLength - whole.length - 1;
            if (availableDecimal > 0) {
                return whole + '.' + decimal.substring(0, availableDecimal);
            }
        }
        
        return str.substring(0, maxLength) + '...';
    }

    static isComplexNumber(str) {
        return str.includes('i') || str.includes('j');
    }

    static validateExpression(expr) {
        // Basic validation
        if (!expr || !expr.trim()) {
            return { valid: false, error: 'Empty expression' };
        }
        
        // Check for balanced parentheses
        let parenCount = 0;
        for (const char of expr) {
            if (char === '(') parenCount++;
            if (char === ')') parenCount--;
            if (parenCount < 0) {
                return { valid: false, error: 'Unbalanced parentheses' };
            }
        }
        
        if (parenCount !== 0) {
            return { valid: false, error: 'Unbalanced parentheses' };
        }
        
        return { valid: true };
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Calculator shortcuts
    if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
            case 'Enter':
                e.preventDefault();
                calculator.calculate();
                break;
            case 'Backspace':
                e.preventDefault();
                calculator.clearAll();
                break;
            case 'h':
                e.preventDefault();
                calculator.toggleHistoryPanel();
                break;
            case 'm':
                e.preventDefault();
                calculator.toggleComplexMode();
                break;
        }
    }
    
    // ESC to close modals
    if (e.key === 'Escape') {
        calculator.hideErrorModal();
        calculator.hideHistoryPanel();
    }
});

// Theme detection and setup (optional future feature)
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('calculatorTheme') || 'light';
        this.applyTheme();
    }
    
    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        localStorage.setItem('calculatorTheme', this.currentTheme);
        this.applyTheme();
    }
}

// Service Worker registration for offline functionality (future feature)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(() => console.log('Service Worker registered'))
            .catch(() => console.log('Service Worker registration failed'));
    });
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.calculator = new AdvancedCalculator();
    window.calculatorUtils = CalculatorUtils;
    
    // Optional theme manager
    // window.themeManager = new ThemeManager();
    
    console.log('Advanced Precision Calculator initialized');
});

// Export for testing (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AdvancedCalculator, CalculatorUtils };
}
