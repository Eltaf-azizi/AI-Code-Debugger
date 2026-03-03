// Result Viewer Component
// Displays analysis results with syntax highlighting

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';

const ResultViewer = ({ result, type = 'json' }) => {
  if (!result) {
    return (
      <div style={styles.empty}>
        Enter code and click analyze to see results
      </div>
    );
  }

  const renderContent = () => {
    // Handle error responses
    if (result.error) {
      return (
        <div style={styles.error}>
          <h3 style={styles.errorTitle}>Error</h3>
          <p>{result.error}</p>
        </div>
      );
    }

    // Handle different result types
    if (type === 'json') {
      return (
        <SyntaxHighlighter 
          language="json" 
          style={vscDarkPlus}
          customStyle={{
            margin: 0,
            padding: '20px',
            background: 'transparent',
            fontSize: '14px'
          }}
        >
          {JSON.stringify(result, null, 2)}
        </SyntaxHighlighter>
      );
    }

    // Plain text
    return <pre style={styles.pre}>{result}</pre>;
  };

  return (
    <div style={styles.container}>
      {renderContent()}
    </div>
  );
};

const styles = {
  container: {
    height: '100%',
    background: '#1e1e2e',
    border: '1px solid #3e3e5e',
    borderRadius: '8px',
    overflow: 'auto',
  },
  empty: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%',
    color: '#666',
    fontSize: '14px',
  },
  error: {
    padding: '20px',
    color: '#ff6b6b',
  },
  errorTitle: {
    marginBottom: '10px',
    color: '#ff6b6b',
  },
  pre: {
    margin: 0,
    padding: '20px',
    whiteSpace: 'pre-wrap',
    fontFamily: 'monospace',
    fontSize: '14px',
  }
};

export default ResultViewer;
