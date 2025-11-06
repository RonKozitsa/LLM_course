# Quick Start Guide - Angular

## Setup in 3 Steps:

### 1. Install Node.js & Angular CLI
```bash
# Install Node.js from https://nodejs.org (v18+)

# Install Angular CLI globally
npm install -g @angular/cli
```

### 2. Install Dependencies & Start Ollama
```bash
# Install project dependencies
npm install

# Start Ollama server (in another terminal)
ollama serve

# Pull a model
ollama pull gemma3:1b
```

### 3. Run the Application
```bash
npm start
# or
ng serve
```

Open browser to: **http://localhost:4200**

---

## Alternative: Use Scripts

```bash
# Make scripts executable
chmod +x install.sh run.sh

# Install everything
./install.sh

# Run the app
./run.sh
```

---

## Requirements
- **Node.js:** 18.x or higher
- **npm:** 9.x or higher
- **Angular CLI:** 17.x
- **Ollama:** Latest version
- **Modern browser** (Chrome, Firefox, Safari, Edge)

---

## Common Commands

### Development
```bash
npm start              # Start dev server
ng serve               # Alternative to npm start
ng build               # Build for production
ng test                # Run tests
```

### Ollama
```bash
ollama serve           # Start Ollama server
ollama list            # List installed models
ollama pull mistral    # Pull a model
```

---

## Popular Models

| Model | Size  | Best For                         |
|-------|-------|----------------------------------|
| **llama2** | 3.8GB | General purpose                  |
| **gemma3:1b** | 778MB | small model (used for this task) |
| **mistral** | 4.1GB | Fast & capable                   |
| **codellama** | 3.8GB | Code generation                  |
| **phi** | 1.6GB | Small & fast                     |
| **neural-chat** | 4.1GB | Conversations                    |

Pull any model:
```bash
ollama pull <model-name>
```

---

## Troubleshooting

### Can't connect to Ollama?
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Port 4200 already in use?
```bash
ng serve --port 4300
```

### Dependencies not installing?
```bash
rm -rf node_modules package-lock.json
npm install
```

---

That's it! Happy chatting! 🚀
