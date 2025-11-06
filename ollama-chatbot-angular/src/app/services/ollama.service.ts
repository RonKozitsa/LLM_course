import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { 
  OllamaConfig, 
  OllamaResponse, 
  OllamaGenerateRequest,
  ConnectionStatus 
} from '../models/chat.model';

@Injectable({
  providedIn: 'root'
})
export class OllamaService {
  private config: OllamaConfig = {
    url: 'http://localhost:11434',
    model: 'gemma3:1b',
    timeout: 120000
  };

  private connectionStatusSubject = new BehaviorSubject<ConnectionStatus>(
    ConnectionStatus.CONNECTING
  );
  public connectionStatus$ = this.connectionStatusSubject.asObservable();

  constructor(private http: HttpClient) {
    this.checkConnection();
  }

  /**
   * Check if Ollama server is reachable
   */
  checkConnection(): void {
    this.connectionStatusSubject.next(ConnectionStatus.CONNECTING);
    
    this.http.get(`${this.config.url}/api/tags`, { 
      observe: 'response',
      responseType: 'json'
    }).pipe(
      catchError(() => of(null))
    ).subscribe(response => {
      if (response && response.status === 200) {
        this.connectionStatusSubject.next(ConnectionStatus.CONNECTED);
      } else {
        this.connectionStatusSubject.next(ConnectionStatus.DISCONNECTED);
      }
    });
  }

  /**
   * Generate response from Ollama
   */
  generateResponse(prompt: string, model?: string): Observable<string> {
    const requestModel = model || this.config.model;
    const request: OllamaGenerateRequest = {
      model: requestModel,
      prompt: prompt,
      stream: false
    };

    return this.http.post<OllamaResponse>(
      `${this.config.url}/api/generate`,
      request,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    ).pipe(
      map(response => response.response),
      catchError(this.handleError)
    );
  }

  /**
   * Get current model
   */
  getCurrentModel(): string {
    return this.config.model;
  }

  /**
   * Set current model
   */
  setModel(model: string): void {
    this.config.model = model;
  }

  /**
   * Get Ollama URL
   */
  getUrl(): string {
    return this.config.url;
  }

  /**
   * Set Ollama URL
   */
  setUrl(url: string): void {
    this.config.url = url;
    this.checkConnection();
  }

  /**
   * Handle HTTP errors
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      if (error.status === 0) {
        errorMessage = 'Cannot connect to Ollama. Make sure it is running on localhost:11434';
      } else if (error.status === 404) {
        errorMessage = 'Model not found. Please check the model name or pull it using: ollama pull <model>';
      } else if (error.status === 500) {
        errorMessage = 'Server error. The model might be having issues processing your request.';
      } else {
        errorMessage = `Server returned code ${error.status}: ${error.message}`;
      }
    }

    return throwError(() => new Error(errorMessage));
  }
}
