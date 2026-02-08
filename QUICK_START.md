# 🚀 Quick Start Guide

Get your AI Text Summarizer running in minutes!

## ⚡ One-Command Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Git

### Step 1: Clone & Install
```bash
git clone <repository-url>
cd ai-text-summarizer

# Backend setup
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Frontend setup  
cd ../frontend
npm install
```

### Step 2: Configure Environment
```bash
cd backend
cp .env.example .env
# Edit .env with your API keys (optional)
```

### Step 3: Start Applications
```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Frontend  
cd frontend
npm run dev
```

### Step 4: Access Application
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

## 🎯 First Test

1. Open http://localhost:3000
2. Paste this text:
```
Artificial intelligence is transforming how we process and understand information. Machine learning algorithms can now analyze vast amounts of text data, identifying patterns and extracting key insights automatically. Natural language processing techniques enable computers to understand human language, making it possible to summarize long documents, answer questions, and even generate creative content. These advancements are revolutionizing industries from healthcare to finance, education to entertainment. As AI technology continues to evolve, we can expect even more sophisticated applications that will further enhance our ability to work with information efficiently and effectively.
```
3. Click "Summarize Text"
4. View your AI-generated summary!

## 🛠️ Troubleshooting

### Common Issues

**Backend won't start**
```bash
# Check Python version
python --version

# Install missing dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

**Frontend errors**
```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version
npm --version
```

**CORS errors**
- Ensure backend is running on port 8000
- Check frontend is on port 3000
- Verify .env CORS settings

**Model download issues**
```bash
# Test model loading
python -c "from transformers import pipeline; print('Models OK')"

# Clear Hugging Face cache (if needed)
rm -rf ~/.cache/huggingface
```

### Port Conflicts
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend

# Or use different ports
# Backend: python main.py --port 8001
# Frontend: npm run dev -- -p 3001
```

## 📱 Mobile Access

Access from your phone:
1. Ensure both services are running
2. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Mac/Linux  
   ifconfig
   ```
3. Use: `http://YOUR_IP:3000`

## 🔧 API Keys (Optional)

For enhanced features, add API keys to `.env`:

```env
# OpenAI (for GPT models)
OPENAI_API_KEY=sk-your-openai-key

# Cohere (for business models)  
COHERE_API_KEY=your-cohere-key
```

Free models (BART, T5, PEGASUS) work without API keys!

## 🎯 Next Steps

1. **Try file uploads** - Upload PDF, DOCX, or TXT files
2. **Test different models** - Compare BART, T5, PEGASUS results
3. **Export summaries** - Download as PDF, DOCX, TXT, or CSV
4. **Batch processing** - Summarize multiple texts at once
5. **Advanced settings** - Fine-tune summary length and quality

## 📚 Need Help?

- 📖 Full documentation: [README.md](README.md)
- 👤 User story: [docs/USER_STORY.md](docs/USER_STORY.md)
- 🧪 Testing guide: [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)
- 🔧 API docs: http://localhost:8000/docs

---

**Ready to transform your text processing? 🚀**
