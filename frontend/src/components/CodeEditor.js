// Code Editor Component
// Monaco-based code editor with syntax highlighting

import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';

const CodeEditor = ({ 
  value, 
  onChange, 
  language = 'python', 
  readOnly = false,
  height = '400px',
  theme = 'vs-dark'
}) => {
  const [editorValue, setEditorValue] = useState(value || '');

  useEffect(() => {
    if (value !== editorValue) {
      setEditorValue(value || '');
    }
  }, [value]);

  const handleEditorChange = (newValue) => {
    setEditorValue(newValue);
    if (onChange) {
      onChange(newValue);
    }
  };

  const handleEditorMount = (editor, monaco) => {
    // Configure editor options
    editor.updateOptions({
      minimap: { enabled: true },
      fontSize: 14,
      lineNumbers: 'on',
      scrollBeyondLastLine: false,
      automaticLayout: true,
      tabSize: 4,
      insertSpaces: true,
      wordWrap: 'on',
    });

    // Add custom themes if needed
    monaco.editor.defineTheme('ai-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [],
      colors: {
        'editor.background': '#1e1e2e',
      },
    });
  };

  return (
    <div style={{ border: '1px solid #3e3e5e', borderRadius: '8px', overflow: 'hidden' }}>
      <Editor
        height={height}
        language={language.toLowerCase()}
        value={editorValue}
        onChange={handleEditorChange}
        onMount={handleEditorMount}
        theme={theme}
        options={{
          readOnly,
          minimap: { enabled: true },
          fontSize: 14,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          insertSpaces: true,
          wordWrap: 'on',
          padding: { top: 16, bottom: 16 },
        }}
        loading={
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            height: height,
            background: '#1e1e2e',
            color: '#888'
          }}>
            Loading editor...
          </div>
        }
      />
    </div>
  );
};

export default CodeEditor;
