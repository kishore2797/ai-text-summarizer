# 🧪 Comprehensive Testing Guide

## 📋 Testing Overview

This guide provides comprehensive testing procedures for the AI Text Summarizer application, covering manual testing, automated testing, performance testing, and user acceptance testing.

## 🎯 Testing Objectives

1. **Functional Testing**: Verify all features work as expected
2. **Performance Testing**: Ensure acceptable response times
3. **Usability Testing**: Validate user experience
4. **Integration Testing**: Test component interactions
5. **Security Testing**: Verify data protection measures

## 🧪 Manual Testing Checklist

### 1. Basic Functionality Tests

#### Text Input Testing
- [ ] **Minimum Length Validation**
  - Input: 49 characters → Should show error
  - Input: 50 characters → Should accept
  - Input: 10,000 characters → Should accept
  - Input: Empty text → Should show error

- [ ] **Text Processing**
  - Plain text with punctuation
  - Text with special characters (@, #, $, %)
  - Text with numbers and dates
  - Text in different formats (paragraphs, lists, tables)

#### File Upload Testing
- [ ] **Supported Formats**
  - PDF file (text-based) → Should extract text
  - DOCX file → Should extract text
  - TXT file → Should extract text
  - Scanned PDF → Should show appropriate error

- [ ] **File Size Limits**
  - Small file (< 1KB) → Should work
  - Large file (5MB) → Should work
  - Oversized file (> 10MB) → Should show error

- [ ] **File Error Handling**
  - Corrupted PDF → Should show error
  - Password-protected file → Should show error
  - Unsupported format (image, video) → Should show error

#### Summarization Methods
- [ ] **Extractive Method**
  - Short text (100 words) → Should work
  - Medium text (500 words) → Should work
  - Long text (2000 words) → Should work

- [ ] **Abstractive Method**
  - Test with all AI models (BART, T5, PEGASUS)
  - Verify output is coherent and readable
  - Check for appropriate length

- [ ] **Hybrid Method**
  - Combine extractive + abstractive
  - Verify quality improvement
  - Check processing time

#### AI Model Testing
- [ ] **BART Model**
  - General purpose text
  - News articles
  - Research papers

- [ ] **T5 Model**
  - Short to medium texts
  - Conversational content
  - Technical documentation

- [ ] **PEGASUS Model**
  - Long documents
  - Academic papers
  - Legal documents

- [ ] **OpenAI Model** (if API key configured)
  - Premium quality requirements
  - Complex content
  - Multiple languages

- [ ] **Cohere Model** (if API key configured)
  - Business documents
  - Professional content
  - Industry-specific text

### 2. Advanced Features Testing

#### Batch Processing
- [ ] **Multiple Texts**
  - 2 texts simultaneously
  - 5 texts simultaneously
  - 10 texts simultaneously (maximum)

- [ ] **Mixed Content**
  - Different text lengths
  - Different formats
  - Different languages

#### Export Functionality
- [ ] **PDF Export**
  - Verify PDF generation
  - Check content formatting
  - Validate metadata inclusion

- [ ] **DOCX Export**
  - Verify Word document creation
  - Check editability
  - Validate formatting

- [ ] **TXT Export**
  - Verify plain text file
  - Check content accuracy
  - Validate encoding

- [ ] **CSV Export**
  - Verify CSV structure
  - Check data fields
  - Validate metadata

#### Settings and Configuration
- [ ] **Advanced Settings**
  - Max sentences (1-20 range)
  - Max length (50-500 words)
  - Min length (10-200 words)
  - Boundary validation

### 3. User Interface Testing

#### Responsive Design
- [ ] **Desktop View** (1920x1080)
  - Layout alignment
  - Element visibility
  - Interaction areas

- [ ] **Tablet View** (768x1024)
  - Responsive layout
  - Touch interactions
  - Navigation

- [ ] **Mobile View** (375x667)
  - Compact layout
  - Mobile controls
  - Scrolling behavior

#### Browser Compatibility
- [ ] **Chrome** (latest version)
- [ ] **Firefox** (latest version)
- [ ] **Safari** (latest version)
- [ ] **Edge** (latest version)

#### Accessibility Testing
- [ ] **Keyboard Navigation**
  - Tab order logical
  - All controls accessible
  - Focus indicators visible

- [ ] **Screen Reader Support**
  - Alt text for images
  - Semantic HTML structure
  - ARIA labels

### 4. Error Handling Testing

#### Network Errors
- [ ] **Backend Offline**
  - Show appropriate error message
  - Graceful degradation
  - Retry mechanism

- [ ] **Slow Response**
  - Loading indicators
  - Timeout handling
  - User feedback

#### Validation Errors
- [ ] **Input Validation**
  - Real-time validation feedback
  - Clear error messages
  - Correction guidance

- [ ] **API Errors**
  - 400 Bad Request handling
  - 500 Server Error handling
  - Network timeout handling

## 🤖 Automated Testing

### Backend Tests

#### Unit Tests
```python
# tests/test_summarizer_service.py
import pytest
from services.summarizer_service import SummarizerService
from models.summarizer import SummarizationRequest

class TestSummarizerService:
    def setup_method(self):
        self.service = SummarizerService()
    
    def test_short_text_summarization(self):
        request = SummarizationRequest(
            text="This is a test text for summarization. " * 10,
            method="extractive",
            max_sentences=3
        )
        result = self.service.summarize_text(request)
        assert result.summary is not None
        assert len(result.summary.split()) <= request.max_length
    
    def test_text_length_validation(self):
        with pytest.raises(ValueError):
            request = SummarizationRequest(text="Short")
            self.service.summarize_text(request)
    
    def test_model_selection(self):
        for model in ["bart", "t5", "pegasus"]:
            request = SummarizationRequest(
                text="Test text " * 50,
                model=model
            )
            result = self.service.summarize_text(request)
            assert result.model == model
```

#### Integration Tests
```python
# tests/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_summarize_endpoint():
    response = client.post("/api/v1/summarize/summarize", json={
        "text": "This is a test text for the API endpoint. " * 20,
        "method": "hybrid",
        "model": "bart",
        "max_sentences": 5,
        "max_length": 150,
        "min_length": 50
    })
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "compression_ratio" in data

def test_file_upload_endpoint():
    with open("test_document.pdf", "rb") as f:
        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.pdf", f, "application/pdf")},
            data={"extract_text": "true"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["text_extracted"] == True

def test_export_endpoint():
    response = client.post("/api/v1/export/export", json={
        "content": "Test summary content",
        "filename": "test_summary",
        "format": "pdf"
    })
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
```

#### Performance Tests
```python
# tests/test_performance.py
import time
import pytest
from services.summarizer_service import SummarizerService

class TestPerformance:
    def setup_method(self):
        self.service = SummarizerService()
    
    def test_response_time_short_text(self):
        start_time = time.time()
        request = SummarizationRequest(
            text="Test text " * 50,  # ~250 words
            method="extractive"
        )
        self.service.summarize_text(request)
        processing_time = time.time() - start_time
        assert processing_time < 5.0  # Should be under 5 seconds
    
    def test_response_time_long_text(self):
        start_time = time.time()
        request = SummarizationRequest(
            text="Test text " * 500,  # ~2500 words
            method="hybrid"
        )
        self.service.summarize_text(request)
        processing_time = time.time() - start_time
        assert processing_time < 30.0  # Should be under 30 seconds
```

### Frontend Tests

#### Component Tests
```typescript
// src/components/__tests__/SummarizerForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import SummarizerForm from '../SummarizerForm'

describe('SummarizerForm', () => {
  const mockOnSummarize = jest.fn()
  
  it('renders form elements correctly', () => {
    render(<SummarizerForm onSummarize={mockOnSummarize} loading={false} />)
    
    expect(screen.getByLabelText('Text to Summarize')).toBeInTheDocument()
    expect(screen.getByDisplayValue('hybrid')).toBeInTheDocument()
    expect(screen.getByDisplayValue('bart')).toBeInTheDocument()
  })
  
  it('validates minimum text length', async () => {
    render(<SummarizerForm onSummarize={mockOnSummarize} loading={false} />)
    
    const textarea = screen.getByLabelText('Text to Summarize')
    const submitButton = screen.getByText('Summarize Text')
    
    fireEvent.change(textarea, { target: { value: 'Short text' } })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(screen.getByText(/Please enter at least 50 characters/)).toBeInTheDocument()
    })
  })
  
  it('calls onSummarize with correct parameters', async () => {
    render(<SummarizerForm onSummarize={mockOnSummarize} loading={false} />)
    
    const textarea = screen.getByLabelText('Text to Summarize')
    const submitButton = screen.getByText('Summarize Text')
    
    fireEvent.change(textarea, { 
      target: { value: 'This is a test text that is long enough for summarization. ' * 5 } 
    })
    fireEvent.click(submitButton)
    
    await waitFor(() => {
      expect(mockOnSummarize).toHaveBeenCalledWith({
        text: expect.any(String),
        method: 'hybrid',
        model: 'bart',
        max_sentences: 5,
        max_length: 150,
        min_length: 50
      })
    })
  })
})
```

#### Integration Tests
```typescript
// src/__tests__/integration.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Home from '../app/page'

// Mock fetch
global.fetch = jest.fn()

describe('Application Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })
  
  it('completes full summarization workflow', async () => {
    ;(fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        summary: 'This is a generated summary.',
        method: 'hybrid',
        model: 'bart',
        original_length: 100,
        summary_length: 25,
        compression_ratio: 0.25,
        processing_time: 1.5
      })
    })
    
    render(<Home />)
    
    // Enter text
    const textarea = screen.getByLabelText('Text to Summarize')
    fireEvent.change(textarea, { 
      target: { value: 'Test text that is long enough for summarization. ' * 10 } 
    })
    
    // Submit form
    const submitButton = screen.getByText('Summarize Text')
    fireEvent.click(submitButton)
    
    // Wait for results
    await waitFor(() => {
      expect(screen.getByText('Summary Result')).toBeInTheDocument()
    })
    
    // Verify summary displayed
    expect(screen.getByText('This is a generated summary.')).toBeInTheDocument()
  })
})
```

## 📊 Performance Testing

### Load Testing

#### Concurrent Users
```bash
# Using Apache Bench (ab)
ab -n 100 -c 10 http://localhost:8000/api/v1/summarize/summarize

# Using wrk (more advanced)
wrk -t12 -c400 -d30s --script=scripts/post_summarize.lua http://localhost:8000/
```

#### Stress Testing Script
```python
# tests/stress_test.py
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def stress_test():
    urls = ["http://localhost:8000/api/v1/summarize/summarize"] * 100
    payload = {
        "text": "Stress test text. " * 100,
        "method": "extractive",
        "model": "bart"
    }
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(
                session.post(url, json=payload)
            )
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        success_count = sum(1 for r in responses if r.status == 200)
        total_time = end_time - start_time
        
        print(f"Successful requests: {success_count}/{len(urls)}")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Requests per second: {len(urls)/total_time:.2f}")

if __name__ == "__main__":
    asyncio.run(stress_test())
```

### Memory Testing
```python
# tests/memory_test.py
import psutil
import os
from services.summarizer_service import SummarizerService

def test_memory_usage():
    process = psutil.Process(os.getpid())
    service = SummarizerService()
    
    # Baseline memory
    baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Process multiple large texts
    for i in range(50):
        large_text = "Memory test text. " * 1000
        request = SummarizationRequest(text=large_text)
        service.summarize_text(request)
    
    # Peak memory
    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = peak_memory - baseline_memory
    
    print(f"Baseline memory: {baseline_memory:.2f} MB")
    print(f"Peak memory: {peak_memory:.2f} MB")
    print(f"Memory increase: {memory_increase:.2f} MB")
    
    # Assert memory usage is reasonable (< 500MB increase)
    assert memory_increase < 500, f"Memory usage increased by {memory_increase} MB"
```

## 🔒 Security Testing

### Input Validation
```python
# tests/test_security.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sql_injection_protection():
    malicious_input = "'; DROP TABLE users; --"
    response = client.post("/api/v1/summarize/summarize", json={
        "text": malicious_input * 100,
        "method": "extractive"
    })
    # Should not cause server error
    assert response.status_code in [200, 400]

def test_xss_protection():
    xss_payload = "<script>alert('xss')</script>"
    response = client.post("/api/v1/summarize/summarize", json={
        "text": xss_payload * 50,
        "method": "extractive"
    })
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        # Summary should not contain executable scripts
        summary = response.json().get("summary", "")
        assert "<script>" not in summary

def test_file_upload_security():
    # Test malicious file upload
    malicious_content = b"<?php system($_GET['cmd']); ?>"
    response = client.post(
        "/api/v1/files/upload",
        files={"file": ("malicious.php", malicious_content, "application/x-php")}
    )
    assert response.status_code == 400
```

## 📱 User Acceptance Testing

### User Scenarios

#### Scenario 1: Research Analyst
```gherkin
Feature: Research Document Summarization
  As a research analyst
  I want to quickly summarize research papers
  So that I can extract key insights efficiently

  Scenario: Summarize academic paper
    Given I am on the summarizer page
    And I have a 20-page research paper (PDF)
    When I upload the PDF file
    And I select "PEGASUS" model
    And I set max sentences to 10
    And I click "Summarize Text"
    Then I should see a summary within 60 seconds
    And the summary should be 8-12 sentences
    And I should be able to export as PDF
```

#### Scenario 2: Business Professional
```gherkin
Feature: Business Report Processing
  As a business professional
  I want to summarize multiple business reports
  So that I can prepare for client meetings

  Scenario: Batch process business documents
    Given I have 5 business reports
    When I upload all files simultaneously
    And I select "Hybrid" method
    And I click "Batch Process"
    Then I should see progress indicators
    And all summaries should complete within 5 minutes
    And I should be able to export all summaries
```

### Usability Testing Script
```javascript
// tests/usability_test.js
const { test, expect } = require('@playwright/test');

test.describe('Usability Tests', () => {
  test('first-time user experience', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Check if page loads properly
    await expect(page.locator('h1')).toContainText('AI Text Summarizer');
    
    // Check if instructions are clear
    await expect(page.locator('text=Transform Long Text')).toBeVisible();
    
    // Test user guidance
    await page.fill('[data-testid="text-input"]', '');
    await page.click('[data-testid="summarize-button"]');
    await expect(page.locator('text=minimum 50 characters')).toBeVisible();
  });
  
  test('workflow efficiency', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Time the complete workflow
    const startTime = Date.now();
    
    await page.fill('[data-testid="text-input"]', 'Test text '.repeat(20));
    await page.selectOption('[data-testid="method-select"]', 'hybrid');
    await page.selectOption('[data-testid="model-select"]', 'bart');
    await page.click('[data-testid="summarize-button"]');
    
    // Wait for results
    await page.waitForSelector('[data-testid="summary-result"]');
    
    const endTime = Date.now();
    const totalTime = (endTime - startTime) / 1000;
    
    // Workflow should complete within reasonable time
    expect(totalTime).toBeLessThan(120); // 2 minutes max
  });
});
```

## 📋 Test Execution Plan

### Daily Tests
- [ ] Smoke tests (basic functionality)
- [ ] API health checks
- [ ] Database connectivity

### Weekly Tests
- [ ] Full regression suite
- [ ] Performance benchmarks
- [ ] Security scans

### Release Tests
- [ ] Complete test suite
- [ ] Load testing
- [ ] User acceptance testing
- [ ] Documentation verification

## 🚀 Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v --cov=.
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm run test
      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e
```

## 📊 Test Metrics and KPIs

### Coverage Targets
- **Backend Code Coverage**: > 90%
- **Frontend Code Coverage**: > 85%
- **API Endpoint Coverage**: 100%
- **User Flow Coverage**: > 95%

### Performance Benchmarks
- **API Response Time**: < 2 seconds (95th percentile)
- **Page Load Time**: < 3 seconds
- **File Processing**: < 30 seconds for 10MB files
- **Concurrent Users**: Support 100+ simultaneous users

### Quality Metrics
- **Bug Detection Rate**: > 95%
- **False Positive Rate**: < 5%
- **Test Execution Time**: < 10 minutes for full suite
- **Environment Setup Time**: < 5 minutes

---

This comprehensive testing guide ensures the AI Text Summarizer meets high quality standards and provides reliable performance for all users.
