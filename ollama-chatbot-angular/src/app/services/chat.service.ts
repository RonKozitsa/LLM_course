import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Message } from '../models/chat.model';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private messagesSubject = new BehaviorSubject<Message[]>([]);
  public messages$ = this.messagesSubject.asObservable();

  private isProcessingSubject = new BehaviorSubject<boolean>(false);
  public isProcessing$ = this.isProcessingSubject.asObservable();

  constructor() {
    this.addWelcomeMessage();
  }

  /**
   * Add welcome message
   */
  private addWelcomeMessage(): void {
    const welcomeMessage: Message = {
      id: this.generateId(),
      sender: 'ai',
      content: "Hello! I'm your local AI assistant powered by Ollama. How can I help you today?",
      timestamp: new Date(),
      type: 'ai'
    };
    this.addMessage(welcomeMessage);
  }

  /**
   * Add a message to the chat
   */
  addMessage(message: Message): void {
    const currentMessages = this.messagesSubject.value;
    this.messagesSubject.next([...currentMessages, message]);
  }

  /**
   * Create a user message
   */
  createUserMessage(content: string): Message {
    return {
      id: this.generateId(),
      sender: 'user',
      content: content,
      timestamp: new Date(),
      type: 'user'
    };
  }

  /**
   * Create an AI message
   */
  createAIMessage(content: string): Message {
    return {
      id: this.generateId(),
      sender: 'ai',
      content: content,
      timestamp: new Date(),
      type: 'ai'
    };
  }

  /**
   * Create an error message
   */
  createErrorMessage(content: string): Message {
    return {
      id: this.generateId(),
      sender: 'system',
      content: content,
      timestamp: new Date(),
      type: 'error'
    };
  }

  /**
   * Clear all messages
   */
  clearMessages(): void {
    this.messagesSubject.next([]);
    this.addWelcomeMessage();
  }

  /**
   * Set processing state
   */
  setProcessing(isProcessing: boolean): void {
    this.isProcessingSubject.next(isProcessing);
  }

  /**
   * Get all messages
   */
  getMessages(): Message[] {
    return this.messagesSubject.value;
  }

  /**
   * Generate unique ID for messages
   */
  private generateId(): string {
    return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
