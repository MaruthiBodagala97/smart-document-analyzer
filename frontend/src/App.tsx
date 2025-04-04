import React, { useState } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  ThemeProvider,
  createTheme
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

// Create a theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

interface AnalysisResult {
  summary: string;
  key_points: string[];
  sentiment: string;
  topics: string[];
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
      setAnalysis(null);
      setError(null);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  const analyzeDocument = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setAnalysis(response.data);
    } catch (err) {
      setError('Error analyzing document. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="md">
        <Box sx={{ my: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Smart Document Analyzer
          </Typography>
          
          <Paper 
            {...getRootProps()} 
            sx={{ 
              p: 3, 
              textAlign: 'center', 
              cursor: 'pointer',
              backgroundColor: isDragActive ? '#f0f8ff' : 'white',
              border: '2px dashed #1976d2',
              mb: 3
            }}
          >
            <input {...getInputProps()} />
            {isDragActive ? (
              <Typography>Drop the file here...</Typography>
            ) : (
              <Typography>
                Drag and drop a document here, or click to select a file
              </Typography>
            )}
          </Paper>

          {file && (
            <Box sx={{ mb: 3, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom>
                Selected file: {file.name}
              </Typography>
              <Chip 
                label="Analyze" 
                onClick={analyzeDocument} 
                color="primary" 
                sx={{ mt: 1 }}
              />
            </Box>
          )}

          {loading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
              <CircularProgress />
            </Box>
          )}

          {error && (
            <Typography color="error" align="center" sx={{ my: 2 }}>
              {error}
            </Typography>
          )}

          {analysis && (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Analysis Results
              </Typography>

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Summary
              </Typography>
              <Typography paragraph>
                {analysis.summary}
              </Typography>

              <Typography variant="h6" gutterBottom>
                Key Points
              </Typography>
              <List>
                {analysis.key_points.map((point, index) => (
                  <ListItem key={index}>
                    <ListItemText primary={point} />
                  </ListItem>
                ))}
              </List>

              <Typography variant="h6" gutterBottom>
                Sentiment
              </Typography>
              <Chip 
                label={analysis.sentiment} 
                color={
                  analysis.sentiment.toLowerCase().includes('positive') ? 'success' :
                  analysis.sentiment.toLowerCase().includes('negative') ? 'error' :
                  'default'
                }
              />

              <Typography variant="h6" gutterBottom sx={{ mt: 2 }}>
                Topics
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {analysis.topics.map((topic, index) => (
                  <Chip key={index} label={topic} />
                ))}
              </Box>
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 