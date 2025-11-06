# Technical Product Requirements Document (PRD)
## Ollama Chatbot GUI - Angular Version

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Status:** Final  
**Technology Stack:** Angular 17 + TypeScript 5.2  
**Owner:** Engineering Team  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [Technical Architecture](#3-technical-architecture)
4. [Angular Architecture](#4-angular-architecture)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [System Requirements](#7-system-requirements)
8. [API Specifications](#8-api-specifications)
9. [Component Specifications](#9-component-specifications)
10. [Service Layer](#10-service-layer)
11. [Data Models](#11-data-models)
12. [State Management](#12-state-management)
13. [Error Handling](#13-error-handling)
14. [Security & Privacy](#14-security--privacy)
15. [Performance Requirements](#15-performance-requirements)
16. [Testing Strategy](#16-testing-strategy)
17. [Build & Deployment](#17-build--deployment)
18. [Future Enhancements](#18-future-enhancements)

---

## 1. Executive Summary

### 1.1 Purpose
Develop a professional, production-ready Angular application that provides a modern, type-safe interface for interacting with locally-hosted Ollama AI models, ensuring complete privacy, excellent performance, and maintainability.

### 1.2 Goals
- Create an enterprise-grade Angular application with best practices
- Implement reactive programming patterns with RxJS
- Ensure full TypeScript type safety across the codebase
- Provide excellent user experience with smooth animations
- Maintain 100% local processing for privacy
- Support multiple Ollama models with easy switching
- Achieve >90 Lighthouse score

### 1.3 Success Metrics
- Time to Interactive: <3s
- Lighthouse Performance Score: >90
- Type Coverage: 100%
- Test Coverage: >80%
- Bundle Size: <500KB (gzipped)
- First Contentful Paint: <1.5s

---

## 2. Product Overview

### 2.1 Product Description
A professional Angular 17 application built with TypeScript that serves as a modern, reactive frontend for Ollama, enabling users to interact with large language models through an intuitive chat interface with full type safety and excellent developer experience.

### 2.2 Target Users
- **Primary:** Developers requiring type-safe, maintainable AI interface
- **Secondary:** Technical teams needing enterprise-grade local AI solution
- **Tertiary:** Organizations requiring GDPR-compliant AI tools

### 2.3 Key Differentiators
- **Angular 17:** Latest Angular with standalone components support
- **Full TypeScript:** 100% type-safe codebase
- **Reactive Programming:** RxJS for elegant state management
- **Modern Architecture:** Services, dependency injection, observables
- **Professional UI:** Smooth animations and transitions
- **Enterprise-Ready:** Scalable, testable, maintainable

---

## 3. Technical Architecture

### 3.1 High-Level Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Angular Application                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Presentation Layer                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │ │
│  │  │   AppComponent  │  Future       │  │   Future     │  │ │
│  │  │   (Main View) │  │  Components │  │  Components  │  │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                            ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Service Layer (Business Logic)             │ │
│  │  ┌──────────────────┐  ┌──────────────────────────┐    │ │
│  │  │  ChatService     │  │  OllamaService           │    │ │
│  │  │  (State Mgmt)    │  │  (API Communication)     │    │ │
│  │  └──────────────────┘  └──────────────────────────┘    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                            ↓                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Data Layer (Models & Types)                │ │
│  │  Message, OllamaConfig, OllamaResponse, etc.            │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                            ↓
         ┌──────────────────────────────────────┐
         │      Angular HTTP Client             │
         │      (HttpClientModule)              │
         └──────────────────────────────────────┘
                            ↓
         ┌──────────────────────────────────────┐
         │         Ollama REST API              │
         │      (http://localhost:11434)        │
         └──────────────────────────────────────┘
```

### 3.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Framework | Angular | 17.0.0 | Frontend framework |
| Language | TypeScript | 5.2.2 | Type-safe JavaScript |
| Reactive | RxJS | 7.8.0 | Reactive programming |
| HTTP | HttpClient | Angular | API communication |
| Forms | FormsModule | Angular | Two-way data binding |
| Build | Angular CLI | 17.0.0 | Build toolchain |
| Testing | Jasmine/Karma | Latest | Unit testing |

### 3.3 Module Structure

```
AppModule (Root)
├── BrowserModule
├── HttpClientModule (HTTP communication)
├── FormsModule (Form handling)
├── CommonModule (Common directives)
├── AppComponent
├── Services
│   ├── OllamaService (providedIn: 'root')
│   └── ChatService (providedIn: 'root')
└── Models
    └── chat.model.ts (interfaces)
```

---

## 4. Angular Architecture

### 4.1 Component Architecture

#### AppComponent (Root Component)
**Responsibility:** Main application container and orchestration

**Inputs:** None (root component)

**Outputs:** None

**Dependencies:**
- OllamaService (injected)
- ChatService (injected)

**State:**
- messages: Message[]
- currentModel: string
- connectionStatus: ConnectionStatus
- isProcessing: boolean
- userInput: string

**Lifecycle Hooks:**
- ngOnInit(): Initialize subscriptions
- ngOnDestroy(): Cleanup subscriptions

### 4.2 Service Architecture

#### OllamaService
**Responsibility:** HTTP communication with Ollama API

**Public API:**
```typescript
class OllamaService {
  connectionStatus$: Observable<ConnectionStatus>
  
  checkConnection(): void
  generateResponse(prompt: string, model?: string): Observable<string>
  getCurrentModel(): string
  setModel(model: string): void
  getUrl(): string
  setUrl(url: string): void
}
```

**State Management:**
- Uses BehaviorSubject for connection status
- Provides observable streams
- Singleton service (providedIn: 'root')

#### ChatService
**Responsibility:** Message state management

**Public API:**
```typescript
class ChatService {
  messages$: Observable<Message[]>
  isProcessing$: Observable<boolean>
  
  addMessage(message: Message): void
  createUserMessage(content: string): Message
  createAIMessage(content: string): Message
  createErrorMessage(content: string): Message
  clearMessages(): void
  setProcessing(isProcessing: boolean): void
  getMessages(): Message[]
}
```

**State Management:**
- BehaviorSubjects for reactive state
- Immutable state updates
- Centralized message management

### 4.3 Data Flow

```
User Input
    ↓
AppComponent.sendMessage()
    ↓
ChatService.addMessage(userMessage)
    ↓
ChatService.setProcessing(true)
    ↓
OllamaService.generateResponse()
    ↓
[Observable pipeline with RxJS operators]
    ↓
ChatService.addMessage(aiMessage)
    ↓
ChatService.setProcessing(false)
    ↓
View Updates (via async pipe)
```

### 4.4 Dependency Injection

```typescript
// Service registration
@Injectable({
  providedIn: 'root'  // Singleton across app
})

// Service injection
constructor(
  private ollamaService: OllamaService,
  private chatService: ChatService
) {}
```

---

## 5. Functional Requirements

### FR-1: Message Exchange
**Priority:** P0 (Critical)  
**Implementation:** AppComponent + ChatService + OllamaService

**Acceptance Criteria:**
- User can type messages in textarea
- Enter sends message (Shift+Enter for newline)
- Messages display immediately
- AI responses stream to chat
- Error messages display on failure

**Technical Details:**
```typescript
sendMessage(): void {
  // 1. Validate input
  // 2. Create user message
  // 3. Add to chat
  // 4. Call Ollama API
  // 5. Handle response/error
}
```

### FR-2: Model Selection
**Priority:** P0 (Critical)  
**Implementation:** AppComponent + OllamaService

**Acceptance Criteria:**
- Model input in sidebar
- Changes persist for session
- Invalid models show errors
- Default to 'gemma3:1b'

**Technical Details:**
```typescript
onModelChange(): void {
  this.ollamaService.setModel(this.currentModel);
}
```

### FR-3: Connection Management
**Priority:** P1 (High)  
**Implementation:** OllamaService

**Acceptance Criteria:**
- Auto-check on startup
- Visual status indicator
- Click to refresh
- Color-coded states

**Technical Details:**
```typescript
checkConnection(): void {
  this.http.get(`${url}/api/tags`)
    .pipe(catchError(() => of(null)))
    .subscribe(/* update status */);
}
```

### FR-4: Chat History
**Priority:** P1 (High)  
**Implementation:** ChatService

**Acceptance Criteria:**
- All messages visible
- Timestamps displayed
- Auto-scroll to bottom
- Clear distinction between senders

### FR-5: Clear Chat
**Priority:** P2 (Medium)  
**Implementation:** AppComponent + ChatService

**Acceptance Criteria:**
- Button in sidebar
- Confirmation dialog
- Clears all messages
- Shows welcome message after clear

---

## 6. Non-Functional Requirements

### 6.1 Performance (NFR-P)

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-P1 | Initial Load Time | <2s | Time to Interactive |
| NFR-P2 | First Contentful Paint | <1.5s | Lighthouse |
| NFR-P3 | Bundle Size | <500KB | Gzipped |
| NFR-P4 | Runtime Performance | 60 FPS | Chrome DevTools |
| NFR-P5 | Memory Usage | <150MB | Chrome Task Manager |

### 6.2 Code Quality (NFR-Q)

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-Q1 | Type Coverage | 100% |
| NFR-Q2 | Linting | 0 errors |
| NFR-Q3 | Code Duplication | <5% |
| NFR-Q4 | Cyclomatic Complexity | <10 per function |

### 6.3 Scalability (NFR-S)

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NFR-S1 | Component Modularity | Single responsibility |
| NFR-S2 | Service Reusability | Dependency injection |
| NFR-S3 | State Management | Observable patterns |

### 6.4 Maintainability (NFR-M)

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NFR-M1 | Code Style | Angular style guide |
| NFR-M2 | Documentation | TSDoc comments |
| NFR-M3 | Folder Structure | Feature-based |

---

## 7. System Requirements

### 7.1 Development Requirements

**Software:**
- Node.js: >=18.0.0
- npm: >=9.0.0
- Angular CLI: >=17.0.0
- TypeScript: >=5.2.0

**Hardware:**
- CPU: 2+ cores
- RAM: 8GB minimum
- Storage: 2GB free space

### 7.2 Production Requirements

**Browser Support:**
- Chrome: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Edge: Latest 2 versions

**Runtime:**
- Modern browser with ES2022 support
- JavaScript enabled
- LocalStorage available

### 7.3 External Dependencies

| Dependency | Version | Purpose | License |
|-----------|---------|---------|---------|
| Angular Core | ^17.0.0 | Framework | MIT |
| RxJS | ~7.8.0 | Reactive programming | Apache 2.0 |
| TypeScript | ~5.2.2 | Type system | Apache 2.0 |
| Zone.js | ~0.14.2 | Change detection | MIT |
| Ollama | Latest | AI Inference | MIT |

---

## 8. API Specifications

### 8.1 Ollama REST API

#### Check Server
```typescript
GET http://localhost:11434/api/tags

Response: {
  models: Array<{
    name: string;
    modified_at: string;
    size: number;
  }>
}
```

#### Generate Response
```typescript
POST http://localhost:11434/api/generate
Content-Type: application/json

Request: OllamaGenerateRequest {
  model: string;
  prompt: string;
  stream: boolean;
}

Response: OllamaResponse {
  model: string;
  created_at: string;
  response: string;
  done: boolean;
  context?: number[];
  total_duration?: number;
}
```

### 8.2 Service Interface Contracts

#### OllamaService

```typescript
interface OllamaService {
  // Observables
  connectionStatus$: Observable<ConnectionStatus>;
  
  // Methods
  checkConnection(): void;
  generateResponse(prompt: string, model?: string): Observable<string>;
  getCurrentModel(): string;
  setModel(model: string): void;
  getUrl(): string;
  setUrl(url: string): void;
}
```

#### ChatService

```typescript
interface ChatService {
  // Observables
  messages$: Observable<Message[]>;
  isProcessing$: Observable<boolean>;
  
  // Methods
  addMessage(message: Message): void;
  createUserMessage(content: string): Message;
  createAIMessage(content: string): Message;
  createErrorMessage(content: string): Message;
  clearMessages(): void;
  setProcessing(isProcessing: boolean): void;
  getMessages(): Message[];
}
```

---

## 9. Component Specifications

### 9.1 AppComponent

**File:** `src/app/app.component.ts`

**Class Definition:**
```typescript
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  // Properties
  title: string;
  messages: Message[];
  currentModel: string;
  connectionStatus: ConnectionStatus;
  isProcessing: boolean;
  userInput: string;
  
  // Lifecycle
  ngOnInit(): void;
  ngOnDestroy(): void;
  
  // Methods
  sendMessage(): void;
  onKeyPress(event: KeyboardEvent): void;
  clearChat(): void;
  onModelChange(): void;
  refreshConnection(): void;
  getStatusClass(): string;
  getStatusText(): string;
}
```

**Template Structure:**
```html
<div class="app-container">
  <div class="sidebar">
    <!-- Sidebar controls -->
  </div>
  <div class="main-content">
    <div class="chat-header">...</div>
    <div class="chat-messages">
      <div *ngFor="let message of messages">...</div>
    </div>
    <div class="input-container">...</div>
  </div>
</div>
```

**Styling:** Dark theme with Catppuccin Mocha palette

---

## 10. Service Layer

### 10.1 OllamaService Implementation

**Responsibility:** HTTP communication and API abstraction

**Key Features:**
- Connection status monitoring
- HTTP error handling
- Request/response transformation
- Configuration management

**RxJS Operators Used:**
- `map`: Transform responses
- `catchError`: Handle errors
- `tap`: Side effects
- `of`: Create observables

**Error Handling:**
```typescript
private handleError(error: HttpErrorResponse): Observable<never> {
  let errorMessage = 'An error occurred';
  
  if (error.status === 0) {
    errorMessage = 'Cannot connect to Ollama...';
  } else if (error.status === 404) {
    errorMessage = 'Model not found...';
  } else if (error.status === 500) {
    errorMessage = 'Server error...';
  }
  
  return throwError(() => new Error(errorMessage));
}
```

### 10.2 ChatService Implementation

**Responsibility:** Message state management

**Key Features:**
- Reactive message list
- Processing state
- Message creation helpers
- Unique ID generation

**State Management Pattern:**
```typescript
private messagesSubject = new BehaviorSubject<Message[]>([]);
public messages$ = this.messagesSubject.asObservable();

addMessage(message: Message): void {
  const currentMessages = this.messagesSubject.value;
  this.messagesSubject.next([...currentMessages, message]);
}
```

---

## 11. Data Models

### 11.1 TypeScript Interfaces

**File:** `src/app/models/chat.model.ts`

```typescript
export interface Message {
  id: string;                    // Unique identifier
  sender: 'user' | 'ai' | 'system';  // Message sender
  content: string;               // Message text
  timestamp: Date;               // Creation time
  type: 'user' | 'ai' | 'error'; // Display type
}

export interface OllamaConfig {
  url: string;      // Ollama server URL
  model: string;    // Current model name
  timeout: number;  // Request timeout (ms)
}

export interface OllamaResponse {
  model: string;
  created_at: string;
  response: string;
  done: boolean;
  context?: number[];
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  eval_count?: number;
}

export interface OllamaGenerateRequest {
  model: string;
  prompt: string;
  stream: boolean;
}

export enum ConnectionStatus {
  CONNECTED = 'connected',
  CONNECTING = 'connecting',
  DISCONNECTED = 'disconnected'
}
```

### 11.2 Type Guards

```typescript
function isMessage(obj: any): obj is Message {
  return 'id' in obj 
    && 'sender' in obj 
    && 'content' in obj 
    && 'timestamp' in obj;
}
```

---

## 12. State Management

### 12.1 Reactive State Pattern

**Architecture:**
- BehaviorSubjects hold current state
- Observables expose state streams
- Components subscribe via async pipe
- Services update state immutably

**Example:**
```typescript
// Service
private stateSubject = new BehaviorSubject<State>(initialState);
public state$ = this.stateSubject.asObservable();

updateState(newState: State): void {
  this.stateSubject.next(newState);
}

// Component
state$: Observable<State>;

ngOnInit(): void {
  this.state$ = this.service.state$;
}

// Template
<div>{{ (state$ | async)?.property }}</div>
```

### 12.2 Subscription Management

**Pattern:** takeUntil with destroy subject

```typescript
private destroy$ = new Subject<void>();

ngOnInit(): void {
  this.service.data$
    .pipe(takeUntil(this.destroy$))
    .subscribe(data => {
      // Handle data
    });
}

ngOnDestroy(): void {
  this.destroy$.next();
  this.destroy$.complete();
}
```

### 12.3 State Flow Diagram

```
User Action
    ↓
Component Method
    ↓
Service Method
    ↓
Update BehaviorSubject
    ↓
Observable emits new value
    ↓
Async pipe receives update
    ↓
View re-renders
```

---

## 13. Error Handling

### 13.1 HTTP Error Handling

**Strategy:** Centralized error handler in service

```typescript
generateResponse(prompt: string): Observable<string> {
  return this.http.post<OllamaResponse>(url, request)
    .pipe(
      map(response => response.response),
      catchError(this.handleError)
    );
}

private handleError(error: HttpErrorResponse): Observable<never> {
  // Transform error to user-friendly message
  return throwError(() => new Error(userMessage));
}
```

### 13.2 Error Categories

| Category | HTTP Status | User Message |
|----------|------------|--------------|
| Network | 0 | "Cannot connect to Ollama..." |
| Not Found | 404 | "Model not found..." |
| Server Error | 500 | "Server error..." |
| Timeout | - | "Request timed out..." |
| Client Error | 400-499 | "Invalid request..." |

### 13.3 Error Display

```typescript
// Component
.subscribe({
  next: (response) => { /* handle success */ },
  error: (error) => {
    const errorMessage = this.chatService.createErrorMessage(
      error.message
    );
    this.chatService.addMessage(errorMessage);
  }
});
```

---

## 14. Security & Privacy

### 14.1 Data Privacy

| Aspect | Implementation |
|--------|---------------|
| Data Storage | No persistent storage |
| Network | Local-only (localhost) |
| Telemetry | None |
| Analytics | None |
| Cookies | None |

### 14.2 TypeScript Security

```typescript
// Strict type checking
"strict": true,
"noImplicitAny": true,
"strictNullChecks": true,

// Prevent common errors
"noUnusedLocals": true,
"noUnusedParameters": true,
"noImplicitReturns": true,
```

### 14.3 Content Security

```typescript
// HTML sanitization (Angular built-in)
// XSS protection via template syntax
// No eval() or dynamic code execution
// Input validation and sanitization
```

---

## 15. Performance Requirements

### 15.1 Bundle Optimization

**Strategies:**
- Tree shaking (unused code removal)
- Lazy loading modules (future)
- AOT compilation
- Production optimizations

**Build Configuration:**
```json
"configurations": {
  "production": {
    "optimization": true,
    "outputHashing": "all",
    "sourceMap": false,
    "namedChunks": false,
    "extractLicenses": true,
    "vendorChunk": false,
    "buildOptimizer": true
  }
}
```

### 15.2 Runtime Performance

**Optimizations:**
- OnPush change detection (future)
- TrackBy for ngFor
- Async pipe for subscriptions
- Unsubscribe on destroy
- Debounce user input (future)

### 15.3 Performance Metrics

| Metric | Target | Tool |
|--------|--------|------|
| FCP | <1.5s | Lighthouse |
| LCP | <2.5s | Lighthouse |
| TTI | <3s | Lighthouse |
| TBT | <200ms | Lighthouse |
| CLS | <0.1 | Lighthouse |

---

## 16. Testing Strategy

### 16.1 Unit Testing

**Framework:** Jasmine + Karma

**Coverage Target:** 80%

**Test Structure:**
```typescript
describe('OllamaService', () => {
  let service: OllamaService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OllamaService]
    });
    service = TestBed.inject(OllamaService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should generate response', () => {
    // Test implementation
  });
});
```

### 16.2 Component Testing

```typescript
describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      imports: [HttpClientTestingModule, FormsModule],
      providers: [OllamaService, ChatService]
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
```

### 16.3 E2E Testing (Future)

**Framework:** Cypress or Playwright

**Scenarios:**
- Complete message flow
- Error handling
- Model switching
- Chat clearing

---

## 17. Build & Deployment

### 17.1 Development Build

```bash
ng serve
# or
npm start
```

**Features:**
- Hot module replacement
- Source maps
- No optimization
- Fast rebuild

### 17.2 Production Build

```bash
ng build --configuration production
```

**Optimizations:**
- AOT compilation
- Tree shaking
- Minification
- Bundling
- Hash-based cache busting

**Output:**
```
dist/ollama-chatbot-angular/
├── index.html
├── main.[hash].js
├── polyfills.[hash].js
├── runtime.[hash].js
└── styles.[hash].css
```

### 17.3 Deployment Options

#### Static Hosting
```bash
# Build
ng build --configuration production

# Deploy to any static host
# - Netlify
# - Vercel
# - GitHub Pages
# - AWS S3
```

#### Docker
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist/ollama-chatbot-angular /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 17.4 Environment Configuration

```typescript
// src/environments/environment.ts (dev)
export const environment = {
  production: false,
  ollamaUrl: 'http://localhost:11434'
};

// src/environments/environment.prod.ts (prod)
export const environment = {
  production: true,
  ollamaUrl: 'http://localhost:11434'
};
```

---

## 18. Future Enhancements

### 18.1 Phase 2 (Q1 2026)

| Feature | Priority | Complexity |
|---------|----------|------------|
| Conversation persistence (LocalStorage) | High | Medium |
| Multiple chat sessions | High | High |
| Export chat history | Medium | Low |
| Code syntax highlighting | Medium | Medium |
| Custom themes | Low | Medium |

### 18.2 Phase 3 (Q2 2026)

| Feature | Priority | Complexity |
|---------|----------|------------|
| Streaming responses | High | High |
| File upload support | Medium | Medium |
| Voice input/output | Low | Very High |
| Plugin system | Low | Very High |

### 18.3 Technical Improvements

- Migrate to standalone components (Angular 17+)
- Implement OnPush change detection
- Add comprehensive E2E tests
- Implement state management library (NgRx/Akita)
- Add i18n support
- Implement PWA features

---

## Appendices

### Appendix A: File Structure

```
src/
├── app/
│   ├── components/           # Future components
│   ├── services/
│   │   ├── ollama.service.ts
│   │   └── chat.service.ts
│   ├── models/
│   │   └── chat.model.ts
│   ├── app.component.ts
│   ├── app.component.html
│   ├── app.component.css
│   └── app.module.ts
├── assets/                   # Static assets
├── environments/
│   ├── environment.ts
│   └── environment.prod.ts
├── index.html
├── main.ts
└── styles.css
```

### Appendix B: Angular Best Practices

1. **Single Responsibility:** One component/service per file
2. **Dependency Injection:** Use DI for all dependencies
3. **Observables:** Prefer observables over promises
4. **Unsubscribe:** Always clean up subscriptions
5. **Type Safety:** Leverage TypeScript fully
6. **OnPush:** Use OnPush change detection when possible
7. **TrackBy:** Always use trackBy with ngFor
8. **Async Pipe:** Prefer async pipe over manual subscription

### Appendix C: RxJS Patterns

**Common Operators:**
- `map`: Transform data
- `filter`: Filter emissions
- `catchError`: Error handling
- `tap`: Side effects
- `switchMap`: Switch to new observable
- `takeUntil`: Unsubscribe on event
- `debounceTime`: Delay emissions
- `distinctUntilChanged`: Skip duplicates

### Appendix D: TypeScript Configuration

**Key Compiler Options:**
```json
{
  "strict": true,
  "noImplicitAny": true,
  "strictNullChecks": true,
  "strictFunctionTypes": true,
  "strictBindCallApply": true,
  "strictPropertyInitialization": true,
  "noImplicitThis": true,
  "alwaysStrict": true
}
```

---

**Document Approval:**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Manager | [Name] | [Date] | _________ |
| Tech Lead (Angular) | [Name] | [Date] | _________ |
| Engineering | [Name] | [Date] | _________ |
| QA Lead | [Name] | [Date] | _________ |

---

**End of Document**
