import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { APP_BASE_HREF } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { QueryService } from './query.service';
import { SimpleQuery } from '../models/simple-query';
import { ExecutionResult } from '../models/execution-result';
import { SimpleQueryResult } from '../models/simple-query-result';
import { environment } from '../../environments/environment';
import { Query } from '../models/query';

describe('QueryService', () => {

  let service: QueryService;
  let backend: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        QueryService,
        { provide: APP_BASE_HREF, useValue : '/' },
      ],
      imports: [HttpClientModule, HttpClientTestingModule]
    });
    service = TestBed.get(QueryService);
    backend = TestBed.get(HttpTestingController);
  });

  it('creates the service', () => {
    expect(service).toBeTruthy();
  });

  it('getQueryList() returns a list of queries', fakeAsync(() => {
    let result: SimpleQueryResult;
    const query1 = new SimpleQuery('Query 1', 'Lorem ipsum sit dolor amet.', '04/03/1990', 1, 'thulio', null, null, null, null);
    const mockobj = new SimpleQueryResult([query1, query1], 1);
    const page = {
      currentPage: 1,
      pageSize: 10
    };
    const textSearch = 'teste';

    service.getQueryList(page.currentPage, page.pageSize, textSearch).then((response: SimpleQueryResult) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries?page=${page.currentPage}&page_size=${page.pageSize}&text=${textSearch}`);
    mock.flush(mockobj);
    tick();

    expect(result.queries).toEqual([query1, query1], ' ');
  }));

  it('getQuery() returns a query', fakeAsync(() => {
    let result: Query;
    const query = new Query('Query', 'description', [], 'topic', 'uuid', 'owner', 'schedule', false);
    const queryId = 1;

    service.getQuery(queryId).then((response: Query) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries/${queryId}`);
    mock.flush(query);
    tick();

    expect(result).toEqual(query, 'Query should be equal');
  }));

  it('deleteQuery() deletes a query', fakeAsync(() => {
    let result = {};
    const queryId = 1;

    service.deleteQuery(queryId).then(response => {
      result = response;
    });
    const mock = backend.expectOne(`${environment.apiUrl}/queries/${queryId}`);
    mock.flush({status: 200, message: 'Query deleted...'});
    tick();

    expect(result['status']).toEqual(200);
  }));

  it('cleanUpTempMarks() executes correct url', fakeAsync(() => {
    const queryUuid = '087d49d1-5296-4270-997c-9074d9079a5a';
    let result;

    service.cleanUpTempMarks(queryUuid).then((response: ExecutionResult) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/marks/clean/` + queryUuid);

    expect(mock.request.method).toEqual('DELETE');

    mock.flush({status: 200});
    tick();

    expect(result['status']).toEqual(200);
  }));

  it('runQueryById() returns a query given an id', fakeAsync(() => {
    const validResult = new ExecutionResult('https://www.google.com.br', 3, 'Mark42', 'uuid', 3);
    let result: ExecutionResult;
    const queryId = 1;

    service.runQueryById(queryId).then((response: ExecutionResult) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries/run/${queryId}`);
    mock.flush(validResult);
    tick();

    expect(result).toEqual(validResult, 'should return valid result');
  }));

  it('runQuery() executes a query without draft mode', fakeAsync(() => {
    const validResult = new ExecutionResult('https://www.google.com.br', 1, 'Mark42', 'uuid', 1);
    const query = new Query('Query', 'description', [], 'topic', 'uuid', 'owner', 'schedule', false);
    let result: ExecutionResult;

    service.runQuery(query, null).then((response: ExecutionResult) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries/run`);
    mock.flush(validResult);
    tick();

    expect(result).toEqual(validResult, 'should return valid result');
  }));

  it('runQuery() executes a query with draft mode', fakeAsync(() => {
    const validResult = new ExecutionResult('https://www.google.com.br', 1, 'Mark42', 'uuid', 1);
    const query = new Query('Query', 'description', [], 'topic', 'uuid', 'owner', 'schedule', false);
    let result: ExecutionResult;

    service.runQuery(query, true).then((response: ExecutionResult) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries/run?mode=draft`);
    mock.flush(validResult);
    tick();

    expect(result).toEqual(validResult, 'should return valid result');
  }));

  it('saveQuery() saves a query ', fakeAsync(() => {
    const query = new Query('Query', 'description', [], 'topic', 'uuid', 'owner', 'schedule', false);
    let result = {};

    service.saveQuery(query).then(response => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries`);
    mock.flush({status: 200});
    tick();

    expect(result['status']).toEqual(200);
  }));

  it('get and setLoadingStatus() sets the correct true boolean value', () => {
    service.setLoadingStatus(true);
    expect(service.getLoadingStatus()).toBeTruthy();
  });

  it('get and setLoadingStatus() sets the correct false boolean value', () => {
    service.setLoadingStatus(false);
    expect(service.getLoadingStatus()).toBeFalsy();
  });

  it('toggleNotification() executes query update', fakeAsync(() => {
    const queryUuid = '087d49d1-5296-4270-997c-9074d9079a5a';
    const expectedParams = {
      uuid: queryUuid,
      notifyFlag: true
    };
    let result;

    service.toggleNotification(queryUuid, true).then((response: ExecutionResult) => result = response);
    const mock = backend.expectOne(`${environment.apiUrl}/queries/notify`);

    expect(mock.request.method).toEqual('PUT');
    expect(mock.request.body).toEqual(JSON.stringify(expectedParams));
    mock.flush({status: 200});
    tick();

    expect(result['status']).toEqual(200);
  }));

});
