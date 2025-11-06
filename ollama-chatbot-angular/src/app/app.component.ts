import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subject, takeUntil } from 'rxjs';
import { OllamaService } from './services/ollama.service';
import { ChatService } from './services/chat.service';
import { Message, ConnectionStatus } from './models/chat.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'Ollama AI Assistant';
  messages: Message[] = [];
  currentModel: string = 'gemma3:1b';
  connectionStatus: ConnectionStatus = ConnectionStatus.CONNECTING;
  isProcessing: boolean = false;
  userInput: string = '';

  ConnectionStatus = ConnectionStatus; // Expose enum to template

  private destroy$ = new Subject<void>();

  constructor(
    private ollamaService: OllamaService,
    private chatService: ChatService
  ) {}

  ngOnInit(): void {
    // Subscribe to messages
    this.chatService.messages$
      .pipe(takeUntil(this.destroy$))
      .subscribe(messages => {
        this.messages = messages;
        setTimeout(() => this.scrollToBottom(), 100);
      });

    // Subscribe to processing state
    this.chatService.isProcessing$
      .pipe(takeUntil(this.destroy$))
      .subscribe(isProcessing => {
        this.isProcessing = isProcessing;
      });

    // Subscribe to connection status
    this.ollamaService.connectionStatus$
      .pipe(takeUntil(this.destroy$))
      .subscribe(status => {
        this.connectionStatus = status;
      });

    // Set initial model
    this.currentModel = this.ollamaService.getCurrentModel();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  /**
   * Send message to AI
   */
  sendMessage(): void {
    const trimmedInput = this.userInput.trim();
    
    if (!trimmedInput || this.isProcessing) {
      return;
    }

    // Add user message
    const userMessage = this.chatService.createUserMessage(trimmedInput);
    this.chatService.addMessage(userMessage);

    // Clear input
    this.userInput = '';

    // Set processing state
    this.chatService.setProcessing(true);

    // Get AI response
    this.ollamaService.generateResponse(trimmedInput, this.currentModel)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (response) => {
          const aiMessage = this.chatService.createAIMessage(response);
          this.chatService.addMessage(aiMessage);
          this.chatService.setProcessing(false);
        },
        error: (error) => {
          const errorMessage = this.chatService.createErrorMessage(
            error.message || 'An error occurred while processing your request.'
          );
          this.chatService.addMessage(errorMessage);
          this.chatService.setProcessing(false);
        }
      });
  }

  /**
   * Handle Enter key press
   */
  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  /**
   * Clear chat history
   */
  clearChat(): void {
    if (confirm('Are you sure you want to clear the chat history?')) {
      this.chatService.clearMessages();
    }
  }

  /**
   * Update model
   */
  onModelChange(): void {
    this.ollamaService.setModel(this.currentModel);
  }

  /**
   * Refresh connection
   */
  refreshConnection(): void {
    this.ollamaService.checkConnection();
  }

  /**
   * Scroll chat to bottom
   */
  private scrollToBottom(): void {
    const chatArea = document.querySelector('.chat-messages');
    if (chatArea) {
      chatArea.scrollTop = chatArea.scrollHeight;
    }
  }

  /**
   * Get status indicator class
   */
  getStatusClass(): string {
    switch (this.connectionStatus) {
      case ConnectionStatus.CONNECTED:
        return 'status-connected';
      case ConnectionStatus.CONNECTING:
        return 'status-connecting';
      case ConnectionStatus.DISCONNECTED:
        return 'status-disconnected';
      default:
        return '';
    }
  }

  /**
   * Get status text
   */
  getStatusText(): string {
    switch (this.connectionStatus) {
      case ConnectionStatus.CONNECTED:
        return 'Connected';
      case ConnectionStatus.CONNECTING:
        return 'Connecting...';
      case ConnectionStatus.DISCONNECTED:
        return 'Disconnected';
      default:
        return '';
    }
  }
}
