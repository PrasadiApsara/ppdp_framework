import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  API_URL = 'http://127.0.0.1:4449/';
  constructor(private http: HttpClient) { }

  getData(): Observable<any> {
      return this.http.get(`${this.API_URL}train`);
  }

  tryExperiment(): Observable<any> {
    return this.http.get(`${this.API_URL}psuedonimizedataset`);
  }

  tryExperimentKAnonymization(): Observable<any> {
    return this.http.get(`${this.API_URL}kanonimizedataset`);
  }

  psedoanonymize(tweet): Observable<any> {
    return this.http.post(`${this.API_URL}tag`, {sentence: tweet});
  }

  exportAndPseudoanonymize(text): Observable<any> {
    return this.http.post(`${this.API_URL}export`, {keyword: text});
  }

  evaluatePseudoanonymized(): Observable<any> {
    return this.http.get(`${this.API_URL}evaluate`);
  }

  exportAndKanonymize(text): Observable<any> {
    return this.http.post(`${this.API_URL}exportkanonymize`, {keyword: text});
  }
  getUtilityTest(): Observable<any> {
    return this.http.get(`${this.API_URL}utilityExperiment`);
  }
  getUtilityTestAnonymized(): Observable<any> {
    return this.http.get(`${this.API_URL}utilityExperimentAnonymize`);
  }
  getUtilityTestKAnonymized(): Observable<any> {
    return this.http.get(`${this.API_URL}utilityExperimentKAnonymize`);
  }
}
