/**
 * Local Python Executor Service
 * Executes Python calculator directly as a local process
 * No server required - runs Python as subprocess
 */
import environment from '../config/environment'

interface PythonResult {
  result: string;
  success: boolean;
  error?: string;
  duration: number;
}

interface TestResult {
  passed: boolean;
  actual: string;
  expected: string;
  duration: number;
  success: boolean;
  error?: string;
}

class LocalPythonExecutor {
  private pythonPath: string;
  private cliScript: string;
  private isAvailable: boolean | null = null; // Cache availability check

  constructor(pythonPath?: string, cliScript?: string) {
    this.pythonPath = pythonPath || environment.pythonPath;
    this.cliScript = cliScript || environment.pythonCliScript;
    
    // Only check availability if local Python execution is enabled
    if (environment.enableLocalPython) {
      // Defer the availability check to avoid blocking constructor
      setTimeout(() => this.checkAvailability(), 100);
    } else {
      console.log('🔧 Local Python execution disabled by configuration');
    }
  }

  /**
   * Check if Python and the calculator script are available
   */
  async checkAvailability(): Promise<boolean> {
    if (this.isAvailable !== null) {
      return this.isAvailable;
    }

    try {
      // Check if we can run Python
      const testCommand = `${this.pythonPath} --version`;
      
      // Note: In a real browser environment, we can't execute subprocess
      // This would need to be handled by Electron, Tauri, or a similar desktop app framework
      // For now, we'll simulate the check
      
      if (typeof window !== 'undefined') {
        // Browser environment - Python execution not available
        console.log('🌐 Browser environment detected - Python execution not available');
        this.isAvailable = false;
        return false;
      }

      // In Node.js environment or Electron, we could use child_process
      if (typeof process !== 'undefined' && process.versions && process.versions.node) {
        try {
          // This would work in Node.js/Electron environment
          const { exec } = await import('child_process');
          
          return new Promise<boolean>((resolve) => {
            exec(testCommand, (error, stdout, stderr) => {
              if (error) {
                console.log(`❌ Python not available: ${error.message}`);
                this.isAvailable = false;
                resolve(false);
              } else {
                console.log(`✅ Python available: ${stdout.trim()}`);
                this.isAvailable = true;
                resolve(true);
              }
            });
          });
        } catch (importError) {
          console.log('❌ child_process module not available');
          this.isAvailable = false;
          return false;
        }
      }

      // Default fallback
      this.isAvailable = false;
      return false;

    } catch (error) {
      console.log(`❌ Python availability check failed: ${error}`);
      this.isAvailable = false;
      return false;
    }
  }

  /**
   * Execute Python calculator with given expression using CLI wrapper
   */
  async calculate(expression: string, precision: string = 'standard'): Promise<PythonResult> {
    const startTime = performance.now();
    
    try {
      // Check if local Python execution is enabled
      if (!environment.enableLocalPython) {
        throw new Error('Local Python execution disabled by configuration');
      }
      
      const available = await this.checkAvailability();
      if (!available) {
        throw new Error('Python executor not available in this environment');
      }

      // Execute Python CLI wrapper
      if (typeof process !== 'undefined' && process.versions && process.versions.node) {
        const { exec } = await import('child_process');
        
        return new Promise<PythonResult>((resolve) => {
          // Escape the expression for shell execution
          const escapedExpression = expression.replace(/"/g, '\\"').replace(/'/g, "\\'");
          const command = `${this.pythonPath} ${this.cliScript} --calculate "${escapedExpression}" --precision ${precision} --json`;
          
          exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
            const duration = performance.now() - startTime;
            
            if (error) {
              resolve({
                result: '',
                success: false,
                error: error.message,
                duration
              });
              return;
            }

            try {
              // Parse JSON response from CLI
              const response = JSON.parse(stdout.trim());
              
              resolve({
                result: response.success ? response.result : '',
                success: response.success,
                error: response.success ? undefined : response.error,
                duration
              });
            } catch (parseError) {
              resolve({
                result: '',
                success: false,
                error: `Failed to parse CLI response: ${parseError}`,
                duration
              });
            }
          });
        });
      } else {
        throw new Error('Node.js environment required for Python execution');
      }

    } catch (error) {
      const duration = performance.now() - startTime;
      return {
        result: '',
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        duration
      };
    }
  }

  /**
   * Run a test case using CLI wrapper
   */
  async runTest(expression: string, expected: string): Promise<TestResult> {
    const startTime = performance.now();
    
    try {
      // Check if local Python execution is enabled
      if (!environment.enableLocalPython) {
        throw new Error('Local Python execution disabled by configuration');
      }
      
      const available = await this.checkAvailability();
      if (!available) {
        throw new Error('Python executor not available in this environment');
      }

      // Execute Python CLI wrapper for testing
      if (typeof process !== 'undefined' && process.versions && process.versions.node) {
        const { exec } = await import('child_process');
        
        return new Promise<TestResult>((resolve) => {
          // Escape the expression and expected for shell execution
          const escapedExpression = expression.replace(/"/g, '\\"').replace(/'/g, "\\'");
          const escapedExpected = expected.replace(/"/g, '\\"').replace(/'/g, "\\'");
          const command = `${this.pythonPath} ${this.cliScript} --test "${escapedExpression}" "${escapedExpected}" --json`;
          
          exec(command, { timeout: 30000 }, (error, stdout, stderr) => {
            const duration = performance.now() - startTime;
            
            if (error) {
              resolve({
                passed: false,
                actual: '',
                expected,
                duration,
                success: false,
                error: error.message
              });
              return;
            }

            try {
              // Parse JSON response from CLI
              const response = JSON.parse(stdout.trim());
              
              resolve({
                passed: response.success ? response.passed : false,
                actual: response.actual || '',
                expected,
                duration,
                success: response.success,
                error: response.success ? undefined : response.error
              });
            } catch (parseError) {
              resolve({
                passed: false,
                actual: '',
                expected,
                duration,
                success: false,
                error: `Failed to parse CLI response: ${parseError}`
              });
            }
          });
        });
      } else {
        throw new Error('Node.js environment required for Python execution');
      }

    } catch (error) {
      const duration = performance.now() - startTime;
      return {
        passed: false,
        actual: '',
        expected,
        duration,
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  /**
   * Check if the executor is available
   */
  async isReady(): Promise<boolean> {
    return await this.checkAvailability();
  }

  /**
   * Get executor status
   */
  getStatus(): {
    pythonPath: string;
    calculatorScript: string;
    isAvailable: boolean | null;
    environment: string;
  } {
    return {
      pythonPath: this.pythonPath,
      calculatorScript: this.calculatorScript,
      isAvailable: this.isAvailable,
      environment: typeof window !== 'undefined' ? 'browser' : 'node'
    };
  }

  /**
   * Set Python path
   */
  setPythonPath(path: string): void {
    this.pythonPath = path;
    this.isAvailable = null; // Reset availability check
  }

  /**
   * Set calculator script path
   */
  setCalculatorScript(path: string): void {
    this.calculatorScript = path;
    this.isAvailable = null; // Reset availability check
  }
}

// Create singleton instance
const localPythonExecutor = new LocalPythonExecutor();

export default localPythonExecutor;
export type { PythonResult, TestResult };
export { LocalPythonExecutor };
