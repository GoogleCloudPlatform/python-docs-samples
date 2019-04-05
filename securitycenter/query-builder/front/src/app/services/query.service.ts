import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SimpleQuery } from '../models/simple-query';
import { Query } from '../models/query';
import { environment } from '../../environments/environment';
import { ExecutionResult } from '../models/execution-result';
import { SimpleQueryResult } from '../models/simple-query-result';

@Injectable({
  providedIn: 'root'
})
export class QueryService {

  constructor(private http: HttpClient) { }

  private loadingStatus: Boolean = false;
  private httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  };

  public setLoadingStatus(status: Boolean) {
    this.loadingStatus = status;
  }

  public getLoadingStatus() {
    return this.loadingStatus;
  }

  public getQueryList(page, pageSize, textSearch) {
    let uriQueryString = '?page=' + page + '&page_size=' + pageSize;

    if (textSearch) {
      uriQueryString += '&text=' + textSearch;
    }

    const getQueryListUrl = environment.apiUrl + '/queries' + uriQueryString;
    return this.http.get(getQueryListUrl, this.httpOptions)
               .toPromise()
               .then(response => response as SimpleQueryResult);
  }

  public getQuery(queryId) {
    const getQuery = environment.apiUrl + '/queries/' + queryId;
    return this.http.get(getQuery, this.httpOptions)
               .toPromise()
               .then(response => response as Query);
  }

  public deleteQuery(queryId) {
    const deleteQueryUrl = environment.apiUrl + '/queries/' + queryId;
    return this.http.delete(deleteQueryUrl, this.httpOptions)
               .toPromise()
               .then(response => response as ExecutionResult);
  }

  public runQueryById(queryId) {
    const runQueryUrl = environment.apiUrl + '/queries/run/' + queryId;
    return this.http.post(runQueryUrl, this.httpOptions)
               .toPromise()
               .then(response => response as ExecutionResult);
  }

  public runQuery(query: Query, draftMode: boolean) {
    let runQueryURL = environment.apiUrl + '/queries/run';
    if (draftMode) {
      runQueryURL += '?mode=draft';
    }
    return this.http.post(runQueryURL, JSON.stringify(query), this.httpOptions)
               .toPromise()
               .then(response => response as ExecutionResult);
  }

  public saveQuery(query: Query) {
    const saveQueryUrl = environment.apiUrl + '/queries';
    return this.http.post(saveQueryUrl, JSON.stringify(query), this.httpOptions)
               .toPromise()
               .then(response => response as ExecutionResult);
  }

  public toggleNotification(uuid: string, notifyFlag: boolean) {
    const updateNotifyUrl = environment.apiUrl + '/queries/notify';
    const payload = {
      uuid: uuid,
      notifyFlag: notifyFlag
    };
    return this.http.put(updateNotifyUrl, JSON.stringify(payload), this.httpOptions)
               .toPromise()
               .then(response => response);
  }

  public cleanUpTempMarks(uuid: string) {
    const cleanMarkUrl = environment.apiUrl + '/marks/clean/' + uuid;
    return this.http.delete(cleanMarkUrl, this.httpOptions)
               .toPromise()
               .then(response => response);
  }
}
