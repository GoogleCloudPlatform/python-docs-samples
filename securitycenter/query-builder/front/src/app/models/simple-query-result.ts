import { SimpleQuery } from './simple-query';

export class SimpleQueryResult {
  queries: SimpleQuery[];
  total: number;

  constructor (queries, total) {
    this.queries = queries;
    this.total = total;
  }
}
