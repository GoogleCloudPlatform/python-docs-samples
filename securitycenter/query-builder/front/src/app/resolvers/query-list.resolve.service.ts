import { Injectable, OnInit } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot } from '@angular/router';
import { QueryService } from '../services/query.service';
import {SessionErrorHandler} from '../handlers/session-error-handler';

@Injectable()
export class QueryListResolve implements Resolve<any> {
  constructor(private queryService: QueryService, private sessionErrorHandler: SessionErrorHandler) { }

   resolve(route: ActivatedRouteSnapshot): Promise<any> | boolean {
    this.queryService.setLoadingStatus(true);
    const pageIndex = 1;
    const pageSize = 10;
    return this.queryService.getQueryList(pageIndex, pageSize, null).then(queries => {
      this.queryService.setLoadingStatus(false);
      if (queries) {
        return queries;
      }
      return {error: 'Session Expired'};
    }).catch((err) => {
      return {'error': 'Session Expired'};
    });
  }
}
