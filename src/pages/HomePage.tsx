import React from 'react'
import { Link } from 'react-router-dom'
import { Calculator, TestTube, Zap, Shield, Infinity, Code } from 'lucide-react'

const HomePage: React.FC = () => {
  const features = [
    {
      icon: <Infinity className="w-8 h-8 text-primary-600" />,
      title: "Arbitrary Precision",
      description: "Handle numbers of unlimited size with perfect accuracy"
    },
    {
      icon: <Code className="w-8 h-8 text-primary-600" />,
      title: "Multiple Bases",
      description: "Support for binary, octal, decimal, hexadecimal, and custom bases"
    },
    {
      icon: <Zap className="w-8 h-8 text-primary-600" />,
      title: "Advanced Functions",
      description: "Factorial, logarithms, trigonometry, and more mathematical operations"
    },
    {
      icon: <Shield className="w-8 h-8 text-primary-600" />,
      title: "Pure Implementation",
      description: "Built from scratch without external mathematical libraries"
    }
  ]

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <div className="mb-8">
            <Calculator className="w-16 h-16 text-primary-600 mx-auto mb-4 animate-pulse-soft" />
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Advanced Precision
              <span className="text-primary-600 block">Integer Calculator</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              A powerful arbitrary-precision calculator built from the ground up. 
              Handle massive numbers, multiple bases, and advanced mathematical operations 
              with perfect accuracy.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              to="/calculator"
              className="btn-primary flex items-center space-x-2 text-lg"
            >
              <Calculator className="w-5 h-5" />
              <span>Launch Calculator</span>
            </Link>
            
            <Link
              to="/test"
              className="btn-secondary flex items-center space-x-2 text-lg"
            >
              <TestTube className="w-5 h-5" />
              <span>Run Tests</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-white/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Powerful Features
            </h2>
            <p className="text-lg text-gray-600">
              Everything you need for advanced mathematical computations
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="card text-center animate-slide-up hover:scale-105"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="mb-4 flex justify-center">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Operations Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Supported Operations
            </h2>
            <p className="text-lg text-gray-600">
              Comprehensive mathematical functionality
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Basic Arithmetic</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Addition (+)</li>
                <li>• Subtraction (-)</li>
                <li>• Multiplication (*)</li>
                <li>• Division (/)</li>
                <li>• Modulo (%)</li>
                <li>• Exponentiation (**)</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Advanced Functions</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Factorial (n!)</li>
                <li>• Square Root (√)</li>
                <li>• Logarithms (log)</li>
                <li>• Exponential (exp)</li>
                <li>• Power functions</li>
                <li>• Inverse operations</li>
              </ul>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Trigonometry</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Sine (sin)</li>
                <li>• Cosine (cos)</li>
                <li>• Tangent (tan)</li>
                <li>• Arcsine (arcsin)</li>
                <li>• Arccosine (arccos)</li>
                <li>• Arctangent (arctan)</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Calculate?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Experience the power of arbitrary precision mathematics
          </p>
          <Link
            to="/calculator"
            className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 active:translate-y-0 inline-flex items-center space-x-2"
          >
            <Calculator className="w-5 h-5" />
            <span>Start Calculating</span>
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage