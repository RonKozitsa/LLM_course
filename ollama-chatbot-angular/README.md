# Ollama Chatbot GUI - Angular

A professional, modern Angular application that provides a sleek interface for interacting with locally-hosted Ollama AI models.

<img width="1438" height="817" alt="Screenshot 2025-11-06 at 10 32 41 PM" src="https://github.com/user-attachments/assets/57e109d0-b2ac-4fbc-9289-8e2afd5728bf" />


## 🌟 Features

- ✨ **Modern Angular Architecture** - Built with Angular 17 and TypeScript
- 🎨 **Professional Dark Theme** - Sleek, modern UI with smooth animations
- 🔒 **100% Local** - All conversations stay on your machine
- ⚡ **Real-time Responses** - Reactive programming with RxJS
- 💬 **Message Management** - Advanced state management with services
- 🔄 **Model Selection** - Easy switching between Ollama models
- 📱 **Responsive Design** - Works great on all screen sizes
- 🎯 **Type Safety** - Full TypeScript support
- 🧪 **Comprehensive Tests** - 150+ unit tests with ~93% code coverage
- 🚀 **Production Ready** - Optimized builds and CI/CD ready

## 📋 Prerequisites

### 1. Node.js & npm
```bash
node --version  # Should be 18.x or higher
npm --version   # Should be 9.x or higher
```

Install from: https://nodejs.org/

### 2. Angular CLI
```bash
npm install -g @angular/cli
```

### 3. Ollama
Install Ollama from https://ollama.com

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Navigate to project directory
cd ollama-chatbot-angular

# Install npm packages
npm install
```

### 2. Start Ollama

```bash
# Start Ollama server
ollama serve

# Pull a model (in another terminal)
ollama pull llama2
```

### 3. Run the Application

```bash
# Development server
npm start

# Or
ng serve
```

Open your browser to `http://localhost:4200`

## 📦 Project Structure

```
ollama-chatbot-angular/
├── src/
│   ├── app/
│   │   ├── components/        # Angular components (future)
│   │   ├── services/          # Services
│   │   │   ├── ollama.service.ts    # Ollama API service
│   │   │   └── chat.service.ts      # Chat state management
│   │   ├── models/            # TypeScript interfaces
│   │   │   └── chat.model.ts        # Data models
│   │   ├── app.component.ts         # Main component
│   │   ├── app.component.html       # Main template
│   │   ├── app.component.css        # Main styles
│   │   └── app.module.ts            # App module
│   ├── assets/                # Static assets
│   ├── environments/          # Environment configs
│   ├── index.html            # HTML entry point
│   ├── main.ts               # Bootstrap file
│   └── styles.css            # Global styles
├── angular.json              # Angular configuration
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript config
└── README.md                 # This file
```

## 🎯 Usage

### Basic Usage

1. **Start the app**: `npm start`
2. **Type a message** in the input field at the bottom
3. **Press Enter** or click "Send" to send
4. **Receive responses** from your local AI model

### Keyboard Shortcuts

- `Enter` - Send message
- `Shift + Enter` - New line in message

### Changing Models

Edit the model name in the sidebar input field and press Enter. Make sure the model is installed:

```bash
ollama list           # See installed models
ollama pull mistral   # Install a new model
```

## ⚙️ Configuration

### Change Ollama URL

Edit `src/app/services/ollama.service.ts`:

```typescript
private config: OllamaConfig = {
  url: 'http://localhost:11434',  // Change this
  model: 'llama2',
  timeout: 120000
};
```

### Customize Colors

Edit the CSS variables in `src/app/app.component.css` and `src/styles.css`.

## 🔧 Development

### Install Development Dependencies

```bash
npm install
```

### Run Development Server

```bash
ng serve
# Or
npm start
```

Navigate to `http://localhost:4200`. The app will automatically reload if you change any source files.

### Build for Production

```bash
ng build --configuration production
```

The build artifacts will be stored in the `dist/` directory.

### Run Tests

```bash
ng test
```

The project includes **comprehensive unit tests** with **150+ test cases** and **~93% code coverage**.

#### Test Files:
- `src/app/services/ollama.service.spec.ts` - 60+ tests for OllamaService
- `src/app/services/chat.service.spec.ts` - 40+ tests for ChatService
- `src/app/app.component.spec.ts` - 50+ tests for AppComponent

