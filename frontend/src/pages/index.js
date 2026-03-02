// Main Page - AI Code Assistant
import { useState } from 'react';
import Head from 'next/head';
import CodeEditor from '../components/CodeEditor';
import apiService from '../services/api';

export default function Home() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('summarize');

  const actions = [
    { id: 'summarize', label: 'Summarize', icon: '📝' },
    { id: 'debug', label: 'Debug', icon: '🐛' },
    { id: 'explain', label: 'Explain', icon: '💡' },
    { id: 'optimize', label: 'Optimize', icon: '⚡' },
    { id: 'security', label: 'Security', icon: '🔒' },
  ];

  const handleSubmit = async () => {
    if (!code.trim()) return;
    
    setLoading(true);
    setResult(null);

    try {
      let response;
      
      switch (activeTab) {
        case 'summarize':
          response = await apiService.summarize(code, language);
          break;
        case 'debug':
          response = await apiService.debug(code, language);
          break;
        case 'explain':
          response = await apiService.explain(code, language);
          break;
        case 'optimize':
          response = await apiService.optimize(code, language);
          break;
        case 'security':
          response = await apiService.security(code, language);
          break;
        default:
          response = await apiService.summarize(code, language);
      }
      
      setResult(response);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: '#0f0f23', color: '#fff' }}>
      <Head>
        <title>AI Code Assistant</title>
        <meta name="description" content="AI-powered code analysis and debugging" />
      </Head>

      {/* Header */}
      <header style={{ 
        padding: '20px 40px', 
        borderBottom: '1px solid #2a2a4a',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h1 style={{ margin: 0, fontSize: '24px' }}>
          🔍 AI Code Assistant
        </h1>
        <div>
          <a href="/docs" style={{ color: '#7c3aed', marginRight: '20px' }}>API Docs</a>
          <a href="https://github.com" style={{ color: '#7c3aed' }}>GitHub</a>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ padding: '40px', maxWidth: '1400px', margin: '0 auto' }}>
        
        {/* Action Tabs */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          {actions.map((action) => (
            <button
              key={action.id}
              onClick={() => setActiveTab(action.id)}
              style={{
                padding: '12px 24px',
                background: activeTab === action.id ? '#7c3aed' : 'transparent',
                border: `1px solid ${activeTab === action.id ? '#7c3aed' : '#3e3e5e'}`,
                borderRadius: '8px',
                color: '#fff',
                cursor: 'pointer',
                fontSize: '14px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
              }}
            >
              <span>{action.icon}</span>
              {action.label}
            </button>
          ))}
        </div>

        {/* Editor and Result Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          
          {/* Code Input */}
          <div>
            <div style={{ marginBottom: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label style={{ color: '#888' }}>Code Input</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{
                  padding: '8px 16px',
                  background: '#1e1e2e',
                  border: '1px solid #3e3e5e',
                  borderRadius: '6px',
                  color: '#fff',
                }}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
                <option value="go">Go</option>
                <option value="rust">Rust</option>
              </select>
            </div>
            
            <CodeEditor
              value={code}
              onChange={setCode}
              language={language}
              height="500px"
            />

            <button
              onClick={handleSubmit}
              disabled={loading || !code.trim()}
              style={{
                width: '100%',
                padding: '16px',
                marginTop: '20px',
                background: loading ? '#4a4a6a' : '#7c3aed',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? 'Processing...' : `🚀 ${actions.find(a => a.id === activeTab)?.label || 'Analyze'} Code`}
            </button>
          </div>

          {/* Result */}
          <div>
            <div style={{ marginBottom: '10px' }}>
              <label style={{ color: '#888' }}>Analysis Result</label>
            </div>
            
            <div style={{
              height: '500px',
              background: '#1e1e2e',
              border: '1px solid #3e3e5e',
              borderRadius: '8px',
              padding: '20px',
              overflow: 'auto',
            }}>
              {result ? (
                <pre style={{ margin: 0, whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                  {JSON.stringify(result, null, 2)}
                </pre>
              ) : (
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  height: '100%',
                  color: '#666'
                }}>
                  Enter code and click analyze to see results
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
