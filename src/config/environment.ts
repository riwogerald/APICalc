/**
 * Environment Configuration
 * Manages settings for development vs production environments
 */

interface EnvironmentConfig {
  apiBaseUrl: string;
  isDevelopment: boolean;
  useLocalCalculator: boolean;
  enableApiHealthCheck: boolean;
  forceLocalCalculator: boolean;
  apiTimeout: number;
  nodeEnv: string;
  // Local Python execution settings
  enableLocalPython: boolean;
  pythonPath: string;
  pythonCliScript: string;
}

const getEnvironmentConfig = (): EnvironmentConfig => {
  // Check if we're in development mode
  const isDev = import.meta.env.DEV || process.env.NODE_ENV === 'development';
  const nodeEnv = process.env.NODE_ENV || (isDev ? 'development' : 'production');
  
  // Get API base URL from environment variables
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 
                     process.env.REACT_APP_API_BASE_URL || 
                     'http://localhost:5000';

  // Determine if we should force local calculator usage
  const forceLocal = import.meta.env.VITE_FORCE_LOCAL_CALCULATOR === 'true' ||
                     process.env.REACT_APP_FORCE_LOCAL_CALCULATOR === 'true';

  // Local Python execution settings
  const enableLocalPython = import.meta.env.VITE_ENABLE_LOCAL_PYTHON === 'true' ||
                            process.env.REACT_APP_ENABLE_LOCAL_PYTHON === 'true' ||
                            isDev; // Enable by default in development

  const pythonPath = import.meta.env.VITE_PYTHON_PATH ||
                     process.env.REACT_APP_PYTHON_PATH ||
                     'python'; // Default to 'python' command

  const pythonCliScript = import.meta.env.VITE_PYTHON_CLI_SCRIPT ||
                          process.env.REACT_APP_PYTHON_CLI_SCRIPT ||
                          'calculator_cli.py';

  return {
    apiBaseUrl,
    isDevelopment: isDev,
    nodeEnv,
    useLocalCalculator: forceLocal,
    enableApiHealthCheck: isDev, // Only check API health in development
    forceLocalCalculator: forceLocal,
    apiTimeout: isDev ? 30000 : 10000, // Longer timeout in development
    enableLocalPython,
    pythonPath,
    pythonCliScript
  };
};

const environment = getEnvironmentConfig();

export default environment;
export type { EnvironmentConfig };
