import { TestBed } from '@angular/core/testing';
import { ChatService } from './chat.service';
import { Message } from '../models/chat.model';

describe('ChatService', () => {
  let service: ChatService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ChatService]
    });
    service = TestBed.inject(ChatService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('Initial State', () => {
    it('should start with welcome message', (done) => {
      service.messages$.subscribe(messages => {
        expect(messages.length).toBe(1);
        expect(messages[0].sender).toBe('ai');
        expect(messages[0].content).toContain('Hello');
        done();
      });
    });

    it('should start with processing false', (done) => {
      service.isProcessing$.subscribe(isProcessing => {
        expect(isProcessing).toBe(false);
        done();
      });
    });
  });

  describe('Message Creation', () => {
    it('should create user message with correct properties', () => {
      const content = 'Test user message';
      const message = service.createUserMessage(content);

      expect(message.id).toBeTruthy();
      expect(message.sender).toBe('user');
      expect(message.content).toBe(content);
      expect(message.type).toBe('user');
      expect(message.timestamp).toBeInstanceOf(Date);
    });

    it('should create AI message with correct properties', () => {
      const content = 'Test AI message';
      const message = service.createAIMessage(content);

      expect(message.id).toBeTruthy();
      expect(message.sender).toBe('ai');
      expect(message.content).toBe(content);
      expect(message.type).toBe('ai');
      expect(message.timestamp).toBeInstanceOf(Date);
    });

    it('should create error message with correct properties', () => {
      const content = 'Test error message';
      const message = service.createErrorMessage(content);

      expect(message.id).toBeTruthy();
      expect(message.sender).toBe('system');
      expect(message.content).toBe(content);
      expect(message.type).toBe('error');
      expect(message.timestamp).toBeInstanceOf(Date);
    });

    it('should create unique IDs for each message', () => {
      const msg1 = service.createUserMessage('Message 1');
      const msg2 = service.createUserMessage('Message 2');
      const msg3 = service.createAIMessage('Message 3');

      expect(msg1.id).not.toBe(msg2.id);
      expect(msg2.id).not.toBe(msg3.id);
      expect(msg1.id).not.toBe(msg3.id);
    });
  });

  describe('Message Management', () => {
    it('should add message to the list', (done) => {
      const newMessage = service.createUserMessage('New message');
      service.addMessage(newMessage);

      service.messages$.subscribe(messages => {
        const found = messages.find(m => m.id === newMessage.id);
        expect(found).toBeTruthy();
        expect(found?.content).toBe(newMessage.content);
        done();
      });
    });

    it('should maintain message order', (done) => {
      const msg1 = service.createUserMessage('First');
      const msg2 = service.createAIMessage('Second');
      const msg3 = service.createUserMessage('Third');

      service.addMessage(msg1);
      service.addMessage(msg2);
      service.addMessage(msg3);

      service.messages$.subscribe(messages => {
        // Skip welcome message (index 0)
        expect(messages[1].content).toBe('First');
        expect(messages[2].content).toBe('Second');
        expect(messages[3].content).toBe('Third');
        done();
      });
    });

    it('should preserve existing messages when adding new ones', (done) => {
      const initialCount = service.getMessages().length;
      const newMessage = service.createUserMessage('Test');
      
      service.addMessage(newMessage);

      service.messages$.subscribe(messages => {
        expect(messages.length).toBe(initialCount + 1);
        done();
      });
    });

    it('should return current messages array', () => {
      const messages = service.getMessages();
      expect(Array.isArray(messages)).toBe(true);
      expect(messages.length).toBeGreaterThan(0);
    });
  });

  describe('Clear Messages', () => {
    it('should clear all messages and add welcome message', (done) => {
      // Add some messages
      service.addMessage(service.createUserMessage('Test 1'));
      service.addMessage(service.createAIMessage('Test 2'));
      service.addMessage(service.createUserMessage('Test 3'));

      // Clear messages
      service.clearMessages();

      service.messages$.subscribe(messages => {
        expect(messages.length).toBe(1);
        expect(messages[0].sender).toBe('ai');
        expect(messages[0].content).toContain('Hello');
        done();
      });
    });

    it('should reset message count to 1 after clear', () => {
      service.addMessage(service.createUserMessage('Test 1'));
      service.addMessage(service.createUserMessage('Test 2'));
      
      service.clearMessages();
      
      const messages = service.getMessages();
      expect(messages.length).toBe(1);
    });
  });

  describe('Processing State', () => {
    it('should update processing state to true', (done) => {
      service.setProcessing(true);

      service.isProcessing$.subscribe(isProcessing => {
        expect(isProcessing).toBe(true);
        done();
      });
    });

    it('should update processing state to false', (done) => {
      service.setProcessing(true);
      service.setProcessing(false);

      service.isProcessing$.subscribe(isProcessing => {
        expect(isProcessing).toBe(false);
        done();
      });
    });

    it('should handle multiple state changes', (done) => {
      const states: boolean[] = [];

      service.isProcessing$.subscribe(isProcessing => {
        states.push(isProcessing);
        
        if (states.length === 4) {
          expect(states).toEqual([false, true, false, true]);
          done();
        }
      });

      service.setProcessing(true);
      service.setProcessing(false);
      service.setProcessing(true);
    });
  });

  describe('Observable Streams', () => {
    it('should emit messages on messages$ observable', (done) => {
      let emissionCount = 0;

      service.messages$.subscribe(messages => {
        emissionCount++;
        if (emissionCount === 2) {
          expect(messages.length).toBeGreaterThan(1);
          done();
        }
      });

      service.addMessage(service.createUserMessage('Test'));
    });

    it('should emit processing state on isProcessing$ observable', (done) => {
      let emissionCount = 0;

      service.isProcessing$.subscribe(isProcessing => {
        emissionCount++;
        if (emissionCount === 2) {
          expect(isProcessing).toBe(true);
          done();
        }
      });

      service.setProcessing(true);
    });
  });

  describe('Message ID Generation', () => {
    it('should generate valid ID format', () => {
      const message = service.createUserMessage('Test');
      expect(message.id).toMatch(/^msg_\d+_[a-z0-9]+$/);
    });

    it('should generate unique IDs rapidly', () => {
      const ids = new Set<string>();
      
      for (let i = 0; i < 100; i++) {
        const msg = service.createUserMessage(`Message ${i}`);
        ids.add(msg.id);
      }

      expect(ids.size).toBe(100);
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty message content', () => {
      const message = service.createUserMessage('');
      expect(message.content).toBe('');
      expect(message.id).toBeTruthy();
    });

    it('should handle very long message content', () => {
      const longContent = 'a'.repeat(10000);
      const message = service.createUserMessage(longContent);
      expect(message.content).toBe(longContent);
      expect(message.content.length).toBe(10000);
    });

    it('should handle special characters in content', () => {
      const specialContent = '<script>alert("test")</script>\n\t"quotes"';
      const message = service.createUserMessage(specialContent);
      expect(message.content).toBe(specialContent);
    });

    it('should handle rapid message additions', () => {
      const initialCount = service.getMessages().length;
      
      for (let i = 0; i < 50; i++) {
        service.addMessage(service.createUserMessage(`Message ${i}`));
      }

      const messages = service.getMessages();
      expect(messages.length).toBe(initialCount + 50);
    });
  });

  describe('Timestamp Accuracy', () => {
    it('should create messages with current timestamp', () => {
      const beforeTime = new Date();
      const message = service.createUserMessage('Test');
      const afterTime = new Date();

      expect(message.timestamp.getTime()).toBeGreaterThanOrEqual(beforeTime.getTime());
      expect(message.timestamp.getTime()).toBeLessThanOrEqual(afterTime.getTime());
    });

    it('should create messages with increasing timestamps', (done) => {
      const msg1 = service.createUserMessage('First');
      
      setTimeout(() => {
        const msg2 = service.createUserMessage('Second');
        expect(msg2.timestamp.getTime()).toBeGreaterThan(msg1.timestamp.getTime());
        done();
      }, 10);
    });
  });
});