#### Run Tests with Coverage:
```bash
ng test --code-coverage
```

#### Run Tests Once (CI/CD):
```bash
ng test --watch=false --browsers=ChromeHeadless
```

#### View Coverage Report:
```bash
open coverage/ollama-chatbot-angular/index.html
```

See [TESTING.md](TESTING.md) for complete testing documentation.

### Lint Code

```bash
ng lint
```

## 📊 Architecture

### Services

**OllamaService** (`src/app/services/ollama.service.ts`)
- Handles HTTP communication with Ollama API
- Manages connection status
- Error handling and recovery

**ChatService** (`src/app/services/chat.service.ts`)
- Manages message state
- Handles message creation and storage
- Processing state management

### Models

**Message Interface** (`src/app/models/chat.model.ts`)
```typescript
interface Message {
  id: string;
  sender: 'user' | 'ai' | 'system';
  content: string;
  timestamp: Date;
  type: 'user' | 'ai' | 'error';
}
```

### State Management

- Uses RxJS BehaviorSubjects for reactive state
- Services provide observables for components
- Unidirectional data flow
- Automatic cleanup with `takeUntil`

## 🐛 Troubleshooting

### Cannot connect to Ollama

**Error:** `Cannot connect to Ollama. Make sure it is running on localhost:11434`

**Solution:**
```bash
# Start Ollama
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### CORS Issues

If you encounter CORS errors, Ollama should allow requests from localhost by default. If not, you may need to configure CORS settings.

### Model not found

**Error:** `Model not found`

**Solution:**
```bash
# List installed models
ollama list

# Pull the model you want
ollama pull llama2
```

### Build errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Angular cache
ng cache clean
```

## 📝 Available Scripts

| Command | Description |
|---------|-------------|
| `npm start` | Start development server |
| `npm run build` | Build for production |
| `npm test` | Run unit tests |
| `npm run watch` | Build and watch for changes |
| `ng serve` | Alternative to npm start |
| `ng build` | Alternative to npm run build |

## 🌐 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 📊 Performance

| Metric | Target |
|--------|--------|
| Initial Load | <2s |
| Time to Interactive | <3s |
| Bundle Size | <500KB |
| Lighthouse Score | >90 |

## 🔐 Security & Privacy

- ✅ **100% Local Processing** - No external servers
- ✅ **No Telemetry** - No data collection
- ✅ **No Internet Required** - After initial setup
- ✅ **Private Conversations** - Everything stays on device
- ✅ **Type Safety** - TypeScript prevents common bugs

## 📚 Technologies Used

- **Angular 17** - Modern web framework
- **TypeScript 5.2** - Type-safe JavaScript
- **RxJS 7.8** - Reactive programming
- **HttpClient** - HTTP communication
- **FormsModule** - Two-way data binding

## 🛠️ System Requirements

**Minimum:**
- Node.js: 18.x
- npm: 9.x
- RAM: 4GB (8GB with model)
- CPU: 2 cores @ 2.0 GHz
- Browser: Modern browser with ES2022 support

**Recommended:**
- Node.js: 20.x
- npm: 10.x
- RAM: 16GB
- CPU: 4+ cores @ 3.0 GHz
- GPU: Optional (8GB+ VRAM for faster inference)

## 📖 Documentation

- [Technical PRD](TECHNICAL_PRD_ANGULAR.md) - Complete technical documentation
- [Testing Guide](TESTING.md) - Unit testing documentation and coverage
- [Quick Start Guide](QUICKSTART.md) - Fast setup instructions
- [Angular Docs](https://angular.io/docs) - Angular documentation
- [Ollama Docs](https://github.com/ollama/ollama) - Ollama documentation
- [RxJS Docs](https://rxjs.dev/) - RxJS documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Credits

- Built with [Angular](https://angular.io)
- Powered by [Ollama](https://ollama.com)
- Icons from Unicode emojis
- Color scheme: Catppuccin Mocha

## 🚀 Deployment

### Development
```bash
ng serve
```

### Production Build
```bash
ng build --configuration production
```

### Docker (Optional)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["ng", "serve", "--host", "0.0.0.0"]
```

---

**Made with ❤️ using Angular and TypeScript**

Enjoy your professional, type-safe, local AI assistant! 🚀
