import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [steps, setSteps] = useState(20);
  const [format, setFormat] = useState('png');
  const [useGpu, setUseGpu] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [generationId, setGenerationId] = useState(null);
  const [icons, setIcons] = useState(null);
  const [metadata, setMetadata] = useState(null);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setIcons(null);
    setMetadata(null);
    setGenerationId(null);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
          steps,
          format,
          use_gpu: useGpu
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Generation failed');
      }

      const data = await response.json();
      setGenerationId(data.generation_id);
      setIcons(data.icons);
      setMetadata(data.metadata);
    } catch (err) {
      setError(err.message);
      console.error('Generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadBundle = async () => {
    if (!generationId) return;
    try {
      const response = await fetch(`/api/download/bundle/${generationId}?format=${format}`);
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `pwa-icons-${generationId.substring(0, 8)}.zip`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Download failed: ' + err.message);
    }
  };

  const handleDownloadSingle = async (size) => {
    if (!generationId) return;
    try {
      const response = await fetch(`/api/download/single/${generationId}/${size}?format=${format}`);
      if (!response.ok) throw new Error('Download failed');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const filename = size === '16'
        ? `favicon-16x16.${format}`
        : `icon-${size}x${size}.${format}`;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Download failed: ' + err.message);
    }
  };

  const getIconLabel = (size) => {
    const labels = {
      '512': '512×512 - Large Icon',
      '192': '192×192 - Medium Icon',
      '164': '164×164 - Small Icon',
      '16': '16×16 - Favicon'
    };
    return labels[size] || size;
  };

  const getIconDescription = (size) => {
    const descriptions = {
      '512': 'App launcher, splash screen',
      '192': 'Home screen, app launcher',
      '164': 'Various UI elements',
      '16': 'Browser tab favicon'
    };
    return descriptions[size] || '';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎨 Cool PWA Icon Generator</h1>
        <p className="subtitle">Offline AI-Powered Progressive Web App Icon Maker</p>
      </header>

      <main className="App-main">
        <div className="controls-container">
          <div className="input-group">
            <label htmlFor="prompt">Icon Description</label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe your icon... (e.g., 'A modern blue gradient app icon with a rocket')"
              rows="3"
              disabled={loading}
            />
          </div>

          <div className="options-row">
            <div className="input-group">
              <label htmlFor="steps">Quality (Steps)</label>
              <select
                id="steps"
                value={steps}
                onChange={(e) => setSteps(Number(e.target.value))}
                disabled={loading}
              >
                <option value={20}>20 - Fast (~10-15s GPU)</option>
                <option value={50}>50 - High Quality (~20-30s GPU)</option>
              </select>
            </div>

            <div className="input-group">
              <label htmlFor="format">Format</label>
              <select
                id="format"
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                disabled={loading}
              >
                <option value="png">PNG (Recommended)</option>
                <option value="jpeg">JPEG</option>
              </select>
            </div>

            <div className="input-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={useGpu}
                  onChange={(e) => setUseGpu(e.target.checked)}
                  disabled={loading}
                />
                <span>Enable GPU Acceleration</span>
              </label>
              <small>Requires NVIDIA CUDA GPU</small>
            </div>
          </div>

          <button
            className="generate-button"
            onClick={handleGenerate}
            disabled={loading || !prompt.trim()}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Generating Icons...
              </>
            ) : (
              '✨ Generate All Icon Sizes'
            )}
          </button>

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          {metadata && (
            <div className="metadata-info">
              <div className="metadata-item">
                <strong>Generation Time:</strong> {metadata.generation_time_seconds}s
              </div>
              <div className="metadata-item">
                <strong>Device:</strong> {metadata.device.toUpperCase()}
              </div>
              <div className="metadata-item">
                <strong>Seed:</strong> {metadata.seed}
              </div>
            </div>
          )}
        </div>

        {icons && (
          <>
            <div className="preview-container">
              <h2>Generated Icons</h2>
              <p className="preview-subtitle">All sizes generated with identical design</p>
              
              <div className="icons-grid">
                {Object.entries(icons).map(([size, base64]) => (
                  <div key={size} className="icon-card">
                    <div className="icon-preview-wrapper">
                      <img
                        src={base64}
                        alt={`Icon ${size}x${size}`}
                        className={`icon-preview size-${size}`}
                      />
                    </div>
                    <div className="icon-info">
                      <h3>{getIconLabel(size)}</h3>
                      <p className="icon-usage">{getIconDescription(size)}</p>
                      <button
                        className="download-single-button"
                        onClick={() => handleDownloadSingle(size)}
                      >
                        ⬇️ Download
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="download-all-container">
              <button
                className="download-all-button"
                onClick={handleDownloadBundle}
              >
                📦 Download All as ZIP Bundle
              </button>
              <p className="download-note">
                Includes all 4 icon sizes + manifest.json template + README
              </p>
            </div>
          </>
        )}

        {!icons && !loading && (
          <div className="empty-state">
            <div className="empty-icon">🎨</div>
            <h3>Ready to Generate Icons</h3>
            <p>Enter a description above and click "Generate All Icon Sizes"</p>
            <div className="features-list">
              <div className="feature-item">✅ 4 PWA-compliant sizes (512, 192, 164, 16px)</div>
              <div className="feature-item">✅ AI-powered with Stable Diffusion + LoRA</div>
              <div className="feature-item">✅ Consistent design across all sizes</div>
              <div className="feature-item">✅ Download individually or as bundle</div>
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>
          Powered by <strong>Stable Diffusion 1.5</strong> with LoRA fine-tuning
          {metadata && metadata.device === 'cuda' && ' | GPU Accelerated ⚡'}
        </p>
      </footer>
    </div>
  );
}

export default App;