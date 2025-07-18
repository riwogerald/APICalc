import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import CalculatorPage from './pages/CalculatorPage'
import TestPage from './pages/TestPage'
import Layout from './components/Layout'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/calculator" element={<CalculatorPage />} />
        <Route path="/test" element={<TestPage />} />
      </Routes>
    </Layout>
  )
}

export default App