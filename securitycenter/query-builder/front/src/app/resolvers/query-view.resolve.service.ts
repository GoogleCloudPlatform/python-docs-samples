import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, Router } from '@angular/router';
import { QueryService } from '../services/query.service';


@Injectable()
export class QueryViewResolve implements Resolve<any> {
  constructor(private queryService: QueryService, private router: Router) { }

  resolve(route: ActivatedRouteSnapshot): Promise<any> | boolean {
    this.queryService.setLoadingStatus(true);
    const queryId = route.params['id'];
    return this.queryService.getQuery(queryId).then(query => {
      this.queryService.setLoadingStatus(false);
      return query;
    })
    .catch(response => {
      return {};
    });
  }
}
