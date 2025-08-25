/**
 * Calculator API Service
 * Handles communication with Python backend API for arbitrary precision calculations
 */
import environment from '../config/environment'

interface CalculateResponse {
  result: string;
  expression: string;
  success: boolean;
  error?: string;
}

interface TestResponse {
  passed: boolean;
  actual: string;
  expected: string;
  duration: number;
  success: boolean;
  error?: string;
}

interface HistoryEntry {
  expression: string;
  result: string;
  timestamp: string;
}

interface HistoryResponse {
  history: HistoryEntry[];
  success: boolean;
}

class CalculatorApiService {
  private baseUrl: string;
  private isApiAvailable: boolean = false;
  private apiCheckInProgress: boolean = false;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || environment.apiBaseUrl;
    
    // Only check API health if not forced to use local calculator
    if (!environment.forceLocalCalculator && environment.enableApiHealthCheck) {
      this.checkApiHealth();
    } else if (environment.forceLocalCalculator) {
      console.log('🔧 Forced to use local calculator - skipping API health check');
    }
  }

  /**
   * Check if the Python API is available
   */
  async checkApiHealth(): Promise<boolean> {
    if (this.apiCheckInProgress) {
      return this.isApiAvailable;
    }

    this.apiCheckInProgress = true;
    
    try {
      const response = await fetch(`${this.baseUrl}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        // Add timeout for health check
        signal: AbortSignal.timeout(3000)
      });

      this.isApiAvailable = response.ok;
      console.log(`🐍 Python API ${this.isApiAvailable ? 'available' : 'unavailable'} at ${this.baseUrl}`);
    } catch (error) {
      this.isApiAvailable = false;
      console.log(`🔴 Python API not available: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      this.apiCheckInProgress = false;
    }

    return this.isApiAvailable;
  }

  /**
   * Calculate mathematical expression using Python backend
   */
  async calculate(expression: string): Promise<string> {
    // If forced to use local calculator, don't try API
    if (environment.forceLocalCalculator) {
      throw new Error('Forced to use local calculator');
    }
    
    // Check API availability first
    const apiAvailable = await this.checkApiHealth();
    
    if (!apiAvailable) {
      throw new Error('Python API not available - using fallback calculator');
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/calculate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          expression: expression.trim(),
          precision_mode: 'standard',
          base: 10
        }),
        // Add timeout for calculations
        signal: AbortSignal.timeout(30000) // 30 seconds for complex calculations
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status} ${response.statusText}`);
      }

      const data: CalculateResponse = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Calculation failed');
      }

      return data.result;
    } catch (error) {
      if (error instanceof Error) {
        // Check if it's a timeout or network error
        if (error.name === 'AbortError') {
          throw new Error('Calculation timeout - expression too complex');
        }
        if (error.message.includes('Failed to fetch')) {
          throw new Error('Network error - Python API unavailable');
        }
        throw error;
      }
      throw new Error('Unknown API error');
    }
  }

  /**
   * Run a single test case using Python backend
   */
  async runTest(expression: string, expected: string): Promise<TestResponse> {
    // If forced to use local calculator, don't try API
    if (environment.forceLocalCalculator) {
      throw new Error('Forced to use local calculator for testing');
    }
    
    const apiAvailable = await this.checkApiHealth();
    
    if (!apiAvailable) {
      throw new Error('Python API not available for testing');
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          expression: expression.trim(),
          expected: expected.trim()
        }),
        signal: AbortSignal.timeout(10000) // 10 seconds for test cases
      });

      if (!response.ok) {
        throw new Error(`Test API request failed: ${response.status}`);
      }

      const data: TestResponse = await response.json();
      return data;
    } catch (error) {
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error('Test timeout');
        }
        throw error;
      }
      throw new Error('Unknown test error');
    }
  }

  /**
   * Get calculation history from backend
   */
  async getHistory(): Promise<HistoryEntry[]> {
    // If forced to use local calculator, don't try API
    if (environment.forceLocalCalculator) {
      return []; // Return empty history when using local calculator
    }
    
    const apiAvailable = await this.checkApiHealth();
    
    if (!apiAvailable) {
      return []; // Return empty history if API not available
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/history`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(5000)
      });

      if (!response.ok) {
        throw new Error(`History API request failed: ${response.status}`);
      }

      const data: HistoryResponse = await response.json();
      return data.success ? data.history : [];
    } catch (error) {
      console.warn('Failed to fetch history from API:', error);
      return [];
    }
  }

  /**
   * Clear calculation history on backend
   */
  async clearHistory(): Promise<boolean> {
    // If forced to use local calculator, don't try API
    if (environment.forceLocalCalculator) {
      return false; // Can't clear history when using local calculator
    }
    
    const apiAvailable = await this.checkApiHealth();
    
    if (!apiAvailable) {
      return false;
    }

    try {
      const response = await fetch(`${this.baseUrl}/api/history`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(5000)
      });

      return response.ok;
    } catch (error) {
      console.warn('Failed to clear history on API:', error);
      return false;
    }
  }

  /**
   * Check if API is currently available
   * Takes into account environment configuration
   */
  isAvailable(): boolean {
    // If forced to use local calculator, API is not available
    if (environment.forceLocalCalculator) {
      return false;
    }
    return this.isApiAvailable;
  }

  /**
   * Get current configuration and status information
   */
  getStatus(): {
    baseUrl: string;
    isApiAvailable: boolean;
    forceLocalCalculator: boolean;
    enableApiHealthCheck: boolean;
    environment: string;
  } {
    return {
      baseUrl: this.baseUrl,
      isApiAvailable: this.isApiAvailable,
      forceLocalCalculator: environment.forceLocalCalculator,
      enableApiHealthCheck: environment.enableApiHealthCheck,
      environment: environment.nodeEnv
    };
  }

  /**
   * Get the current API base URL
   */
  getBaseUrl(): string {
    return this.baseUrl;
  }

  /**
   * Update the API base URL (for configuration changes)
   */
  setBaseUrl(url: string): void {
    this.baseUrl = url;
    this.isApiAvailable = false; // Reset availability check
    this.checkApiHealth(); // Re-check with new URL
  }
}

// Create singleton instance
const calculatorApi = new CalculatorApiService();

export default calculatorApi;
export type { CalculateResponse, TestResponse, HistoryEntry, HistoryResponse };
