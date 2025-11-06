import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { OllamaService } from './ollama.service';
import { ConnectionStatus, OllamaResponse } from '../models/chat.model';

describe('OllamaService', () => {
  let service: OllamaService;
  let httpMock: HttpTestingController;
  const mockOllamaUrl = 'http://localhost:11434';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OllamaService]
    });
    service = TestBed.inject(OllamaService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('Connection Status', () => {
    it('should start with CONNECTING status', (done) => {
      service.connectionStatus$.subscribe(status => {
        expect(status).toBe(ConnectionStatus.CONNECTING);
        done();
      });
    });

    it('should update to CONNECTED when connection succeeds', (done) => {
      service.checkConnection();

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/tags`);
      expect(req.request.method).toBe('GET');
      
      req.flush({ models: [] }, { status: 200, statusText: 'OK' });

      setTimeout(() => {
        service.connectionStatus$.subscribe(status => {
          expect(status).toBe(ConnectionStatus.CONNECTED);
          done();
        });
      }, 100);
    });

    it('should update to DISCONNECTED when connection fails', (done) => {
      service.checkConnection();

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/tags`);
      req.error(new ErrorEvent('Network error'));

      setTimeout(() => {
        service.connectionStatus$.subscribe(status => {
          expect(status).toBe(ConnectionStatus.DISCONNECTED);
          done();
        });
      }, 100);
    });
  });

  describe('generateResponse', () => {
    it('should generate a response successfully', (done) => {
      const prompt = 'Hello, AI!';
      const mockResponse: OllamaResponse = {
        model: 'gemma3:1b',
        created_at: '2025-11-06T12:00:00Z',
        response: 'Hello! How can I help you?',
        done: true
      };

      service.generateResponse(prompt).subscribe(response => {
        expect(response).toBe(mockResponse.response);
        done();
      });

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      expect(req.request.method).toBe('POST');
      expect(req.request.body.prompt).toBe(prompt);
      expect(req.request.body.model).toBe('gemma3:1b');
      expect(req.request.body.stream).toBe(false);

      req.flush(mockResponse);
    });

    it('should use custom model when provided', (done) => {
      const prompt = 'Test prompt';
      const customModel = 'mistral';

      service.generateResponse(prompt, customModel).subscribe();

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      expect(req.request.body.model).toBe(customModel);
      
      req.flush({ response: 'test', done: true });
      done();
    });

    it('should handle connection errors', (done) => {
      const prompt = 'Test';

      service.generateResponse(prompt).subscribe({
        next: () => fail('should have errored'),
        error: (error) => {
          expect(error.message).toContain('Cannot connect to Ollama');
          done();
        }
      });

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      req.error(new ErrorEvent('Network error'), { status: 0 });
    });

    it('should handle 404 model not found error', (done) => {
      const prompt = 'Test';

      service.generateResponse(prompt).subscribe({
        next: () => fail('should have errored'),
        error: (error) => {
          expect(error.message).toContain('Model not found');
          done();
        }
      });

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      req.flush('Not found', { status: 404, statusText: 'Not Found' });
    });

    it('should handle 500 server error', (done) => {
      const prompt = 'Test';

      service.generateResponse(prompt).subscribe({
        next: () => fail('should have errored'),
        error: (error) => {
          expect(error.message).toContain('Server error');
          done();
        }
      });

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      req.flush('Server error', { status: 500, statusText: 'Internal Server Error' });
    });
  });

  describe('Model Management', () => {
    it('should return default model', () => {
      expect(service.getCurrentModel()).toBe('gemma3:1b');
    });

    it('should update current model', () => {
      const newModel = 'mistral';
      service.setModel(newModel);
      expect(service.getCurrentModel()).toBe(newModel);
    });

    it('should use updated model in requests', (done) => {
      const newModel = 'codellama';
      service.setModel(newModel);

      service.generateResponse('test').subscribe();

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      expect(req.request.body.model).toBe(newModel);
      
      req.flush({ response: 'test', done: true });
      done();
    });
  });

  describe('URL Management', () => {
    it('should return default URL', () => {
      expect(service.getUrl()).toBe(mockOllamaUrl);
    });

    it('should update URL and check connection', () => {
      const newUrl = 'http://localhost:8080';
      service.setUrl(newUrl);
      
      expect(service.getUrl()).toBe(newUrl);

      const req = httpMock.expectOne(`${newUrl}/api/tags`);
      req.flush({ models: [] });
    });
  });

  describe('Error Handling', () => {
    it('should provide user-friendly error messages', (done) => {
      service.generateResponse('test').subscribe({
        error: (error) => {
          expect(error).toBeInstanceOf(Error);
          expect(error.message).toBeTruthy();
          expect(error.message.length).toBeGreaterThan(0);
          done();
        }
      });

      const req = httpMock.expectOne(`${mockOllamaUrl}/api/generate`);
      req.error(new ErrorEvent('Network error'));
    });
  });
});
