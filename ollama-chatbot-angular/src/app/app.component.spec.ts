import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { FormsModule } from '@angular/forms';
import { of, throwError, BehaviorSubject } from 'rxjs';

import { AppComponent } from './app.component';
import { OllamaService } from './services/ollama.service';
import { ChatService } from './services/chat.service';
import { ConnectionStatus, Message } from './models/chat.model';

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let ollamaService: jasmine.SpyObj<OllamaService>;
  let chatService: jasmine.SpyObj<ChatService>;
  let messagesSubject: BehaviorSubject<Message[]>;
  let isProcessingSubject: BehaviorSubject<boolean>;
  let connectionStatusSubject: BehaviorSubject<ConnectionStatus>;

  beforeEach(async () => {
    // Create mock observables
    messagesSubject = new BehaviorSubject<Message[]>([]);
    isProcessingSubject = new BehaviorSubject<boolean>(false);
    connectionStatusSubject = new BehaviorSubject<ConnectionStatus>(ConnectionStatus.CONNECTING);

    // Create spy objects
    const ollamaSpy = jasmine.createSpyObj('OllamaService', [
      'generateResponse',
      'getCurrentModel',
      'setModel',
      'checkConnection'
    ], {
      connectionStatus$: connectionStatusSubject.asObservable()
    });

    const chatSpy = jasmine.createSpyObj('ChatService', [
      'addMessage',
      'createUserMessage',
      'createAIMessage',
      'createErrorMessage',
      'clearMessages',
      'setProcessing'
    ], {
      messages$: messagesSubject.asObservable(),
      isProcessing$: isProcessingSubject.asObservable()
    });

    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      imports: [HttpClientTestingModule, FormsModule],
      providers: [
        { provide: OllamaService, useValue: ollamaSpy },
        { provide: ChatService, useValue: chatSpy }
      ]
    }).compileComponents();

    ollamaService = TestBed.inject(OllamaService) as jasmine.SpyObj<OllamaService>;
    chatService = TestBed.inject(ChatService) as jasmine.SpyObj<ChatService>;

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Initialization', () => {
    it('should set title on creation', () => {
      expect(component.title).toBe('Ollama AI Assistant');
    });

    it('should initialize with default model', () => {
      ollamaService.getCurrentModel.and.returnValue('gemma3:1b');
      fixture.detectChanges();
      expect(component.currentModel).toBe('gemma3:1b');
    });

    it('should subscribe to messages on init', () => {
      const mockMessages: Message[] = [
        {
          id: '1',
          sender: 'ai',
          content: 'Hello',
          timestamp: new Date(),
          type: 'ai'
        }
      ];

      messagesSubject.next(mockMessages);
      fixture.detectChanges();

      expect(component.messages).toEqual(mockMessages);
    });

    it('should subscribe to processing state on init', () => {
      isProcessingSubject.next(true);
      fixture.detectChanges();

      expect(component.isProcessing).toBe(true);
    });

    it('should subscribe to connection status on init', () => {
      connectionStatusSubject.next(ConnectionStatus.CONNECTED);
      fixture.detectChanges();

      expect(component.connectionStatus).toBe(ConnectionStatus.CONNECTED);
    });
  });

  describe('sendMessage', () => {
    beforeEach(() => {
      ollamaService.getCurrentModel.and.returnValue('gemma3:1b');
      fixture.detectChanges();
    });

    it('should not send empty message', () => {
      component.userInput = '';
      component.sendMessage();

      expect(chatService.addMessage).not.toHaveBeenCalled();
    });

    it('should not send whitespace-only message', () => {
      component.userInput = '   ';
      component.sendMessage();

      expect(chatService.addMessage).not.toHaveBeenCalled();
    });

    it('should not send message when processing', () => {
      component.userInput = 'Test message';
      component.isProcessing = true;
      component.sendMessage();

      expect(chatService.addMessage).not.toHaveBeenCalled();
    });

    it('should create and add user message', () => {
      const mockUserMessage: Message = {
        id: '1',
        sender: 'user',
        content: 'Test message',
        timestamp: new Date(),
        type: 'user'
      };

      component.userInput = 'Test message';
      chatService.createUserMessage.and.returnValue(mockUserMessage);
      ollamaService.generateResponse.and.returnValue(of('AI response'));

      component.sendMessage();

      expect(chatService.createUserMessage).toHaveBeenCalledWith('Test message');
      expect(chatService.addMessage).toHaveBeenCalledWith(mockUserMessage);
    });

    it('should clear input after sending', () => {
      component.userInput = 'Test message';
      chatService.createUserMessage.and.returnValue({
        id: '1',
        sender: 'user',
        content: 'Test',
        timestamp: new Date(),
        type: 'user'
      });
      ollamaService.generateResponse.and.returnValue(of('AI response'));

      component.sendMessage();

      expect(component.userInput).toBe('');
    });

    it('should set processing to true', () => {
      component.userInput = 'Test message';
      chatService.createUserMessage.and.returnValue({
        id: '1',
        sender: 'user',
        content: 'Test',
        timestamp: new Date(),
        type: 'user'
      });
      ollamaService.generateResponse.and.returnValue(of('AI response'));

      component.sendMessage();

      expect(chatService.setProcessing).toHaveBeenCalledWith(true);
    });

    it('should call ollama service with prompt', () => {
      const userInput = 'Test message';
      component.userInput = userInput;
      component.currentModel = 'mistral';
      
      chatService.createUserMessage.and.returnValue({
        id: '1',
        sender: 'user',
        content: userInput,
        timestamp: new Date(),
        type: 'user'
      });
      ollamaService.generateResponse.and.returnValue(of('AI response'));

      component.sendMessage();

      expect(ollamaService.generateResponse).toHaveBeenCalledWith(userInput, 'mistral');
    });

    it('should add AI response on success', (done) => {
      const aiResponse = 'This is the AI response';
      const mockAIMessage: Message = {
        id: '2',
        sender: 'ai',
        content: aiResponse,
        timestamp: new Date(),
        type: 'ai'
      };

      component.userInput = 'Test';
      chatService.createUserMessage.and.returnValue({
        id: '1',
        sender: 'user',
        content: 'Test',
        timestamp: new Date(),
        type: 'user'
      });
      chatService.createAIMessage.and.returnValue(mockAIMessage);
      ollamaService.generateResponse.and.returnValue(of(aiResponse));

      component.sendMessage();

      setTimeout(() => {
        expect(chatService.createAIMessage).toHaveBeenCalledWith(aiResponse);
        expect(chatService.addMessage).toHaveBeenCalledWith(mockAIMessage);
        done();
      }, 100);
    });

    it('should set processing to false after success', (done) => {
      component.userInput = 'Test';
      chatService.createUserMessage.and.returnValue({
        id: '1',
        sender: 'user',
        content: 'Test',
        timestamp: new Date(),
        type: 'user'
      });
      ollamaService.generateResponse.and.returnValue(of('AI response'));

      component.sendMessage();

      setTimeout(() => {
        expect(chatService.setProcessing).toHaveBeenCalledWith(false);
        done();
      }, 100);
    });

    it('should handle errors gracefully', (done) => {
      const errorMessage = 'Connection failed';
      const mockErrorMessage: Message = {
        id: '2',
        sender: 'system',
        content: errorMessage,
        timestamp: new Date(),
        type: 'error'
      };

      component.userInput = 'Test';
      chatService.createUserMessage.and.returnValue({
        id: '1',
        sender: 'user',
        content: 'Test',
        timestamp: new Date(),
        type: 'user'
      });
      chatService.createErrorMessage.and.returnValue(mockErrorMessage);
      ollamaService.generateResponse.and.returnValue(
        throwError(() => new Error(errorMessage))
      );

      component.sendMessage();

      setTimeout(() => {
        expect(chatService.createErrorMessage).toHaveBeenCalledWith(errorMessage);
        expect(chatService.addMessage).toHaveBeenCalledWith(mockErrorMessage);
        expect(chatService.setProcessing).toHaveBeenCalledWith(false);
        done();
      }, 100);
    });
  });

  describe('onKeyPress', () => {
    beforeEach(() => {
      fixture.detectChanges();
      spyOn(component, 'sendMessage');
    });

    it('should send message on Enter key', () => {
      const event = new KeyboardEvent('keydown', { key: 'Enter' });
      spyOn(event, 'preventDefault');

      component.onKeyPress(event);

      expect(event.preventDefault).toHaveBeenCalled();
      expect(component.sendMessage).toHaveBeenCalled();
    });

    it('should not send message on Shift+Enter', () => {
      const event = new KeyboardEvent('keydown', { 
        key: 'Enter', 
        shiftKey: true 
      });

      component.onKeyPress(event);

      expect(component.sendMessage).not.toHaveBeenCalled();
    });

    it('should not send message on other keys', () => {
      const event = new KeyboardEvent('keydown', { key: 'a' });

      component.onKeyPress(event);

      expect(component.sendMessage).not.toHaveBeenCalled();
    });
  });

  describe('clearChat', () => {
    beforeEach(() => {
      fixture.detectChanges();
    });

    it('should call chatService.clearMessages on confirmation', () => {
      spyOn(window, 'confirm').and.returnValue(true);

      component.clearChat();

      expect(chatService.clearMessages).toHaveBeenCalled();
    });

    it('should not clear messages on cancel', () => {
      spyOn(window, 'confirm').and.returnValue(false);

      component.clearChat();

      expect(chatService.clearMessages).not.toHaveBeenCalled();
    });
  });

  describe('onModelChange', () => {
    beforeEach(() => {
      fixture.detectChanges();
    });

    it('should update model in ollama service', () => {
      component.currentModel = 'mistral';
      component.onModelChange();

      expect(ollamaService.setModel).toHaveBeenCalledWith('mistral');
    });

    it('should handle different model names', () => {
      const models = ['gemma3:1b', 'mistral', 'codellama', 'phi'];

      models.forEach(model => {
        component.currentModel = model;
        component.onModelChange();
        expect(ollamaService.setModel).toHaveBeenCalledWith(model);
      });
    });
  });

  describe('refreshConnection', () => {
    beforeEach(() => {
      fixture.detectChanges();
    });

    it('should call checkConnection on ollama service', () => {
      component.refreshConnection();

      expect(ollamaService.checkConnection).toHaveBeenCalled();
    });
  });

  describe('getStatusClass', () => {
    beforeEach(() => {
      fixture.detectChanges();
    });

    it('should return correct class for CONNECTED status', () => {
      component.connectionStatus = ConnectionStatus.CONNECTED;
      expect(component.getStatusClass()).toBe('status-connected');
    });

    it('should return correct class for CONNECTING status', () => {
      component.connectionStatus = ConnectionStatus.CONNECTING;
      expect(component.getStatusClass()).toBe('status-connecting');
    });

    it('should return correct class for DISCONNECTED status', () => {
      component.connectionStatus = ConnectionStatus.DISCONNECTED;
      expect(component.getStatusClass()).toBe('status-disconnected');
    });
  });

  describe('getStatusText', () => {
    beforeEach(() => {
      fixture.detectChanges();
    });

    it('should return correct text for CONNECTED status', () => {
      component.connectionStatus = ConnectionStatus.CONNECTED;
      expect(component.getStatusText()).toBe('Connected');
    });

    it('should return correct text for CONNECTING status', () => {
      component.connectionStatus = ConnectionStatus.CONNECTING;
      expect(component.getStatusText()).toBe('Connecting...');
    });

    it('should return correct text for DISCONNECTED status', () => {
      component.connectionStatus = ConnectionStatus.DISCONNECTED;
      expect(component.getStatusText()).toBe('Disconnected');
    });
  });

  describe('Component Cleanup', () => {
    it('should unsubscribe on destroy', () => {
      fixture.detectChanges();
      const destroySpy = spyOn((component as any).destroy$, 'next');
      const completeSpy = spyOn((component as any).destroy$, 'complete');

      component.ngOnDestroy();

      expect(destroySpy).toHaveBeenCalled();
      expect(completeSpy).toHaveBeenCalled();
    });
  });

  describe('Template Integration', () => {
    beforeEach(() => {
      ollamaService.getCurrentModel.and.returnValue('gemma3:1b');
      fixture.detectChanges();
    });

    it('should render app container', () => {
      const compiled = fixture.nativeElement;
      expect(compiled.querySelector('.app-container')).toBeTruthy();
    });

    it('should render sidebar', () => {
      const compiled = fixture.nativeElement;
      expect(compiled.querySelector('.sidebar')).toBeTruthy();
    });

    it('should render main content', () => {
      const compiled = fixture.nativeElement;
      expect(compiled.querySelector('.main-content')).toBeTruthy();
    });

    it('should bind userInput to textarea', () => {
      component.userInput = 'Test input';
      fixture.detectChanges();

      const textarea = fixture.nativeElement.querySelector('.message-input');
      expect(textarea.value).toBe('Test input');
    });

    it('should render messages', () => {
      const mockMessages: Message[] = [
        {
          id: '1',
          sender: 'ai',
          content: 'Hello!',
          timestamp: new Date(),
          type: 'ai'
        },
        {
          id: '2',
          sender: 'user',
          content: 'Hi there',
          timestamp: new Date(),
          type: 'user'
        }
      ];

      messagesSubject.next(mockMessages);
      fixture.detectChanges();

      const messages = fixture.nativeElement.querySelectorAll('.message');
      expect(messages.length).toBe(2);
    });
  });
});
